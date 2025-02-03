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
            logger.info(f"Connecting to database: {self.db_path}")
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [t[0] for t in tables]
            logger.info(f"Available tables: {table_names}")
            
            # Check if required tables exist
            required_tables = ['ssml_patterns', 'interaction_patterns', 'core_identity']
            missing_tables = [t for t in required_tables if t not in table_names]
            if missing_tables:
                logger.error(f"Missing required tables: {missing_tables}")
                raise Exception(f"Missing required tables: {missing_tables}")
            
            return conn
        except Exception as e:
            logger.error(f"Database connection error: {e}")
            logger.exception(e)
            raise

    def get_patterns_by_type(self, pattern_type: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT pattern_type, pattern, context, success_rating, metadata
                FROM interaction_patterns 
                WHERE LOWER(pattern_type) = LOWER(?) AND success_rating > 0.7
                ORDER BY last_used DESC
            ''', (pattern_type,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting patterns: {e}")
            return []
        finally:
            conn.close()

    def get_relationship(self, person: str) -> Optional[Dict[str, Any]]:
        """Get relationship data for a person"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM relationships WHERE LOWER(person_name) = LOWER(?)",
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
        """Get stories by category and optional mood"""
        category = self.resolve_category_alias(category, 'stories')
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM stories WHERE LOWER(category) = LOWER(?)"
            params = [category]
            if mood:
                query += " AND LOWER(mood) = LOWER(?)"
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
                logger.info(f"Looking for trait type: {trait_type}")
                cursor.execute(
                    """SELECT trait_type, trait_value, ssml_impact, description
                       FROM character_traits WHERE trait_type = ?""",
                    (trait_type,)
                )
                row = cursor.fetchone()
                if row:
                    logger.info(f"Found trait: {dict(row)}")
                    return dict(row)
                logger.info("No specific trait found, falling back to core identity")
            
            # If no specific trait type or no result found, return core identity
            logger.info("Querying core identity")
            cursor.execute("SELECT * FROM core_identity LIMIT 1")
            row = cursor.fetchone()
            if row:
                logger.info("Found core identity")
                result = dict(row)
                # Parse base_personality JSON if it exists
                if result.get('base_personality'):
                    logger.info("Parsing base_personality JSON")
                    result['base_personality'] = json.loads(result['base_personality'])
                return result
            logger.warning("No core identity found")
            return {}
        except Exception as e:
            logger.error(f"Error getting character traits: {e}")
            logger.exception(e)
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
        try:
            logger.info(f"Looking for SSML pattern: type={pattern_type}, name={pattern_name}")
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT pattern_type, pattern_name, ssml_pattern, description
                    FROM ssml_patterns
                    WHERE pattern_type = ? AND pattern_name = ?
                ''', (pattern_type, pattern_name))
                row = cursor.fetchone()
                if row:
                    logger.info(f"Found pattern: {dict(row)}")
                    return {
                        'pattern_type': row[0],
                        'pattern_name': row[1],
                        'ssml_pattern': row[2],
                        'description': row[3]
                    }
                logger.warning(f"No pattern found for type={pattern_type}, name={pattern_name}")
                return None
        except Exception as e:
            logger.error(f"Error getting SSML pattern: {e}")
            logger.exception(e)
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
        """Build SSML markup for text using a specific pattern"""
        try:
            logger.info(f"Building SSML for text='{text}', type='{pattern_type}', name='{pattern_name}'")
            pattern = self.get_ssml_pattern(pattern_type, pattern_name)
            if not pattern:
                logger.warning("No pattern found")
                return None
            
            # Replace $TEXT placeholder with actual text
            logger.info(f"Using pattern: {pattern}")
            ssml = pattern['ssml_pattern'].replace('$TEXT', text)
            logger.info(f"Generated SSML: {ssml}")
            return {"ssml": ssml}  # Return as dictionary to match API response format
        except Exception as e:
            logger.error(f"Error building SSML: {e}")
            logger.exception(e)
            return None

    def build_slang_ssml(self, term: str) -> Optional[str]:
        """Build SSML markup for a slang term"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT term, ssml_pattern_type
                FROM slang_terms
                WHERE term = ?
            ''', (term,))
            row = cursor.fetchone()
            if not row:
                return None
            
            # Get the appropriate SSML pattern
            pattern = self.get_ssml_pattern('slang', row['ssml_pattern_type'])
            if not pattern:
                return None
            
            # Replace $TEXT placeholder with the term
            ssml = pattern['ssml_pattern'].replace('$TEXT', term)
            return ssml
        except Exception as e:
            logger.error(f"Error building slang SSML: {e}")
            return None
        finally:
            conn.close()

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

    def build_character_ssml(self, text: str, emotion: str) -> Optional[str]:
        """Build character-specific SSML markup"""
        try:
            # Get character's base voice pattern
            core = self.get_character_trait()
            if not core:
                return None
            
            # Get emotion pattern
            pattern = self.get_ssml_pattern('emotion', emotion)
            if not pattern:
                return None
            
            # Combine character voice with emotion
            ssml = pattern['ssml_pattern'].replace('$TEXT', text)
            return ssml
        except Exception as e:
            logger.error(f"Error building character SSML: {e}")
            return None

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
        try:
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
        except Exception as e:
            logger.error(f"Error getting pattern stats: {e}")
            logger.exception(e)
            return {}

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

    def get_response_templates(self, template_type: str) -> List[Dict[str, Any]]:
        """Get all response templates of a specific type"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_type, template_name, ssml_pattern, description
                FROM response_templates
                WHERE template_type = ?
            ''', (template_type,))
            return [{
                'template_type': row[0],
                'template_name': row[1],
                'ssml_pattern': row[2],
                'description': row[3]
            } for row in cursor.fetchall()]

    def get_specific_template(self, template_type: str, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific response template"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_type, template_name, ssml_pattern, description
                FROM response_templates
                WHERE template_type = ? AND template_name = ?
            ''', (template_type, template_name))
            row = cursor.fetchone()
            if row:
                return {
                    'template_type': row[0],
                    'template_name': row[1],
                    'ssml_pattern': row[2],
                    'description': row[3]
                }
            return None

    def get_voicemail_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific voicemail template"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_type, template_name, ssml_content, description
                FROM voicemail_templates
                WHERE template_name = ?
            ''', (template_name,))
            row = cursor.fetchone()
            if row:
                return {
                    'template_type': row[0],
                    'template_name': row[1],
                    'ssml_content': row[2],
                    'description': row[3]
                }
            return None

    def get_all_voicemail_templates(self) -> List[Dict[str, Any]]:
        """Get all voicemail templates"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT template_type, template_name, ssml_content, description
                FROM voicemail_templates
            ''')
            return [{
                'template_type': row[0],
                'template_name': row[1],
                'ssml_content': row[2],
                'description': row[3]
            } for row in cursor.fetchall()]

    def get_romantic_relationship(self, name: str) -> Optional[Dict[str, Any]]:
        """Get romantic relationship data"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM romantic_relationships WHERE LOWER(name) = LOWER(?)",
                (name,)
            )
            row = cursor.fetchone()
            if row:
                result = dict(row)
                if result.get('interaction_history'):
                    result['interaction_history'] = json.loads(result['interaction_history'])
                if result.get('locations'):
                    result['locations'] = json.loads(result['locations'])
                return result
            return None
        except Exception as e:
            logger.error(f"Error getting romantic relationship: {e}")
            return None
        finally:
            conn.close()

    def get_romantic_stories(self, category: str) -> List[Dict[str, Any]]:
        """Get romantic stories by category"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM romantic_stories WHERE LOWER(category) = LOWER(?)",
                (category,)
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                story = dict(row)
                if story.get('characters'):
                    story['characters'] = json.loads(story['characters'])
                results.append(story)
            return results
        except Exception as e:
            logger.error(f"Error getting romantic stories: {e}")
            return []
        finally:
            conn.close()

    def get_task_locations(self, category: str) -> List[Dict[str, Any]]:
        """Get task locations by category"""
        category = self.resolve_category_alias(category, 'task_locations')
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM task_locations WHERE LOWER(category) = LOWER(?)",
                (category,)
            )
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error getting task locations: {e}")
            return []
        finally:
            conn.close()

    def get_task_priorities(self, level: str) -> Optional[Dict[str, Any]]:
        """Get task priority by level"""
        level = self.resolve_category_alias(level, 'task_priorities')
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM task_priorities WHERE LOWER(level) = LOWER(?)",
                (level,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error getting task priority: {e}")
            return None
        finally:
            conn.close()

    def resolve_category_alias(self, alias: str, table_name: str) -> str:
        """Resolve a category alias to its canonical form"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT canonical_category FROM category_aliases 
                   WHERE LOWER(alias) = LOWER(?) AND table_name = ?""",
                (alias, table_name)
            )
            row = cursor.fetchone()
            return row['canonical_category'] if row else alias
        except Exception as e:
            logger.error(f"Error resolving category alias: {e}")
            return alias
        finally:
            conn.close()

    def get_routines(self, routine_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get daily routines by type.
        
        Args:
            routine_type (str): Type of routine (e.g., morning_ritual, power_moves)
            
        Returns:
            List of routines with time, activity, location, quirks, frequency, importance_rating
            or None if no routines found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT time, activity, location, quirks, frequency, importance_rating 
            FROM daily_routines 
            WHERE LOWER(routine_type) = LOWER(?)
            ORDER BY time
        ''', (routine_type,))
        routines = cursor.fetchall()
        if not routines:
            return None
        return [{"time": r[0], "activity": r[1], "location": r[2], 
                 "quirks": json.loads(r[3]), "frequency": r[4], 
                 "importance_rating": r[5]} for r in routines]

    def get_rules(self, context: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get personal rules by context.
        
        Args:
            context (str): Rule context (e.g., gambling, business, power)
            
        Returns:
            List of rules with rule text, origin story, importance rating
            or None if no rules found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT rule, origin_story, importance_rating 
            FROM personal_rules 
            WHERE LOWER(context) LIKE '%' || LOWER(?) || '%'
            ORDER BY importance_rating DESC
        ''', (context,))
        rules = cursor.fetchall()
        if not rules:
            return None
        return [{"rule": r[0], "origin_story": r[1], 
                 "importance_rating": r[2]} for r in rules]

    def get_skills(self, proficiency: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get secret skills by proficiency level.
        
        Args:
            proficiency (str): Skill proficiency level (e.g., expert)
            
        Returns:
            List of skills with skill name, origin story, reveal frequency
            or None if no skills found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT skill, origin_story, reveal_frequency 
            FROM secret_skills 
            WHERE LOWER(proficiency_level) = LOWER(?)
            ORDER BY reveal_frequency
        ''', (proficiency,))
        skills = cursor.fetchall()
        if not skills:
            return None
        return [{"skill": s[0], "origin_story": s[1], 
                 "reveal_frequency": s[2]} for s in skills]

    def get_vulnerabilities(self) -> Optional[List[Dict[str, Any]]]:
        """
        Get all vulnerabilities.
        
        Returns:
            List of vulnerabilities with trigger, reaction, background, coping mechanism
            or None if no vulnerabilities found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT trigger, reaction, background, coping_mechanism 
            FROM vulnerabilities
            ORDER BY trigger
        ''')
        vulns = cursor.fetchall()
        if not vulns:
            return None
        return [{"trigger": v[0], "reaction": v[1], 
                 "background": v[2], "coping_mechanism": v[3]} for v in vulns]

    def get_haunts(self, city: str, time_of_day: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get regular haunts by city and time of day.
        
        Args:
            city (str): City name (e.g., boston, new york)
            time_of_day (str): Time of day (morning, afternoon, evening)
            
        Returns:
            List of locations with purpose, frequency, special notes
            or None if no haunts found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT location, purpose, frequency, special_notes 
            FROM regular_haunts 
            WHERE LOWER(city) = LOWER(?) AND LOWER(time_of_day) = LOWER(?)
            ORDER BY frequency DESC
        ''', (city, time_of_day))
        haunts = cursor.fetchall()
        if not haunts:
            return None
        return [{"location": h[0], "purpose": h[1], 
                 "frequency": h[2], "special_notes": h[3]} for h in haunts]

    def get_traits(self, city: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get regional traits by city.
        
        Args:
            city (str): City name (e.g., boston, new york)
            
        Returns:
            List of traits with context, manifestation, frequency
            or None if no traits found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT trait, context, manifestation, frequency 
            FROM regional_traits 
            WHERE LOWER(city) = LOWER(?)
            ORDER BY frequency DESC
        ''', (city,))
        traits = cursor.fetchall()
        if not traits:
            return None
        return [{"trait": t[0], "context": t[1], 
                 "manifestation": t[2], "frequency": t[3]} for t in traits]

    def get_dreams(self, dream_type: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get future dreams by type.
        
        Args:
            dream_type (str): Dream type (admitted, secret)
            
        Returns:
            List of dreams with progress status and related actions
            or None if no dreams found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT dream, progress_status, related_actions 
            FROM future_dreams 
            WHERE LOWER(type) = LOWER(?)
            ORDER BY progress_status
        ''', (dream_type,))
        dreams = cursor.fetchall()
        if not dreams:
            return None
        return [{"dream": d[0], "progress_status": d[1], 
                 "related_actions": json.loads(d[2])} for d in dreams]

    def get_pleasures(self, frequency: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get guilty pleasures by frequency.
        
        Args:
            frequency (str): Frequency of indulgence (weekly, monthly)
            
        Returns:
            List of pleasures with secrecy level
            or None if no pleasures found
        """
        cursor = self._get_connection().cursor()
        cursor.execute('''
            SELECT pleasure, secrecy_level 
            FROM guilty_pleasures 
            WHERE LOWER(frequency) = LOWER(?)
            ORDER BY secrecy_level DESC
        ''', (frequency,))
        pleasures = cursor.fetchall()
        if not pleasures:
            return None
        return [{"pleasure": p[0], "secrecy_level": p[1]} for p in pleasures]

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