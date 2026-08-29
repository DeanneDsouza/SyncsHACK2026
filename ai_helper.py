"""
AI helper for "Before We Forget".

UNESCO's ich001 dataset only gives us ONE description field per
record - there's no separate "history" data to show on a
Wikipedia-style page. This module asks Claude to reorganize and
lightly expand that single description into an Overview + History
pair, using ONLY the facts UNESCO already gave us.

NOTE: Tutorial and "Connect with Other People" are NOT generated
here. Tutorial is left as an empty placeholder in the template for
now (see _wiki_article.html) - wire it up here later the same way
overview/history are done, once you're ready to spend the extra
tokens on it. "Connect with Other People" is static content in the
template, not AI-generated at all.

Design choices worth knowing about:

- Cached in the `ai_cache` DB table, keyed by a hash of the record's
  name + description. Since get_single_record() already picks the
  same record all day (see app.py), this means ONE API call per
  record per day, not one per page view.
- The prompt explicitly forbids inventing facts not present in the
  source description, and asks Claude to say so plainly instead of
  fabricating when the source doesn't cover a section - this matters
  in a cultural-heritage app where "history" you can't verify is
  worse than no history at all.
- Every failure mode (no API key set, package not installed, network
  error, malformed JSON back) returns None rather than raising -
  the templates already fall back to showing the raw UNESCO
  description in the Overview section when `art.sections` is None.
"""

import os
import json
import hashlib

MODEL = "claude-sonnet-5"
SECTION_KEYS = ["overview", "history"]


def _cache_key(name, description):
    raw = f"{name}|{description}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _get_cached(db, cache_key):
    row = db.execute(
        "SELECT sections_json FROM ai_cache WHERE cache_key = ?",
        (cache_key,)
    ).fetchone()
    return json.loads(row["sections_json"]) if row else None


def _save_cache(db, cache_key, sections):
    db.execute(
        "INSERT OR REPLACE INTO ai_cache (cache_key, sections_json) VALUES (?, ?)",
        (cache_key, json.dumps(sections))
    )
    db.commit()


def _build_prompt(name, description, country, category):
    return f"""You are helping structure an encyclopedia-style page about a UNESCO
Intangible Cultural Heritage practice.

Practice: {name}
Country: {country}
Category: {category}

Official UNESCO description (this is your ONLY source of facts):
\"\"\"{description}\"\"\"

Using ONLY the information in that description, reorganize and lightly
expand it into two short sections for a wiki-style page. Do not invent
specific facts, dates, names, or statistics that are not in the source
description. If the description doesn't cover a section in any detail,
write one honest sentence saying UNESCO's summary doesn't go into
detail there - do not make something up to fill the space.

Respond with ONLY valid JSON, no other text, no markdown code fences,
in exactly this shape:
{{
  "overview": "2-3 sentences, a general-audience summary",
  "history": "short paragraph on origins and history, if present in the source"
}}"""


def generate_sections(db, name, description, country, category):
    """
    Returns a dict with keys overview/history/significance/practice,
    or None if AI generation isn't available/configured or fails -
    callers should treat None as "just show the raw description".
    """

    if not description:
        return None

    cache_key = _cache_key(name, description)
    cached = _get_cached(db, cache_key)
    if cached:
        return cached

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("ANTHROPIC_API_KEY not set - skipping AI section generation.")
        return None

    try:
        import anthropic
    except ImportError:
        print("anthropic package not installed - run: pip install anthropic")
        return None

    try:
        client = anthropic.Anthropic()

        message = client.messages.create(
            model=MODEL,
            max_tokens=800,
            messages=[
                {"role": "user", "content": _build_prompt(name, description, country, category)}
            ]
        )

        text = "".join(
            block.text for block in message.content if block.type == "text"
        ).strip()

        # Defensive cleanup in case Claude wraps the JSON in a code
        # fence despite being told not to.
        text = text.replace("```json", "").replace("```", "").strip()

        sections = json.loads(text)

        if not all(key in sections for key in SECTION_KEYS):
            print("AI response missing expected keys:", sections.keys())
            return None

        _save_cache(db, cache_key, sections)
        return sections

    except Exception as e:
        print("AI section generation failed:", e)
        return None
