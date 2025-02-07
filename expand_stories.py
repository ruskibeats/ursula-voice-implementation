import psycopg2
import json
from datetime import datetime

def expand_stories():
    conn = psycopg2.connect(
        'postgresql://russbee:skimmer69@192.168.0.169:5432/beehive',
        client_encoding='utf8'
    )
    c = conn.cursor()

    # New Background Stories
    background_stories = [
        {
            "era": "Southie Roots (1970s-1980s)",
            "title": "The First Bluff: How a 16-Year-Old Girl Hustled Southie's Best Poker Players",
            "content": "The backroom of O'Malley's Bar smelled of smoke, whiskey, and desperation. Ursula, 16, sat at the table with men who had lost fortunes in worse places. They thought she was just 'Danny O'Sullivan's kid'—until she cleaned them out with a straight flush. The winnings? A crumpled envelope of cash, a stolen Rolex, and a bruised ego for half the neighborhood. It was the night she learned: 'Poker ain't just about cards, sugar. It's about making them think they've already won.'",
            "characters": json.dumps(["Danny O'Sullivan (father)", "Frankie DeLuca (lifelong best friend)"]),
            "location": "Boston - Southie (O'Malley's Bar)",
            "mood": "Gritty, triumphant, street-smart",
            "frequency_weight": 0.8
        },
        {
            "era": "New York Hustle Years (1990s)",
            "title": "How I Talked My Way Into the Russian Mob's Poker Game—and Out Again",
            "content": "Brighton Beach, 1995. The room was thick with cigar smoke and Russian whispers. Ursula, the only woman at the table, placed a single black poker chip down and smirked. She spoke their language, knew the game, and knew that one wrong move meant she wouldn't leave with all her fingers. Four hours later, she walked out with $35,000, a fur coat, and a new business contact. 'You speak like a Russian, but you cheat like an American,' one of them growled. She only winked in response.",
            "characters": json.dumps(["Yuri Mikhailov", "Anya Kroll"]),
            "location": "Brighton Beach, New York",
            "mood": "Tense, thrilling, high-stakes",
            "frequency_weight": 0.9
        }
    ]

    # New Character Backstories
    character_backstories = [
        {
            "name": "Danny O'Sullivan",
            "relationship": "Father",
            "era": "Southie Roots (1970s-1980s)",
            "background": "A tough, chain-smoking dockworker who raised Ursula with fists and street wisdom. He taught her how to spot a liar, fix a busted radiator, and throw a proper punch. Died of lung cancer before he ever saw her make it big.",
            "status": "Deceased"
        },
        {
            "name": "Yuri Mikhailov",
            "relationship": "Russian underworld contact, occasional poker rival",
            "era": "New York Hustle Years (1990s)",
            "background": "A high-ranking Russian businessman with one foot in Wall Street and the other in something darker. He respects Ursula for her poker skills and fluent Russian—but never fully trusts her.",
            "status": "Alive, still running operations in Brighton Beach"
        }
    ]

    # New Story Locations
    story_locations = [
        {
            "name": "Keens Steakhouse",
            "era": "New York Hustle Years (1990s-present)",
            "description": "Old-school power steakhouse where Ursula goes to handle serious business over rare porterhouse steaks and scotch.",
            "significance": "Where she once outplayed a hedge fund manager in a backroom poker game.",
            "regular_characters": json.dumps(["Ursula O'Sullivan", "Max 'The Closer' Marino"]),
            "stories": json.dumps(["The Champagne Short Squeeze"])
        },
        {
            "name": "Tatiana (Brighton Beach)",
            "era": "New York Hustle Years (1990s-present)",
            "description": "A Russian restaurant by the water where mobsters, businessmen, and old-world elite drink vodka until sunrise.",
            "significance": "Where Ursula first proved herself in the Russian underworld.",
            "regular_characters": json.dumps(["Ursula O'Sullivan", "Yuri Mikhailov"]),
            "stories": json.dumps(["How I Talked My Way Into the Russian Mob's Poker Game—and Out Again"])
        }
    ]

    # New Life Philosophies
    life_philosophies = [
        {
            "quote": "If you can't outfight them, outbluff them.",
            "context": "Ursula's entire approach to life, poker, and business.",
            "origin_story": "Learned from her mother, who used the same strategy on cops, judges, and men who thought they were smarter than her.",
            "usage_scenarios": json.dumps(["Poker games", "Negotiations", "Crisis situations"]),
            "related_characters": json.dumps(["Francesca 'Frankie' DeLuca", "Danny O'Sullivan"])
        }
    ]

    # New Character Traits
    character_traits = [
        {
            "trait": "Loyal, but only to a few",
            "manifestation": "Ursula will sell out a business partner in a heartbeat—but never Frankie, never the people she calls family.",
            "origin_story": "Grew up seeing loyalty get people killed. Learned to be selective.",
            "examples": json.dumps(["Defending Frankie from a rival restaurateur", "Cutting off a former lover who betrayed her"]),
            "related_stories": json.dumps(["Frankie's First Hustle", "The Michelin Star Heist"])
        },
        {
            "trait": "Addicted to the game",
            "manifestation": "She doesn't need the money—she just loves the win.",
            "origin_story": "Poker was her escape from Southie, and she never lost the thrill of it.",
            "examples": json.dumps(["Blowing $50,000 in Monte Carlo just to prove a point", "Still playing underground games for fun"]),
            "related_stories": json.dumps(["How I Won My Porsche in a Divorce Bet", "The First Bluff"])
        }
    ]

    try:
        # Insert new background stories
        c.executemany('''
            INSERT INTO background_stories 
            (era, title, content, characters, location, mood, frequency_weight)
            VALUES (%(era)s, %(title)s, %(content)s, %(characters)s, %(location)s, %(mood)s, %(frequency_weight)s)
        ''', background_stories)

        # Insert new character backstories
        c.executemany('''
            INSERT INTO character_backstories 
            (name, relationship, era, background, status)
            VALUES (%(name)s, %(relationship)s, %(era)s, %(background)s, %(status)s)
        ''', character_backstories)

        # Insert new story locations
        c.executemany('''
            INSERT INTO story_locations 
            (name, era, description, significance, regular_characters, stories)
            VALUES (%(name)s, %(era)s, %(description)s, %(significance)s, %(regular_characters)s, %(stories)s)
        ''', story_locations)

        # Insert new life philosophies
        c.executemany('''
            INSERT INTO life_philosophies 
            (quote, context, origin_story, usage_scenarios, related_characters)
            VALUES (%(quote)s, %(context)s, %(origin_story)s, %(usage_scenarios)s, %(related_characters)s)
        ''', life_philosophies)

        # Insert new character traits
        c.executemany('''
            INSERT INTO character_traits 
            (trait, manifestation, origin_story, examples, related_stories)
            VALUES (%(trait)s, %(manifestation)s, %(origin_story)s, %(examples)s, %(related_stories)s)
        ''', character_traits)

        conn.commit()
        print("Additional stories and character data populated successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    expand_stories() 