"""
Curated content for "Before We Forget".

First-round version: each (country, category) combination has exactly
ONE fixed, standard art form - no rotation, no live filtering. Every
entry was picked by hand for one reason: it's something a person can
actually attempt in a short session with ordinary materials - not a
festival, ritual, or multi-year apprenticeship craft. That's a
judgment call no public API (UNESCO or otherwise) can make reliably,
so it's made once here instead of guessed at on every request.

Structure: ART_DATA[country][category] -> a single dict:
    name            - display name
    image_url       - path under /static, or None (falls back to no image)
    overview        - 2-3 sentence summary
    history         - short paragraph on origins
    materials       - list of strings, what you need to try it (optional)
    tutorial_steps  - list of strings, ordered steps (required - this is
                       the whole point of the app)
    learn_more_url  - optional external link for further reading

To change the featured topic for a combination, just edit that dict
in place. To bring back daily rotation later, change the value back
to a list of dicts and swap get_today_pick() in app.py to pick from
it (random.choice / date-seeded, same pattern as before).
"""

ART_DATA = {'China': {'Art & Crafts': {'name': 'Jianzhi (Chinese Paper Cutting)',
                            'image_url': None,
                            'overview': 'Jianzhi is the Chinese folk art of cutting intricate '
                                        'designs out of paper, traditionally used to decorate '
                                        'windows and doors, especially around Lunar New Year.',
                            'history': 'Paper cutting developed in China not long after paper '
                                       'itself was invented, around the 6th century, and spread '
                                       'into everyday folk decoration over the following '
                                       'centuries. Red paper cut-outs of characters like the '
                                       'double-happiness symbol remain a common sight at weddings '
                                       'and festivals.',
                            'materials': ['A square piece of paper',
                                          'Scissors',
                                          'Pencil (optional, for sketching a guide first)'],
                            'tutorial_steps': ['Fold your square of paper in half, then in half '
                                               'again, so you have a smaller square or triangle.',
                                               'Lightly sketch a simple shape along the folded '
                                               'edges - a flower petal, a leaf, or a simple '
                                               'geometric pattern works well for a first attempt.',
                                               'Cut along your pencil lines through all the folded '
                                               'layers, leaving some folded edges uncut so the '
                                               'design stays connected.',
                                               'Carefully unfold the paper to reveal a symmetrical '
                                               'pattern.',
                                               'Press it flat, and try displaying it against a '
                                               'window so light shows through the cut-out shapes.'],
                            'learn_more_url': 'https://en.wikipedia.org/wiki/Paper_cutting'},
           'Music': {'name': 'Pentatonic Melody (Guzheng-style)',
                     'image_url': None,
                     'overview': 'Traditional Chinese melodies are very often built from a '
                                 'five-note (pentatonic) scale rather than the seven-note scale '
                                 'common in Western pop music, giving them their distinctive open, '
                                 'airy sound.',
                     'history': 'The pentatonic scale has been central to Chinese music for '
                                'thousands of years and underlies traditional instruments like the '
                                'guzheng (a plucked zither) and the erhu (a bowed two-string '
                                'fiddle), as well as countless folk songs.',
                     'materials': ['Any instrument you have access to (piano, guitar, xylophone, '
                                   'even a phone piano app)'],
                     'tutorial_steps': ['On a piano or keyboard, play only the black keys - these '
                                        'happen to form a pentatonic scale, so anything you play '
                                        "using only them will sound 'right' together.",
                                        'On a guitar or other instrument, use the notes C, D, E, '
                                        'G, A (in any octave) as your five-note palette.',
                                        'Play those five notes slowly, one at a time, and listen '
                                        'to how they relate to each other.',
                                        'Try composing your own short 4-8 note phrase using only '
                                        "those five notes - there's no wrong answer, since any "
                                        'combination of them tends to sound harmonious.',
                                        'Repeat your phrase a few times, varying the rhythm, the '
                                        'way traditional melodies are often built from a repeating '
                                        'core idea.'],
                     'learn_more_url': 'https://en.wikipedia.org/wiki/Guzheng'},
           'Literature': {'name': 'The Farmer Waiting by the Stump',
                          'image_url': None,
                          'overview': 'A short, well-known Chinese fable about a farmer who gives '
                                      'up working his field after a lucky accident, hoping the '
                                      'same luck will repeat itself.',
                          'history': 'This story comes from a set of ancient Chinese fables '
                                     'collected over two thousand years ago and survives today as '
                                     'a common four-character idiom people still use to describe '
                                     'someone relying on luck instead of effort.',
                          'tutorial_steps': ['Read the retelling: A farmer was working his field '
                                             'one day when a hare, running in fright, crashed '
                                             'headfirst into a tree stump and died instantly. '
                                             'Delighted at the free meal, the farmer picked it up '
                                             'and took it home.',
                                             'The next day, instead of returning to his work, he '
                                             'sat by the stump, waiting for another hare to come '
                                             'running into it.',
                                             'No hare came. He waited the next day, and the next, '
                                             'neglecting his field entirely, until his crops '
                                             'withered and the other villagers began to laugh at '
                                             'him.',
                                             'Now try it yourself: write a short 4-6 sentence '
                                             'version of this same story in your own words, or '
                                             'invent a modern equivalent (someone waiting for a '
                                             'one-off stroke of luck to repeat itself).'],
                          'learn_more_url': 'https://en.wikipedia.org/wiki/Chinese_idiom'}},
 'India': {'Art & Crafts': {'name': 'Warli Painting',
                            'image_url': None,
                            'overview': 'Warli painting is a simple, geometric folk art style from '
                                        'Maharashtra, built almost entirely from circles, '
                                        'triangles, and straight lines to depict everyday village '
                                        'life.',
                            'history': 'The style is named after the Warli tribal community and '
                                       'was traditionally painted with rice paste on the mud walls '
                                       'of homes, often to mark harvests, weddings, or other '
                                       'important occasions, long before it became known outside '
                                       'the community.',
                            'materials': ['White paint, chalk, or white crayon',
                                          'Dark or reddish-brown paper (or any paper - a brown '
                                          'paper bag works)',
                                          'A thin brush or cotton bud'],
                            'tutorial_steps': ['Draw one central circle - this often represents '
                                               'the sun, a tree, or a village gathering point.',
                                               'Around it, add a ring of simple triangle-based '
                                               'figures: two triangles joined at a point make a '
                                               'basic human figure (a small triangle for the '
                                               'torso, a bigger one below for the skirt/legs).',
                                               'Add smaller triangles for animals - a single '
                                               'elongated triangle with four thin lines for legs '
                                               'makes a simple deer or dog.',
                                               'Connect the figures with thin straight or wavy '
                                               'lines suggesting paths, fields, or dancing '
                                               'circles.',
                                               'Keep every shape built only from circles, '
                                               'triangles, and straight lines - that constraint is '
                                               'the whole style.'],
                            'learn_more_url': 'https://en.wikipedia.org/wiki/Warli_painting'},
           'Music': {'name': 'Basic Tabla Bol Pattern',
                     'image_url': None,
                     'overview': "Tabla drumming is built from spoken syllables called 'bols' that "
                                 'represent specific strokes - learning to speak a rhythm before '
                                 'you play it is the traditional starting point.',
                     'history': 'The tabla has been central to North Indian classical and folk '
                                'music for centuries, and its bol system - reciting syllables like '
                                'dha, dhin, na, tin - is used to teach and pass down rhythmic '
                                'patterns without written notation.',
                     'materials': ['Any hand drum, or just your hands on a table'],
                     'tutorial_steps': ["Say this basic pattern out loud slowly, evenly: 'dha - "
                                        "dhin - dhin - dha - dha - dhin - dhin - dha'.",
                                        "Now tap it out: 'dha' = a firm hit near the centre of the "
                                        "drum (or flat table), 'dhin' = a slightly lighter hit "
                                        'closer to the edge.',
                                        'Practice saying and tapping it together until the rhythm '
                                        'feels steady.',
                                        'Once comfortable, loop the 8-beat pattern continuously - '
                                        'this is the same way many tabla rhythms (taals) are '
                                        'learned, as a repeating cycle.'],
                     'learn_more_url': 'https://en.wikipedia.org/wiki/Tabla'},
           'Literature': {'name': 'The Monkey and the Crocodile',
                          'image_url': None,
                          'overview': 'A short animal fable from the Panchatantra, an ancient '
                                      'Indian collection of moral stories, about a clever monkey '
                                      'who outwits a crocodile trying to trick him.',
                          'history': 'The Panchatantra is one of the oldest known collections of '
                                     'fables in the world, compiled roughly two thousand years '
                                     'ago, and its stories have since spread across many cultures '
                                     'and languages.',
                          'tutorial_steps': ['Read the retelling: A monkey lived in a tree by a '
                                             'river and became friends with a crocodile, sharing '
                                             'fruit with him every day.',
                                             "The crocodile's wife grew jealous and demanded the "
                                             "monkey's heart, believing it must be as sweet as the "
                                             'fruit he ate. The crocodile reluctantly agreed to '
                                             'bring the monkey home under false pretences.',
                                             'Partway across the river, the crocodile admitted the '
                                             "plan. Thinking quickly, the monkey said he'd left "
                                             'his heart back in the tree, and offered to fetch it '
                                             'if the crocodile turned around.',
                                             'Now try it yourself: write your own short fable '
                                             'where a smaller, clever character outsmarts a '
                                             'bigger, more powerful one - a common pattern across '
                                             'folk stories worldwide.'],
                          'learn_more_url': 'https://en.wikipedia.org/wiki/Panchatantra'}},
 'Australia': {'Art & Crafts': {'name': 'Dot-Pattern Painting',
                                'image_url': None,
                                'overview': 'Dot painting is a technique widely associated with '
                                            'Aboriginal Australian art, where designs are built up '
                                            'entirely from small, carefully placed dots of colour.',
                                'history': 'Dot painting as widely seen today became prominent '
                                           'from the 1970s onward, particularly from Central '
                                           'Desert communities, though it draws on much older '
                                           'traditions of symbolic mark-making. Specific symbols '
                                           'and stories used by individual Aboriginal artists and '
                                           'communities are often culturally owned - this activity '
                                           'is a general introduction to the dotting technique '
                                           "itself, not a reproduction of any specific community's "
                                           'designs.',
                                'materials': ['Paper or card',
                                              'Paint (acrylic works well) or coloured markers',
                                              'A cotton bud, the end of a paintbrush handle, or a '
                                              'toothpick'],
                                'tutorial_steps': ['Lightly sketch a simple outline shape of your '
                                                   'choice - it could be a spiral, a simple animal '
                                                   'silhouette, or just a few connected circles.',
                                                   'Dip your cotton bud or brush handle tip into '
                                                   'paint and place a single dot along your '
                                                   'outline.',
                                                   'Continue placing dots closely together along '
                                                   'the whole outline, keeping the spacing as even '
                                                   'as you can.',
                                                   'Fill in larger areas by layering dots of two '
                                                   'or three related colours close together rather '
                                                   'than using a solid block of colour.',
                                                   'Step back periodically to check the overall '
                                                   'pattern - dot painting rewards patience and '
                                                   'rhythm over speed.'],
                                'learn_more_url': 'https://en.wikipedia.org/wiki/Australian_Aboriginal_art'},
               'Music': {'name': 'Clapstick Rhythm Pattern',
                         'image_url': None,
                         'overview': 'Clapsticks (also called bilma or bimbirr in some languages) '
                                     'are simple percussion sticks used across many Aboriginal '
                                     'communities to keep rhythm, often alongside song and '
                                     'didgeridoo.',
                         'history': 'Clapsticks are among the oldest and most widespread musical '
                                    'instruments used in Aboriginal Australia, with rhythmic '
                                    'patterns and songs varying between different language groups '
                                    'and regions.',
                         'materials': ['Two sturdy sticks, or two wooden spoons'],
                         'tutorial_steps': ['Hold one stick in each hand and strike them together '
                                            'on a steady, even beat: tap-tap-tap-tap.',
                                            'Once that feels steady, group the beats in fours, '
                                            'with a very slightly stronger tap on the first beat '
                                            'of each group of four.',
                                            'Try adding a short pause after every fourth group, '
                                            'then resuming - simple rests like this are common in '
                                            'call-and-response rhythm traditions.',
                                            'Practice keeping the tempo completely steady for a '
                                            'minute or two without speeding up, which is harder '
                                            'than it sounds.'],
                         'learn_more_url': 'https://en.wikipedia.org/wiki/Clapstick'},
               'Literature': {'name': 'Write Your Own Origin Story',
                              'image_url': None,
                              'overview': 'Rather than retelling a specific sacred story - many '
                                          'traditional Aboriginal Dreaming stories are owned by, '
                                          'and specific to, particular communities and are not '
                                          'appropriate to reproduce outside that context - this '
                                          'activity invites you to try the storytelling form '
                                          'itself: a short oral tale explaining how something in '
                                          'the natural world came to be.',
                              'history': 'Oral storytelling explaining the origins of landscapes, '
                                         'animals, and natural features is one of the oldest and '
                                         'most widespread literary traditions in the world, and '
                                         'Aboriginal oral storytelling traditions in Australia are '
                                         'among the longest continuously practiced in human '
                                         'history.',
                              'tutorial_steps': ['Pick a small natural feature you can observe '
                                                 'near you - a hill, a particular tree, an animal, '
                                                 'a pattern in the stars.',
                                                 'Invent a short explanation for how it came to '
                                                 "look or behave the way it does - it doesn't need "
                                                 'to be scientifically accurate, just a satisfying '
                                                 'short story.',
                                                 'Tell it out loud to someone, the way oral '
                                                 'traditions are passed on, rather than only '
                                                 'writing it down.',
                                                 "If you'd like to learn about real Aboriginal "
                                                 'Dreaming stories respectfully, look for stories '
                                                 'that community members and cultural '
                                                 'organisations have specifically chosen to share '
                                                 'publicly, rather than secondhand retellings.'],
                              'learn_more_url': 'https://en.wikipedia.org/wiki/Dreaming_(Australian_Aboriginal_art)'}}}
