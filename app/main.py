from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import uuid
from typing import Optional
from pydantic import BaseModel
import time
import threading
from PIL import Image, ImageDraw, ImageFont
import random

app = FastAPI(title="Luminous - AI Wallpaper Generator")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory job storage
jobs = {}

# Job status
JOB_STATUS = {
    "PENDING": "pending",
    "PROCESSING": "processing",
    "COMPLETED": "completed",
    "FAILED": "failed"
}

class WallpaperRequest(BaseModel):
    color: str
    style: str
    description: str
    resolution: str = "1920x1080"
    colorTemp: int = 6500

class JobResponse(BaseModel):
    jobId: str
    status: str
    previewUrl: Optional[str] = None
    message: Optional[str] = None

def generate_wallpaper_image(color: str, style: str, description: str, resolution: str = "1920x1080") -> str:
    """Generate actual wallpaper image based on parameters"""
    try:
        # Parse resolution
        width, height = map(int, resolution.split('x'))
        
        # Create base image
        img = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(img)
        
        # Generate pattern based on style
        if style == "gradient":
            # Create gradient effect
            base_color = Image.new('RGB', (1, 1), color=color)
            base_rgb = base_color.getpixel((0, 0))
            
            for y in range(height):
                factor = y / height
                r = int(base_rgb[0] * (1 - factor * 0.5))
                g = int(base_rgb[1] * (1 - factor * 0.5))
                b = int(base_rgb[2] * (1 - factor * 0.5))
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        elif style == "geometric":
            # Add geometric shapes
            for i in range(15):
                x = random.randint(0, width-80)
                y = random.randint(0, height-80)
                shape_color = (
                    random.randint(100, 255),
                    random.randint(100, 255),
                    random.randint(100, 255)
                )
                draw.rectangle([x, y, x+80, y+80], fill=shape_color)
        
        elif style == "abstract":
            # Add abstract patterns
            for i in range(30):
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = random.randint(0, width)
                y2 = random.randint(0, height)
                line_color = (
                    random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255)
                )
                draw.line([(x1, y1), (x2, y2)], fill=line_color, width=2)
        
        # Save to file
        filename = f"wallpaper_{uuid.uuid4().hex}.png"
        filepath = os.path.join("static", "previews", filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        img.save(filepath, "PNG")
        
        return f"/static/previews/{filename}"
        
    except Exception as e:
        print(f"Error generating wallpaper: {e}")
        return "/static/previews/default.png"

@app.get("/")
async def home(request: Request):
    """Main landing page with wallpaper generation form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_model=JobResponse)
async def generate_wallpaper(request: WallpaperRequest):
    """Generate wallpaper based on user input"""
    job_id = str(uuid.uuid4())
    
    # Store job in memory
    jobs[job_id] = {
        "status": JOB_STATUS["PENDING"],
        "request": request.dict(),
        "created_at": time.time()
    }
    
    def process_wallpaper():
        try:
            jobs[job_id]["status"] = JOB_STATUS["PROCESSING"]
            
            # Generate actual wallpaper
            preview_url = generate_wallpaper_image(
                request.color,
                request.style,
                request.description,
                request.resolution
            )
            
            jobs[job_id]["status"] = JOB_STATUS["COMPLETED"]
            jobs[job_id]["preview_url"] = preview_url
            
        except Exception as e:
            jobs[job_id]["status"] = JOB_STATUS["FAILED"]
            jobs[job_id]["message"] = str(e)
    
    threading.Thread(target=process_wallpaper).start()
    
    return JobResponse(
        jobId=job_id,
        status="success",
        message="Wallpaper generation started"
    )

@app.get("/preview/{job_id}", response_model=JobResponse)
async def preview_wallpaper(job_id: str):
    """Get preview of generated wallpaper"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] == JOB_STATUS["COMPLETED"]:
        return JobResponse(
            jobId=job_id,
            status="success",
            previewUrl=job.get("preview_url"),
            message="Preview available"
        )
    else:
        return JobResponse(
            jobId=job_id,
            status=job["status"],
            message="Wallpaper still processing"
        )

@app.get("/download/{job_id}")
async def download_wallpaper(job_id: str):
    """Download final wallpaper"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    if job["status"] != JOB_STATUS["COMPLETED"]:
        raise HTTPException(status_code=400, detail="Wallpaper not ready")
    
    preview_url = job.get("preview_url", "/static/previews/default.png")
    filename = preview_url.split("/")[-1]
    filepath = os.path.join("app", "static", "previews", filename)
    
    if not os.path.exists(filepath):
        filepath = "app/static/previews/default.png"
    
    return FileResponse(
        filepath,
        filename=f"luminous-wallpaper-{job_id}.png",
        media_type="image/png"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
