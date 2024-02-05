from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import cv2
import base64
from typing import List
import get_ip


app = FastAPI(debug=True)

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




class videoManager:


    def __init__(self):

        #self.video_capture = cv2.VideoCapture("http://192.168.0.150:4747/video")
        self.video_capture = cv2.VideoCapture(0)
    

    def generate_frames(self):

        while True:

            success, frame = self.video_capture.read()

            if not success:
                break
            
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = base64.b64encode(buffer.tobytes())
            frame_str = frame_bytes.decode('utf-8')
            yield frame_str
        


manager = ConnectionManager()
vManager = videoManager()



@app.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)


    try:

        for frame in vManager.generate_frames():

            for client in manager.active_connections:

                try:
                    await client.send_text(frame)
                
                except Exception:

                    manager.disconnect(client)
    
    finally:

        manager.disconnect(websocket)



   
#uvicorn app:app --host 0.0.0.0 --port 8000 --reload