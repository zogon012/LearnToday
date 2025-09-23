#!/bin/bash

# 코드 포매팅 스크립트

echo "Formatting code with Black and Ruff..."

# Black으로 포매팅
echo "Formatting with Black..."
poetry run black app tests

# Ruff로 자동 수정
echo "Auto-fixing with Ruff..."
poetry run ruff check --fix app tests

echo "Code formatting completed!"
