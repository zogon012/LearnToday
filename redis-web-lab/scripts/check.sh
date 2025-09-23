#!/bin/bash

# 코드 품질 검사 스크립트

echo "Running code quality checks..."

# Ruff로 린팅
echo "Running Ruff linter..."
poetry run ruff check app tests

# Black으로 포매팅 체크
echo "Checking code formatting with Black..."
poetry run black --check app tests

# MyPy로 타입 검사
echo "Running MyPy type checking..."
poetry run mypy app

# 테스트 실행
echo "Running tests..."
poetry run pytest tests/ -v --cov=app --cov-report=term-missing

echo "Code quality checks completed!"
