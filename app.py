from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import base64
from typing import List
import get_ip
import asyncio
from multiprocessing import Process, Queue

app = FastAPI(debug=False)

print()
print(f"Video feed is available is at: http://{get_ip.get_ip_address()}:8000")
print()

templates = Jinja2Templates(directory="templates")


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_frame_message(self, message, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


class VideoProcess:

    def __init__(self, manager, frame_queue):
        self.manager = manager
        self.frame_queue = frame_queue
       

    def start(self):
        self.process = Process(target=self._capture_frames)
        self.process.start()

    def stop(self):
        self.process.terminate()

    def _capture_frames(self):
        video_capture = cv2.VideoCapture(0)
        #video_capture = cv2.VideoCapture("/home/knight/PixelSync/diabetes_information.mp4")
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = base64.b64encode(buffer.tobytes())
            frame_str = frame_bytes.decode('utf-8')
            self.frame_queue.put(frame_str)


manager = ConnectionManager()
frame_queue = Queue()
video_process = VideoProcess(manager, frame_queue)


async def send_frames():
    video_process.start()

    try:
        while True:
            frame = frame_queue.get()
            await manager.broadcast(frame)
            await asyncio.sleep(0.01)
    
    except asyncio.CancelledError:
        video_process.stop()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_frames())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
