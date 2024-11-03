import requests
import os
import time
from typing import Optional
import logging
from urllib.parse import urljoin

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def wait_for_server(self, timeout: int = 30, interval: int = 1) -> bool:
        """서버가 준비될 때까지 대기"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = self.session.get(self.base_url)
                if response.status_code == 200:
                    logger.info("Server is ready!")
                    return True
            except requests.exceptions.RequestException:
                logger.info("Waiting for server to be ready...")
                time.sleep(interval)
        return False

    def upload_video(self, file_path: str) -> dict:
        """비디오 파일을 서버에 업로드합니다."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = self.session.post(
                    urljoin(self.base_url, "upload"),
                    files=files
                )
                response.raise_for_status()
                return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading video: {str(e)}")
            raise

    def list_videos(self) -> list:
        """서버에 있는 비디오 목록을 가져옵니다."""
        try:
            response = self.session.get(urljoin(self.base_url, "videos"))
            response.raise_for_status()
            return response.json()["videos"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing videos: {str(e)}")
            raise

    def download_video(self, video_name: str, save_path: Optional[str] = None) -> str:
        """서버로부터 비디오를 다운로드합니다."""
        if save_path is None:
            save_path = video_name

        try:
            response = self.session.get(
                urljoin(self.base_url, f"stream/{video_name}"),
                stream=True
            )
            response.raise_for_status()

            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            logger.info(f"Successfully downloaded video to {save_path}")
            return save_path
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading video: {str(e)}")
            raise

def main():
    # 환경 변수에서 서버 정보 가져오기
    server_host = os.getenv("SERVER_HOST", "localhost")
    server_port = os.getenv("SERVER_PORT", "8000")
    base_url = f"http://{server_host}:{server_port}"

    client = VideoClient(base_url)
    
    try:
        # 서버가 준비될 때까지 대기
        if not client.wait_for_server():
            logger.error("Server did not become ready in time")
            return

        # 테스트: 비디오 목록 가져오기
        videos = client.list_videos()
        logger.info(f"Available videos: {videos}")

        # 여기에 추가적인 테스트 코드를 작성할 수 있습니다.
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main() 