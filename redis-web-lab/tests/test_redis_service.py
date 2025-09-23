import pytest
from app.models import PushRecord
from app.redis_service import RedisService
from uuid import uuid4
from datetime import datetime


class TestRedisService:
    """Redis 서비스 테스트"""

    @pytest.mark.asyncio
    async def test_redis_connection(self, test_redis_service: RedisService):
        """Redis 연결 테스트"""
        is_connected = await test_redis_service.is_connected()
        assert is_connected is True

    @pytest.mark.asyncio
    async def test_save_and_get_push_record(self, test_redis_service: RedisService):
        """푸시 기록 저장 및 조회 테스트"""
        # 테스트 데이터 생성
        push_uuid = str(uuid4())
        now = datetime.now().isoformat()
        
        record = PushRecord(
            push_uuid=push_uuid,
            user_id="test_user_123",
            message="테스트 메시지",
            topic="test_topic",
            created_at=now,
            api_call_time=now,
            status="created"
        )
        
        # 저장
        success = await test_redis_service.save_push_record(record)
        assert success is True
        
        # 조회
        retrieved_record = await test_redis_service.get_push_record(push_uuid)
        assert retrieved_record is not None
        assert retrieved_record.push_uuid == push_uuid
        assert retrieved_record.user_id == "test_user_123"
        assert retrieved_record.message == "테스트 메시지"
        assert retrieved_record.topic == "test_topic"

    @pytest.mark.asyncio
    async def test_get_nonexistent_push_record(self, test_redis_service: RedisService):
        """존재하지 않는 푸시 기록 조회 테스트"""
        fake_uuid = str(uuid4())
        record = await test_redis_service.get_push_record(fake_uuid)
        assert record is None

    @pytest.mark.asyncio
    async def test_get_user_pushes(self, test_redis_service: RedisService):
        """사용자별 푸시 기록 조회 테스트"""
        user_id = "test_user_456"
        now = datetime.now().isoformat()
        
        # 여러 개의 푸시 기록 생성
        records = []
        for i in range(3):
            push_uuid = str(uuid4())
            record = PushRecord(
                push_uuid=push_uuid,
                user_id=user_id,
                message=f"테스트 메시지 {i}",
                topic=f"test_topic_{i}",
                created_at=now,
                api_call_time=now,
                status="created"
            )
            records.append(record)
            await test_redis_service.save_push_record(record)
        
        # 사용자 푸시 기록 조회
        user_records = await test_redis_service.get_user_pushes(user_id)
        assert len(user_records) == 3
        assert all(r.user_id == user_id for r in user_records)

    @pytest.mark.asyncio
    async def test_get_topic_pushes(self, test_redis_service: RedisService):
        """토픽별 푸시 기록 조회 테스트"""
        topic = "test_topic_special"
        now = datetime.now().isoformat()
        
        # 같은 토픽으로 여러 푸시 기록 생성
        for i in range(2):
            push_uuid = str(uuid4())
            record = PushRecord(
                push_uuid=push_uuid,
                user_id=f"user_{i}",
                message=f"토픽 테스트 메시지 {i}",
                topic=topic,
                created_at=now,
                api_call_time=now,
                status="created"
            )
            await test_redis_service.save_push_record(record)
        
        # 토픽별 푸시 기록 조회
        topic_records = await test_redis_service.get_topic_pushes(topic)
        assert len(topic_records) == 2
        assert all(r.topic == topic for r in topic_records)

    @pytest.mark.asyncio
    async def test_delete_push_record(self, test_redis_service: RedisService):
        """푸시 기록 삭제 테스트"""
        # 테스트 데이터 생성 및 저장
        push_uuid = str(uuid4())
        now = datetime.now().isoformat()
        
        record = PushRecord(
            push_uuid=push_uuid,
            user_id="delete_test_user",
            message="삭제 테스트 메시지",
            topic="delete_test_topic",
            created_at=now,
            api_call_time=now,
            status="created"
        )
        
        await test_redis_service.save_push_record(record)
        
        # 존재 확인
        retrieved_record = await test_redis_service.get_push_record(push_uuid)
        assert retrieved_record is not None
        
        # 삭제
        success = await test_redis_service.delete_push_record(push_uuid)
        assert success is True
        
        # 삭제 확인
        deleted_record = await test_redis_service.get_push_record(push_uuid)
        assert deleted_record is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_record(self, test_redis_service: RedisService):
        """존재하지 않는 기록 삭제 테스트"""
        fake_uuid = str(uuid4())
        success = await test_redis_service.delete_push_record(fake_uuid)
        assert success is False