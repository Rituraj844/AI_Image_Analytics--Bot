from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from vision_engine import analyze_image
from gtts import gTTS
import os

app = FastAPI()

# ফাইল সেভ করার জন্য ফোল্ডার
if not os.path.exists("uploads"): os.makedirs("uploads")
if not os.path.exists("static"): os.makedirs("static")

@app.post("/analyze")
async def analyze(file: UploadFile = File(...), query: str = Form("ছবিটি বর্ণনা করো")):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # এআই বিশ্লেষণ
    description = analyze_image(file_path, query)
    
    # ভয়েস তৈরি (বাংলা)
    tts = gTTS(description, lang='bn')
    audio_path = f"static/output.mp3"
    tts.save(audio_path)
    
    return {"description": description, "audio_url": "/static/output.mp3"}

@app.get("/")
def index():
    return FileResponse("index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)