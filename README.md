docker build -t corujo-backend:Dockerfile .
docker run -e PORT=8000 -p 8000:8000 corujo-backend:Dockerfile
