from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Union, Any
import uvicorn
from ursula_db_api import UrsulaDB
from datetime import datetime
import json
import databases
import sqlalchemy
from sqlalchemy import create_engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Database setup
DATABASE_URL = "sqlite:///./ursula.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Create tables
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

app = FastAPI(
    title="Ursula API",
    description="API for Ursula's voice, memory, and personality",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

db = UrsulaDB()

# Request Models
class SSMLRequest(BaseModel):
    text: str
    pattern_type: str
    pattern_name: str

class SlangRequest(BaseModel):
    term: str

class SceneRequest(BaseModel):
    template_name: str
    content: Dict[str, str]

class MemoryRequest(BaseModel):
    category: str
    content: Dict[str, Any]
    context: str

# Additional Request Models
class PatternUpdateRequest(BaseModel):
    pattern_id: int
    success_rating: float

class StoryUpdateRequest(BaseModel):
    story_id: int
    times_told: int
    success_rating: Optional[float] = None

class RelationshipUpdateRequest(BaseModel):
    person_name: str
    interaction_type: str
    success_rating: float
    notes: Optional[str] = None

class PatternResponseRequest(BaseModel):
    pattern_id: int
    response_type: str

# API Routes
@app.get("/api/ursula/memory/relationships/{person_name}")
async def get_relationship(person_name: str):
    """Get relationship data for a person"""
    relationship = db.get_relationship(person_name)
    if not relationship:
        raise HTTPException(status_code=404, detail=f"No relationship found with: {person_name}")
    return relationship

@app.get("/api/ursula/memory/stories/{category}")
async def get_stories(category: str, mood: Optional[str] = None):
    """Get stories by category and optional mood"""
    stories = db.get_stories(category, mood)
    if not stories:
        raise HTTPException(status_code=404, detail=f"No stories found for category: {category}")
    return stories

@app.get("/api/ursula/patterns/{pattern_type}")
async def get_patterns(pattern_type: str):
    """Get voice patterns by type"""
    patterns = db.get_patterns_by_type(pattern_type)
    if not patterns:
        raise HTTPException(status_code=404, detail=f"No patterns found for type: {pattern_type}")
    return patterns

@app.post("/api/ursula/memory/store")
async def store_memory(request: MemoryRequest):
    """Store a new memory"""
    success = db.store_memory(request.category, request.content, request.context)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to store memory")
    return {"status": "success"}

@app.post("/api/ursula/ssml/build")
async def build_ssml(request: SSMLRequest):
    """Build SSML markup for text"""
    try:
        logger.info(f"Building SSML for request: {request}")
        result = db.build_ssml(request.text, request.pattern_type, request.pattern_name)
        if not result:
            logger.warning("Could not build SSML")
            raise HTTPException(status_code=404, detail="Could not build SSML with given parameters")
        logger.info(f"Built SSML: {result}")
        return result  # Already in correct format {"ssml": "..."}
    except Exception as e:
        logger.error(f"Error building SSML: {e}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ursula/slang/build")
async def build_slang_ssml(request: SlangRequest):
    """Build SSML markup for slang term"""
    ssml = db.build_slang_ssml(request.term)
    if not ssml:
        raise HTTPException(status_code=404, detail=f"Could not build SSML for slang term: {request.term}")
    return {"ssml": ssml}

@app.post("/api/ursula/scene/build")
async def build_scene(request: SceneRequest):
    """Build a complete scene"""
    scene = db.build_scene(request.template_name, request.content)
    if not scene:
        raise HTTPException(status_code=404, detail=f"Could not build scene with template: {request.template_name}")
    return {"ssml": scene}

@app.get("/api/ursula/character/traits")
@app.get("/api/ursula/character/traits/{trait_type}")
async def get_character_traits(trait_type: Optional[str] = None):
    """Get character traits"""
    try:
        logger.info(f"Getting character traits. trait_type={trait_type}")
        traits = db.get_character_trait(trait_type)
        logger.info(f"Retrieved traits: {traits}")
        if not traits:
            if trait_type:
                logger.warning(f"No traits found for type: {trait_type}")
                raise HTTPException(status_code=404, detail=f"No traits found for type: {trait_type}")
            else:
                logger.warning("No core identity found")
                raise HTTPException(status_code=404, detail="No core identity found")
        return traits
    except Exception as e:
        logger.error(f"Error getting character traits: {str(e)}")
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ursula/phrases/{phrase_type}")
async def get_required_phrases(phrase_type: str):
    """Get required phrases of a specific type"""
    phrases = db.get_required_phrase(phrase_type)
    if not phrases:
        raise HTTPException(status_code=404, detail=f"No phrases found for type: {phrase_type}")
    return phrases

# Additional API Routes
@app.get("/api/ursula/memory/recent/{category}")
async def get_recent_memories(category: str, limit: int = 5):
    """Get recent memories by category"""
    memories = db.get_recent_memories(category, limit)
    if not memories:
        raise HTTPException(status_code=404, detail=f"No recent memories found for category: {category}")
    return memories

@app.get("/api/ursula/patterns/successful/{pattern_type}")
async def get_successful_patterns(pattern_type: str, min_success_rate: float = 0.7):
    """Get patterns with success rate above threshold"""
    patterns = db.get_successful_patterns(pattern_type, min_success_rate)
    if not patterns:
        raise HTTPException(status_code=404, detail=f"No successful patterns found for type: {pattern_type}")
    return patterns

@app.post("/api/ursula/patterns/update")
async def update_pattern_success(request: PatternUpdateRequest):
    """Update pattern success rating"""
    success = db.update_pattern_success(request.pattern_id, request.success_rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update pattern")
    return {"status": "success"}

@app.post("/api/ursula/stories/update")
async def update_story_stats(request: StoryUpdateRequest):
    """Update story usage statistics"""
    success = db.update_story_stats(request.story_id, request.times_told, request.success_rating)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update story stats")
    return {"status": "success"}

@app.post("/api/ursula/relationships/update")
async def update_relationship(request: RelationshipUpdateRequest):
    """Update relationship interaction history"""
    success = db.update_relationship_interaction(
        request.person_name,
        request.interaction_type,
        request.success_rating,
        request.notes
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to update relationship")
    return {"status": "success"}

@app.get("/api/ursula/stories/favorite")
async def get_favorite_stories(min_success_rate: float = 0.8, limit: int = 5):
    """Get most successful stories"""
    stories = db.get_favorite_stories(min_success_rate, limit)
    if not stories:
        raise HTTPException(status_code=404, detail="No favorite stories found")
    return stories

@app.get("/api/ursula/memory/interactions/{person_name}")
async def get_interaction_history(person_name: str, limit: int = 10):
    """Get recent interactions with a person"""
    history = db.get_interaction_history(person_name, limit)
    if not history:
        raise HTTPException(status_code=404, detail=f"No interaction history found for: {person_name}")
    return history

@app.get("/api/ursula/stats/patterns")
async def get_pattern_stats(min_success_rate: float = 0.0):
    """Get pattern usage statistics"""
    stats = db.get_pattern_stats(min_success_rate)
    if not stats:
        raise HTTPException(status_code=404, detail="No pattern statistics found")
    return stats

@app.post("/api/ursula/patterns/response")
async def track_pattern_response(request: PatternResponseRequest):
    """Track response to a pattern"""
    if request.response_type not in ['positive', 'negative', 'neutral']:
        raise HTTPException(status_code=400, detail="Invalid response type")
    success = db.track_pattern_response(request.pattern_id, request.response_type)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to track pattern response")
    return {"status": "success"}

@app.get("/api/ursula/templates/{template_type}")
async def get_response_templates(template_type: str):
    """Get response templates by type"""
    templates = db.get_response_templates(template_type)
    if not templates:
        raise HTTPException(status_code=404, detail=f"No templates found for type: {template_type}")
    return templates

@app.get("/api/ursula/templates/{template_type}/{template_name}")
async def get_specific_template(template_type: str, template_name: str):
    """Get a specific response template"""
    template = db.get_specific_template(template_type, template_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Template not found: {template_type}/{template_name}")
    return template

@app.get("/api/ursula/voicemail/templates/{template_name}")
async def get_voicemail_template(template_name: str):
    """Get a specific voicemail template"""
    template = db.get_voicemail_template(template_name)
    if not template:
        raise HTTPException(status_code=404, detail=f"Voicemail template not found: {template_name}")
    return template

@app.get("/api/ursula/voicemail/templates")
async def get_all_voicemail_templates():
    """Get all voicemail templates"""
    templates = db.get_all_voicemail_templates()
    if not templates:
        raise HTTPException(status_code=404, detail="No voicemail templates found")
    return templates

if __name__ == "__main__":
    uvicorn.run("ursula_api:app", host="0.0.0.0", port=8080, reload=True) 
@app.get("/api/ursula/memory/romance/{name}")
async def get_romantic_history(name: str):
    """Get romantic relationship history"""
    romance = db.get_romantic_relationship(name)
    if not romance:
        raise HTTPException(status_code=404, detail=f"No romantic history found with: {name}")
    return romance

@app.get("/api/ursula/memory/romance/stories/{category}")
async def get_romantic_stories(category: str):
    """Get romantic stories by category"""
    stories = db.get_romantic_stories(category)
    if not stories:
        raise HTTPException(status_code=404, detail=f"No romantic stories found for category: {category}")
    return stories
