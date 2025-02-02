import sqlite3
import json
import logging
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UrsulaDB:
    def __init__(self):
        self.db_path = 'ursula.db'
        
    def _get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            raise

    def get_patterns_by_type(self, pattern_type: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pattern_type, pattern, context, success_rating, metadata
                FROM interaction_patterns 
                WHERE pattern_type = ? AND success_rating > 0.7
                ORDER BY last_used DESC
            ''', (pattern_type,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting patterns: {e}")
            return []
        finally:
            conn.close()

    def get_relationship(self, person: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM relationships WHERE person_name = ?",
                (person,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting relationship: {e}")
            return None
        finally:
            conn.close()

    def get_stories(self, category: str, mood: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM stories WHERE category = ?"
            params = [category]
            if mood:
                query += " AND mood = ?"
                params.append(mood)
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting stories: {e}")
            return []
        finally:
            conn.close()

    def store_memory(self, category: str, content: Dict[str, Any], context: str) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO memory_updates 
                   (category, content, context) VALUES (?, ?, ?)""",
                (category, json.dumps(content), context)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error storing memory: {e}")
            return False
        finally:
            conn.close()

    def update_pattern_success(self, pattern_id: int, success_rating: float) -> bool:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE interaction_patterns 
                   SET success_rating = ?, last_used = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (success_rating, pattern_id)
            )
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating pattern success: {e}")
            return False
        finally:
            conn.close()

    def get_character_trait(self, trait_type: Optional[str] = None) -> Dict[str, Any]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            if trait_type:
                cursor.execute(
                    """SELECT trait_type, trait_value, ssml_impact, description
                       FROM character_traits WHERE trait_type = ?""",
                    (trait_type,)
                )
            else:
                cursor.execute("SELECT * FROM core_identity LIMIT 1")
            row = cursor.fetchone()
            return dict(row) if row else {}
        except Exception as e:
            logger.error(f"Error getting character traits: {e}")
            return {}
        finally:
            conn.close()

    def build_scene(self, template_name: str, content: Dict[str, Any]) -> Optional[str]:
        try:
            patterns = self.get_patterns_by_type(content.get('type', 'default'))
            if not patterns:
                return None
            
            pattern = patterns[0]['pattern']
            return pattern.format(**content)
        except Exception as e:
            logger.error(f"Error building scene: {e}")
            return None

    def get_required_phrase(self, phrase_type: str) -> List[str]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT pattern FROM interaction_patterns 
                   WHERE pattern_type = ? AND success_rating > 0.7
                   ORDER BY last_used DESC LIMIT 5""",
                (phrase_type,)
            )
            return [row['pattern'] for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting phrases: {e}")
            return []
        finally:
            conn.close()

    def get_ssml_pattern(self, pattern_type: str, pattern_name: str) -> Optional[Dict]:
        """Get a specific SSML pattern"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pattern_type, pattern_name, ssml_pattern, description
                FROM ssml_patterns
                WHERE pattern_type = ? AND pattern_name = ?
            ''', (pattern_type, pattern_name))
            row = cursor.fetchone()
            if row:
                return {
                    'pattern_type': row[0],
                    'pattern_name': row[1],
                    'ssml_pattern': row[2],
                    'description': row[3]
                }
            return None

    def get_slang_term(self, term: str) -> Optional[Dict]:
        """Get a specific slang term with its SSML pattern"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT term, meaning, usage_example, ssml_pattern_type, category, region
                FROM slang_terms
                WHERE term = ?
            ''', (term,))
            row = cursor.fetchone()
            if row:
                return {
                    'term': row[0],
                    'meaning': row[1],
                    'usage_example': row[2],
                    'ssml_pattern_type': row[3],
                    'category': row[4],
                    'region': row[5]
                }
            return None

    def get_scene(self, scene_name: str) -> Optional[Dict]:
        """Get a specific scene template"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT scene_name, scene_type, ssml_content, description
                FROM scenes
                WHERE scene_name = ?
            ''', (scene_name,))
            row = cursor.fetchone()
            if row:
                return {
                    'scene_name': row[0],
                    'scene_type': row[1],
                    'ssml_content': row[2],
                    'description': row[3]
                }
            return None

    def get_slang_by_category(self, category: str) -> List[Dict]:
        """Get all slang terms in a specific category"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT term, meaning, usage_example, ssml_pattern_type, category, region
                FROM slang_terms
                WHERE category = ?
            ''', (category,))
            return [{
                'term': row[0],
                'meaning': row[1],
                'usage_example': row[2],
                'ssml_pattern_type': row[3],
                'category': row[4],
                'region': row[5]
            } for row in cursor.fetchall()]

    def get_patterns_by_type(self, pattern_type: str) -> List[Dict]:
        """Get all SSML patterns of a specific type"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pattern_type, pattern_name, ssml_pattern, description
                FROM ssml_patterns
                WHERE pattern_type = ?
            ''', (pattern_type,))
            return [{
                'pattern_type': row[0],
                'pattern_name': row[1],
                'ssml_pattern': row[2],
                'description': row[3]
            } for row in cursor.fetchall()]

    def build_ssml(self, text: str, pattern_type: str, pattern_name: str) -> Optional[str]:
        """Build SSML markup for a given text using a specific pattern"""
        patterns = self.get_patterns_by_type(pattern_type)
        if patterns:
            pattern = next((p for p in patterns if p.get('pattern_name') == pattern_name), patterns[0])
            return pattern['ssml_pattern'].replace('TEXT', text)
        return None

    def build_slang_ssml(self, term: str) -> Optional[str]:
        """Build SSML markup for a slang term"""
        slang = self.get_slang_term(term)
        if not slang:
            return None

        # Map slang pattern type to SSML pattern
        pattern_map = {
            'emphasis': {'type': 'prosody', 'name': 'emphasis'},
            'casual': {'type': 'prosody', 'name': 'soft'},
            'excited': {'type': 'emotion', 'name': 'excited'}
        }

        pattern_info = pattern_map.get(slang['ssml_pattern_type'])
        if not pattern_info:
            return None

        pattern = self.get_ssml_pattern(pattern_info['type'], pattern_info['name'])
        if pattern:
            return pattern['ssml_pattern'].replace('TEXT', term)
        return None

    def get_all_categories(self) -> List[str]:
        """Get all unique slang categories"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT category FROM slang_terms')
            return [row[0] for row in cursor.fetchall()]

    def get_all_regions(self) -> List[str]:
        """Get all unique regions"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT region FROM slang_terms WHERE region IS NOT NULL')
            return [row[0] for row in cursor.fetchall()]

    def get_required_phrase(self, phrase_type: str, phrase_text: str = None) -> Union[Dict, List[Dict]]:
        """Get a specific required phrase or all phrases of a type"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if phrase_text:
                cursor.execute('''
                    SELECT phrase_type, phrase_text, ssml_pattern_type, ssml_pattern_name, context
                    FROM required_phrases
                    WHERE phrase_type = ? AND phrase_text = ?
                ''', (phrase_type, phrase_text))
                row = cursor.fetchone()
                if row:
                    return {
                        'phrase_type': row[0],
                        'phrase_text': row[1],
                        'ssml_pattern_type': row[2],
                        'ssml_pattern_name': row[3],
                        'context': row[4]
                    }
                return None
            else:
                cursor.execute('''
                    SELECT phrase_type, phrase_text, ssml_pattern_type, ssml_pattern_name, context
                    FROM required_phrases
                    WHERE phrase_type = ?
                ''', (phrase_type,))
                return [{
                    'phrase_type': row[0],
                    'phrase_text': row[1],
                    'ssml_pattern_type': row[2],
                    'ssml_pattern_name': row[3],
                    'context': row[4]
                } for row in cursor.fetchall()]

    def get_scene_template(self, template_name: str) -> Optional[Dict]:
        """Get a specific scene template"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_name, template_type, base_emotion, structure, 
                       required_elements, optional_elements
                FROM scene_templates
                WHERE template_name = ?
            ''', (template_name,))
            row = cursor.fetchone()
            if row:
                return {
                    'template_name': row[0],
                    'template_type': row[1],
                    'base_emotion': row[2],
                    'structure': row[3],
                    'required_elements': row[4].split(','),
                    'optional_elements': row[5].split(',') if row[5] else []
                }
            return None

    def get_character_trait(self, trait_type: str = None) -> Union[Dict, List[Dict]]:
        """Get character traits by type or all traits"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if trait_type:
                cursor.execute('''
                    SELECT trait_type, trait_value, ssml_impact, description
                    FROM character_traits
                    WHERE trait_type = ?
                ''', (trait_type,))
            else:
                cursor.execute('''
                    SELECT trait_type, trait_value, ssml_impact, description
                    FROM character_traits
                ''')
            return [{
                'trait_type': row[0],
                'trait_value': row[1],
                'ssml_impact': row[2],
                'description': row[3]
            } for row in cursor.fetchall()]

    def build_scene(self, template_name: str, content: Dict) -> Optional[str]:
        """Build a complete scene using a template and content"""
        template = self.get_scene_template(template_name)
        if not template:
            return None

        # Get base emotion SSML
        base_emotion = self.get_ssml_pattern('emotion', template['base_emotion'])
        
        # Process required elements
        elements = {}
        for element in template['required_elements']:
            if element == 'greeting':
                greeting = self.get_required_phrase('greeting')[0]
                elements['greeting'] = self.build_ssml(
                    greeting['phrase_text'],
                    greeting['ssml_pattern_type'],
                    greeting['ssml_pattern_name']
                )
            elif element == 'closing':
                closing = self.get_required_phrase('closing')[0]
                elements['closing'] = self.build_ssml(
                    closing['phrase_text'],
                    closing['ssml_pattern_type'],
                    closing['ssml_pattern_name']
                )
            else:
                elements[element] = content.get(element, '')

        # Build scene
        scene = template['structure']
        for key, value in elements.items():
            scene = scene.replace(f'[{key.upper()}]', value)

        return f"<speak>{scene}</speak>"

    def build_character_ssml(self, text: str, emotion: str = None) -> str:
        """Build SSML with character trait modifications"""
        traits = self.get_character_trait('voice')
        base_ssml = text

        # Apply voice traits
        for trait in traits:
            if trait['ssml_impact'] and trait['ssml_impact'] != 'none':
                impact_type, impact_value = trait['ssml_impact'].split(':')
                param_name, param_value = impact_value.split('=')
                base_ssml = f"<prosody {param_name}='{param_value}'>{base_ssml}</prosody>"

        # Apply emotion if specified
        if emotion:
            emotion_pattern = self.get_ssml_pattern('emotion', emotion)
            if emotion_pattern:
                base_ssml = emotion_pattern['ssml_pattern'].replace('TEXT', base_ssml)

        return base_ssml

    def get_recent_memories(self, category: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent memories by category"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM memory_updates
                WHERE category = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (category, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_successful_patterns(self, pattern_type: str, min_success_rate: float = 0.7) -> List[Dict[str, Any]]:
        """Get patterns with success rate above threshold"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM interaction_patterns
                WHERE pattern_type = ? AND success_rating >= ?
                ORDER BY success_rating DESC, last_used DESC
            ''', (pattern_type, min_success_rate))
            return [dict(row) for row in cursor.fetchall()]

    def update_story_stats(self, story_id: int, times_told: int, success_rating: Optional[float] = None) -> bool:
        """Update story usage statistics"""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                if success_rating is not None:
                    cursor.execute('''
                        UPDATE stories
                        SET times_told = ?,
                            success_rating = ?,
                            last_told = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (times_told, success_rating, story_id))
                else:
                    cursor.execute('''
                        UPDATE stories
                        SET times_told = ?,
                            last_told = CURRENT_TIMESTAMP
                        WHERE id = ?
                    ''', (times_told, story_id))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f"Error updating story stats: {e}")
                return False

    def update_relationship_interaction(self, person_name: str, interaction_type: str, success_rating: float, notes: Optional[str] = None) -> bool:
        """Update relationship interaction history"""
        with self._get_connection() as conn:
            try:
                cursor = conn.cursor()
                # Get current history
                cursor.execute('''
                    SELECT interaction_history
                    FROM relationships
                    WHERE person_name = ?
                ''', (person_name,))
                row = cursor.fetchone()
                if not row:
                    return False

                # Update history
                history = json.loads(row[0] or '[]')
                history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': interaction_type,
                    'success_rating': success_rating,
                    'notes': notes
                })

                # Save updated history
                cursor.execute('''
                    UPDATE relationships
                    SET interaction_history = ?,
                        last_interaction = CURRENT_TIMESTAMP
                    WHERE person_name = ?
                ''', (json.dumps(history), person_name))
                conn.commit()
                return True
            except Exception as e:
                logger.error(f"Error updating relationship: {e}")
                return False

    def get_favorite_stories(self, min_success_rate: float = 0.8, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most successful stories"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM stories
                WHERE success_rating >= ?
                ORDER BY success_rating DESC, times_told DESC
                LIMIT ?
            ''', (min_success_rate, limit))
            return [dict(row) for row in cursor.fetchall()]

    def get_interaction_history(self, person_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent interactions with a person"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT interaction_history
                FROM relationships
                WHERE person_name = ?
            ''', (person_name,))
            row = cursor.fetchone()
            if not row or not row[0]:
                return []
            history = json.loads(row[0])
            return sorted(history, key=lambda x: x['timestamp'], reverse=True)[:limit]

    def get_pattern_stats(self, min_success_rate: float = 0.0) -> Dict[str, Any]:
        """Get pattern usage statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    pattern_type,
                    COUNT(*) as total_patterns,
                    AVG(success_rating) as avg_success_rate,
                    COUNT(CASE WHEN success_rating >= ? THEN 1 END) as successful_patterns
                FROM interaction_patterns
                GROUP BY pattern_type
            ''', (min_success_rate,))
            return {row['pattern_type']: {
                'total': row['total_patterns'],
                'average_success': row['avg_success_rate'],
                'successful_count': row['successful_patterns']
            } for row in cursor.fetchall()}

    def track_pattern_response(self, pattern_id: int, response_type: str) -> bool:
        """Track response to a pattern and update success rating
        response_type can be 'positive', 'negative', or 'neutral'"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # Get current metadata
            cursor.execute('SELECT metadata FROM interaction_patterns WHERE id = ?', (pattern_id,))
            row = cursor.fetchone()
            if not row:
                return False
                
            metadata = json.loads(row[0] or '{"responses": {"positive": 0, "negative": 0, "neutral": 0}}')
            
            # Update response count
            metadata['responses'][response_type] = metadata['responses'].get(response_type, 0) + 1
            
            # Calculate new success rating
            total_responses = sum(metadata['responses'].values())
            if total_responses > 0:
                success_rating = (metadata['responses']['positive'] * 1.0 + 
                                metadata['responses']['neutral'] * 0.5) / total_responses
            else:
                success_rating = 0.0
            
            # Update pattern
            cursor.execute('''
                UPDATE interaction_patterns
                SET metadata = ?,
                    success_rating = ?,
                    last_used = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (json.dumps(metadata), success_rating, pattern_id))
            
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error tracking pattern response: {e}")
            return False
        finally:
            conn.close()

# Example usage:
if __name__ == "__main__":
    db = UrsulaDB()
    
    # Get a pattern
    pattern = db.get_ssml_pattern('emotion', 'happy_high')
    print("Pattern:", json.dumps(pattern, indent=2))
    
    # Get a slang term
    slang = db.get_slang_term('wicked')
    print("\nSlang:", json.dumps(slang, indent=2))
    
    # Build SSML
    text = "Hello there!"
    ssml = db.build_ssml(text, 'emotion', 'happy_high')
    print("\nSSML:", ssml)
    
    # Build slang SSML
    slang_ssml = db.build_slang_ssml('wicked')
    print("\nSlang SSML:", slang_ssml)
    
    # Get all categories
    categories = db.get_all_categories()
    print("\nCategories:", categories)
    
    # Get all regions
    regions = db.get_all_regions()
    print("\nRegions:", regions)
    
    # Test required phrases
    print("Required Greetings:", json.dumps(db.get_required_phrase('greeting'), indent=2))
    
    # Test scene template
    print("\nScene Template:", json.dumps(db.get_scene_template('task_update'), indent=2))
    
    # Test character traits
    print("\nCharacter Traits:", json.dumps(db.get_character_trait('voice'), indent=2))
    
    # Test scene building
    content = {
        'tasks': 'Complete the report',
        'personal_update': 'Had a great date last night'
    }
    print("\nBuilt Scene:", db.build_scene('task_update', content))
    
    # Test character SSML
    print("\nCharacter SSML:", db.build_character_ssml("Hey sugar!", "happy_high")) 