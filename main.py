from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import joblib
import json
import random

app = FastAPI()
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

# Load trained model
model = joblib.load("sentiment_model.joblib")

# Store active connections
connections = []

# AI responses based on sentiment
ai_responses = {
    "positive": [
        "That's wonderful to hear! 😊 Your positivity is contagious!",
        "I love your positive energy! ✨ Keep spreading those good vibes!",
        "That sounds amazing! 🎉 Your optimism brightens my day!",
        "What a delightful message! 😄 I'm feeling the joy too!",
        "Your happiness is infectious! 🌟 Thanks for sharing that!"
    ],
    "negative": [
        "I'm sorry you're feeling that way. 😔 Is there anything I can help with?",
        "That sounds tough. 💙 Remember, difficult times don't last forever.",
        "I hear you, and your feelings are valid. 🤗 Take care of yourself!",
        "I understand this is challenging. 💜 You're stronger than you know!",
        "That must be difficult. 🫂 I'm here if you need someone to listen."
    ],
    "neutral": [
        "I see what you mean. 🤔 Thanks for sharing your thoughts!",
        "That's an interesting perspective! 💭 I appreciate you sharing that.",
        "Got it! 👍 Thanks for letting me know.",
        "I understand. 😌 Is there anything else you'd like to discuss?",
        "Thanks for the update! 📝 How are you feeling about it?"
    ]
}

@app.get("/")
async def home():
    return HTMLResponse(open("index.html").read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            sentiment = model.predict([message])[0]
            
            # Send user message
            user_data = {
                "type": "user",
                "message": message,
                "timestamp": "now"
            }
            
            # Select AI response based on sentiment
            ai_message = random.choice(ai_responses.get(sentiment, ai_responses["neutral"]))
            ai_data = {
                "type": "ai",
                "message": ai_message,
                "sentiment": sentiment,
                "timestamp": "now"
            }
            
            # Send both messages to all connections
            for conn in connections:
                await conn.send_text(json.dumps(user_data))
                await conn.send_text(json.dumps(ai_data))
                
    except WebSocketDisconnect:
        connections.remove(websocket)
