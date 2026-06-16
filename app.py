import os
import uuid
import redis
from fastapi import FastAPI, UploadFile, File
from rq import Queue

app = FastAPI(title="QuantumDub-Supreme-2026")
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)
q = Queue('dubbing', connection=r)

@app.post("/dub")
async def start_dubbing(file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    file_path = f"in_{task_id}.wav"
    with open(file_path, "wb") as f: f.write(await file.read())
    
    # إرسال المهمة للـ worker
    q.enqueue('worker.process_video', task_id, file_path)
    return {"status": "processing", "task_id": task_id}