# Makefile for Chatboot-RAG project

.PHONY: help install docker-build docker-run docker-compose-up k8s-deploy clean

help:
	@echo "Available commands:"
	@echo "  make install         - Install Python dependencies"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run Docker container"
	@echo "  make docker-compose-up - Start services with Docker Compose"
	@echo "  make k8s-deploy      - Deploy to Kubernetes"
	@echo "  make clean           - Clean up generated files"

install:
	pip install -r requirements.txt

docker-build:
	docker build -t chatboot-rag:latest .

docker-run:
	docker run -p 8501:8501 -e OLLAMA_HOST=http://host.docker.internal:11434 chatboot-rag:latest

docker-compose-up:
	docker-compose up -d

k8s-deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -f conversation_archive_*.json
	rm -rf models/*.idx models/*.pkl
	rm -f documents.txt
