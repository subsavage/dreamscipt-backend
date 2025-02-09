from fastapi import APIRouter, HTTPException, Form
from services.llm_service import generate_story

router = APIRouter()

# Store ongoing stories per user
story_data = {}

@router.post("/start-story")
async def start_story(user_id: str = Form(...)):
    """Starts a new AI-generated story."""
    try:
        first_prompt = "A mysterious door appears in front of you. As you step closer..."
        story_data[user_id] = first_prompt  # Store initial story
        output = generate_story(first_prompt)  # Use Gemini API
        story_data[user_id] += "\n" + output
        return {'story': output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/continue-story")
async def continue_story(user_id: str = Form(...)):
    """Continues the AI story."""
    try:
        if user_id not in story_data:
            raise HTTPException(status_code=400, detail="No story found. Start a new one.")

        output = generate_story(story_data[user_id])
        story_data[user_id] += "\n" + output
        return {'story': output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/user-writes")
async def user_writes(user_id: str = Form(...), user_input: str = Form(...)):
    """Takes user-written story continuation and lets AI continue."""
    try:
        if user_id not in story_data:
            raise HTTPException(status_code=400, detail="No story found. Start a new one.")

        story_data[user_id] += "\n" + user_input  # Append user input
        output = generate_story(story_data[user_id])
        story_data[user_id] += "\n" + output
        return {'story': output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/redo")
async def redo_story(user_id: str = Form(...)):
    """Regenerates the last AI-generated story part."""
    try:
        if user_id not in story_data:
            raise HTTPException(status_code=400, detail="No story found. Start a new one.")

        # Remove last AI part
        last_ai_output = story_data[user_id].rfind("\n")  # Find last generated AI text
        if last_ai_output != -1:
            story_data[user_id] = story_data[user_id][:last_ai_output]  # Trim story

        output = generate_story(story_data[user_id])
        story_data[user_id] += "\n" + output
        return {'story': output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
