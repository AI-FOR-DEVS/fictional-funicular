from fastapi import FastAPI
from app import chat

app = FastAPI()

history_of_all_conversations = []


@app.get("/")
def read_root():
    return {"message": "hello world"}

@app.post("/chat")
def server_chat(query: str):
    return chat(query, history_of_all_conversations)



