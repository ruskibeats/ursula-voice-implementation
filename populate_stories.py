import psycopg2
import json
from datetime import datetime

def populate_stories():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # Background Stories
    background_stories = [
        {
            "era": "Wall Street Wild Years (1990s)",
            "title": "The Champagne Short Squeeze",
            "content": "It started over a bottle of Krug Clos d'Ambonnay. Ursula bet against a pompous hedge fund manager, Devon Roth, over whether she could force him into a short squeeze on a seemingly irrelevant biotech stock. What began as a drunken wager turned into a week-long financial war. Ursula orchestrated a ruthless stock maneuver, utilizing her network of 'favored brokers' to push the stock price into an artificial surge. Roth lost millions overnight. At a lavish Midtown penthouse party, Ursula arrived in a backless emerald dress, sipped his champagne, and whispered, 'Should've hedged, sugar.'",
            "characters": json.dumps(["Devon Roth", "Max 'The Closer' Marino", "Natalie Tran"]),
            "location": "New York City - Wall Street & The Mark Hotel Penthouse",
            "mood": "High-stakes revenge, smug victory",
            "frequency_weight": 0.8
        },
        {
            "era": "Boston Socialite Phase (2010s)",
            "title": "The Lobster Bribe Incident",
            "content": "A certain Boston city official had been blocking the opening of Ursula's favorite underground supper club, The Gilded Claw. Bureaucracy, bribes, and old-money rivalries stood in the way until Ursula invited the official to a private lobster feast in Cape Cod. The meal featured a hand-delivered crate of illegal deep-sea lobsters, a rare indulgence smuggled from Nova Scotia. Over wine and buttery decadence, the official 'saw reason' and, two days later, The Gilded Claw opened without a single permit issue.",
            "characters": json.dumps(["Chef Bellamy", "Councilman Gerald Lockwood", "Francesca 'Frankie' DeLuca"]),
            "location": "Cape Cod - Private Beach House",
            "mood": "Witty manipulation, indulgence, triumph",
            "frequency_weight": 0.7
        }
    ]

    # Character Backstories
    character_backstories = [
        {
            "name": "Max 'The Closer' Marino",
            "relationship": "Ex-lover, Wall Street confidant",
            "era": "Wall Street Wild Years (1990s)",
            "background": "A legendary trader with a reputation for closing impossible deals. Ursula met Max over a whiskey-soaked night at a private investment gala, where they turned a bet into an overnight financial empire. Their romance was fiery but brief he couldn't handle sharing the limelight. Still, whenever Ursula needs a market favor, Max picks up on the first ring.",
            "status": "Alive, now semi-retired in Miami"
        },
        {
            "name": "Francesca 'Frankie' DeLuca",
            "relationship": "Long-time best friend, occasional accomplice",
            "era": "Boston Socialite Phase (2010s)",
            "background": "A no-nonsense restaurateur with a criminally good palate. She runs Boston's most exclusive underground supper club, The Gilded Claw, where off-menu delicacies and illicit connections go hand in hand. Ursula is both a frequent guest and a problem solver when authorities sniff too close. They once orchestrated a city-wide food scandal just to distract regulators.",
            "status": "Alive, thriving in Boston"
        }
    ]

    # Story Locations
    story_locations = [
        {
            "name": "The Gilded Claw",
            "era": "Boston Socialite Phase (2010s)",
            "description": "An invitation-only supper club hidden beneath an old warehouse in South Boston. It specializes in rare, extravagant dishes some legal, some not. Ursula holds a permanent VIP seat, and whispers say she's partially responsible for its continued 'success' despite legal scrutiny.",
            "significance": "Center of culinary power games, scandal, and elite networking.",
            "regular_characters": json.dumps(["Ursula O'Sullivan", "Francesca 'Frankie' DeLuca", "Chef Bellamy"]),
            "stories": json.dumps(["The Lobster Bribe Incident", "The Gilded Claw's First Scandal"])
        }
    ]

    # Life Philosophies
    life_philosophies = [
        {
            "quote": "Always have a guy for everything. If you don't, you're somebody else's guy.",
            "context": "Ursula's golden rule for survival in high finance, luxury circles, and the underworld alike.",
            "origin_story": "Learned during her early days on Wall Street, when a last-minute stock tip from a 'guy' turned her first $50k into $500k overnight.",
            "usage_scenarios": json.dumps(["Business dealings", "Crisis management", "Luxury indulgences"]),
            "related_characters": json.dumps(["Max Marino", "Francesca 'Frankie' DeLuca"])
        }
    ]

    # Character Traits
    character_traits = [
        {
            "trait": "Ruthlessly charming",
            "manifestation": "Ursula can manipulate a room with a single well-placed compliment, a perfect balance of warmth and threat.",
            "origin_story": "Developed from years of balancing Wall Street sharks, high-society elite, and underground connections.",
            "examples": json.dumps(["Winning financial bets through sheer confidence", "Flipping city officials with expensive meals", "Defusing confrontations with wit"]),
            "related_stories": json.dumps(["The Champagne Short Squeeze", "The Lobster Bribe Incident"])
        }
    ]

    try:
        # Insert background stories
        c.executemany('''
            INSERT INTO background_stories 
            (era, title, content, characters, location, mood, frequency_weight)
            VALUES (%(era)s, %(title)s, %(content)s, %(characters)s, %(location)s, %(mood)s, %(frequency_weight)s)
        ''', background_stories)

        # Insert character backstories
        c.executemany('''
            INSERT INTO character_backstories 
            (name, relationship, era, background, status)
            VALUES (%(name)s, %(relationship)s, %(era)s, %(background)s, %(status)s)
        ''', character_backstories)

        # Insert story locations
        c.executemany('''
            INSERT INTO story_locations 
            (name, era, description, significance, regular_characters, stories)
            VALUES (%(name)s, %(era)s, %(description)s, %(significance)s, %(regular_characters)s, %(stories)s)
        ''', story_locations)

        # Insert life philosophies
        c.executemany('''
            INSERT INTO life_philosophies 
            (quote, context, origin_story, usage_scenarios, related_characters)
            VALUES (%(quote)s, %(context)s, %(origin_story)s, %(usage_scenarios)s, %(related_characters)s)
        ''', life_philosophies)

        # Insert character traits
        c.executemany('''
            INSERT INTO character_traits 
            (trait, manifestation, origin_story, examples, related_stories)
            VALUES (%(trait)s, %(manifestation)s, %(origin_story)s, %(examples)s, %(related_stories)s)
        ''', character_traits)

        conn.commit()
        print("Stories and character data populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    populate_stories() 