from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app import chat
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

history_of_all_conversations = {}

def get_or_create_session(session_id: str = None):
    """Get or create a session. Returns (session_id, history)"""
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in history_of_all_conversations:
        history_of_all_conversations[session_id] = []

    return session_id, history_of_all_conversations[session_id]


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
def server_chat(query: str = Form(...), session_id: str = Form(None)):
    session_id, history = get_or_create_session(session_id)
    response_text = chat(query, history)
    
    # Return both the response and session_id so client can store it
    return JSONResponse({
        "response": response_text,
        "session_id": session_id
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
