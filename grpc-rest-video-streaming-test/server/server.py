from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import aiofiles
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI 인스턴스 생성 및 메타데이터 설정
app = FastAPI(
    title="Video Streaming Server",
    description="REST API server for video streaming with FastAPI",
    version="1.0.0",
    docs_url="/docs",   # Swagger UI endpoint
    redoc_url="/redoc"  # ReDoc endpoint
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 비디오 파일을 저장할 디렉토리
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", 
         response_model=Dict[str, str],
         summary="Root endpoint",
         description="Returns a welcome message to confirm the server is running")
async def read_root():
    """
    루트 엔드포인트: 서버 상태 확인용
    """
    return {"message": "Video Streaming Server"}

@app.post("/upload",
          response_model=Dict[str, str],
          summary="Upload a video file",
          description="Upload a video file to the server")
async def upload_video(file: UploadFile):
    """
    비디오 파일 업로드 엔드포인트

    - **file**: 업로드할 비디오 파일 (지원 형식: .mp4, .avi, .mkv)

    Returns:
        - **filename**: 업로드된 파일명
        - **status**: 업로드 상태
    """
    if not file.filename.endswith(('.mp4', '.avi', '.mkv')):
        raise HTTPException(
            status_code=400, 
            detail="Only .mp4, .avi, and .mkv files are supported"
        )

    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        logger.info(f"Successfully uploaded video: {file.filename}")
        return {"filename": file.filename, "status": "uploaded"}
    
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos",
         response_model=Dict[str, List[str]],
         summary="List all videos",
         description="Returns a list of all available video files on the server")
async def list_videos():
    """
    서버에 저장된 모든 비디오 파일 목록 조회

    Returns:
        - **videos**: 사용 가능한 비디오 파일 목록
    """
    try:
        videos = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(('.mp4', '.avi', '.mkv'))]
        return {"videos": videos}
    except Exception as e:
        logger.error(f"Error listing videos: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stream/{video_name}",
         response_class=StreamingResponse,
         summary="Stream a video",
         description="Stream a video file from the server")
async def stream_video(video_name: str):
    """
    비디오 스트리밍 엔드포인트

    - **video_name**: 스트리밍할 비디오 파일명

    Returns:
        - Video stream in chunks
    """
    video_path = os.path.join(UPLOAD_DIR, video_name)
    
    if not os.path.exists(video_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Video '{video_name}' not found"
        )
    
    try:
        return StreamingResponse(
            video_streamer(video_path),
            media_type="video/mp4"
        )
    except Exception as e:
        logger.error(f"Error streaming video: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def video_streamer(video_path: str):
    """비디오 파일을 청크 단위로 스트리밍하는 제너레이터 함수"""
    async with aiofiles.open(video_path, mode='rb') as file:
        while True:
            chunk = await file.read(8192)
            if not chunk:
                break
            yield chunk

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)