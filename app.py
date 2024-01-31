from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import base64

app = FastAPI()

templates = Jinja2Templates(directory="templates")

video_capture = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = base64.b64encode(buffer.tobytes())
        frame_str = frame_bytes.decode('utf-8')
        yield frame_str

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    for frame in generate_frames():
        await websocket.send_text(frame)

@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
