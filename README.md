# SeatSniper


### Requirements Start Application
- Docker
- Docker Compose


### Project Startup
```bash
> docker pull python:3.12
> docker pull postgres:17.2
> docker network create seatsnipernet
> docker volume create local-services-db-data
> docker compose -f docker-compose-services.yml up -d
> docker build . -t "seatsniper-core":"latest"
> docker compose -f docker-compose.yml up -d
```