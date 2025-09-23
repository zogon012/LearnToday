import pytest
from httpx import AsyncClient
import json
from uuid import UUID


class TestFastAPIEndpoints:
    """FastAPI 엔드포인트 테스트"""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, async_client: AsyncClient):
        """루트 엔드포인트 테스트"""
        response = await async_client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "timestamp" in data

    @pytest.mark.asyncio
    async def test_health_check(self, async_client: AsyncClient):
        """헬스체크 엔드포인트 테스트"""
        response = await async_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["redis_connected"] is True
        assert "timestamp" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_create_push(self, async_client: AsyncClient):
        """푸시 생성 엔드포인트 테스트"""
        push_data = {
            "user_id": "test_user_123",
            "message": "테스트 푸시 메시지",
            "topic": "test_topic"
        }
        
        response = await async_client.post("/push", json=push_data)
        assert response.status_code == 200
        
        data = response.json()
        assert UUID(data["push_uuid"])  # UUID 형식 검증
        assert data["user_id"] == "test_user_123"
        assert data["message"] == "테스트 푸시 메시지"
        assert data["topic"] == "test_topic"
        assert data["status"] == "created"
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_push_without_topic(self, async_client: AsyncClient):
        """토픽 없이 푸시 생성 테스트"""
        push_data = {
            "user_id": "test_user_456",
            "message": "토픽 없는 푸시 메시지"
        }
        
        response = await async_client.post("/push", json=push_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["topic"] == "user_test_user_456_default"  # 기본 토픽

    @pytest.mark.asyncio
    async def test_get_push_by_uuid(self, async_client: AsyncClient):
        """UUID로 푸시 조회 테스트"""
        # 먼저 푸시 생성
        push_data = {
            "user_id": "test_user_789",
            "message": "조회 테스트 메시지"
        }
        
        create_response = await async_client.post("/push", json=push_data)
        created_push = create_response.json()
        push_uuid = created_push["push_uuid"]
        
        # UUID로 조회
        response = await async_client.get(f"/push/{push_uuid}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["push_uuid"] == push_uuid
        assert data["user_id"] == "test_user_789"
        assert data["message"] == "조회 테스트 메시지"

    @pytest.mark.asyncio
    async def test_get_nonexistent_push(self, async_client: AsyncClient):
        """존재하지 않는 푸시 조회 테스트"""
        fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
        response = await async_client.get(f"/push/{fake_uuid}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_user_pushes(self, async_client: AsyncClient):
        """사용자별 푸시 목록 조회 테스트"""
        user_id = "test_user_list"
        
        # 여러 푸시 생성
        for i in range(3):
            push_data = {
                "user_id": user_id,
                "message": f"사용자 푸시 {i}"
            }
            await async_client.post("/push", json=push_data)
        
        # 사용자별 조회
        response = await async_client.get(f"/user/{user_id}/pushes")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3
        assert all(push["user_id"] == user_id for push in data)

    @pytest.mark.asyncio
    async def test_get_topic_pushes(self, async_client: AsyncClient):
        """토픽별 푸시 목록 조회 테스트"""
        topic = "test_topic_list"
        
        # 같은 토픽으로 여러 푸시 생성
        for i in range(2):
            push_data = {
                "user_id": f"user_{i}",
                "message": f"토픽 푸시 {i}",
                "topic": topic
            }
            await async_client.post("/push", json=push_data)
        
        # 토픽별 조회
        response = await async_client.get(f"/topic/{topic}/pushes")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        assert all(push["topic"] == topic for push in data)

    @pytest.mark.asyncio
    async def test_delete_push(self, async_client: AsyncClient):
        """푸시 삭제 테스트"""
        # 먼저 푸시 생성
        push_data = {
            "user_id": "test_user_delete",
            "message": "삭제할 푸시"
        }
        
        create_response = await async_client.post("/push", json=push_data)
        created_push = create_response.json()
        push_uuid = created_push["push_uuid"]
        
        # 삭제
        delete_response = await async_client.delete(f"/push/{push_uuid}")
        assert delete_response.status_code == 200
        
        # 삭제 확인
        get_response = await async_client.get(f"/push/{push_uuid}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_nonexistent_push(self, async_client: AsyncClient):
        """존재하지 않는 푸시 삭제 테스트"""
        fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
        response = await async_client.delete(f"/push/{fake_uuid}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_create_push_validation(self, async_client: AsyncClient):
        """푸시 생성 데이터 검증 테스트"""
        # 필수 필드 누락
        invalid_data = {
            "message": "user_id가 없는 푸시"
        }
        
        response = await async_client.post("/push", json=invalid_data)
        assert response.status_code == 422  # Validation Error

    @pytest.mark.asyncio
    async def test_get_user_pushes_with_limit(self, async_client: AsyncClient):
        """제한된 수의 사용자 푸시 조회 테스트"""
        user_id = "test_user_limit"
        
        # 5개 푸시 생성
        for i in range(5):
            push_data = {
                "user_id": user_id,
                "message": f"제한 테스트 푸시 {i}"
            }
            await async_client.post("/push", json=push_data)
        
        # 3개만 조회
        response = await async_client.get(f"/user/{user_id}/pushes?limit=3")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3