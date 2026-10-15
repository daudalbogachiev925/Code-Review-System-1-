from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
from src.analyzer import analyze_directory
from src.metrics import analyze_project, summary
from src.report import to_markdown
import shutil
import tempfile
import os

app = FastAPI(title="1C Code Review API")

class ReviewRequest(BaseModel):
    path: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/analyze")
def analyze(req: ReviewRequest):
    if not os.path.isdir(req.path):
        return {"error": "path not found"}
    issues = analyze_directory(req.path)
    metrics = analyze_project(req.path)
    return {
        "summary": summary(metrics),
        "issues": [i.__dict__ for i in issues],
    }

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    tmp = tempfile.mkdtemp()
    for f in files:
        dest = os.path.join(tmp, f.filename)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as out:
            out.write(await f.read())
    issues = analyze_directory(tmp)
    metrics = analyze_project(tmp)
    shutil.rmtree(tmp)
    return {"summary": summary(metrics),
            "issues": [i.__dict__ for i in issues]}
