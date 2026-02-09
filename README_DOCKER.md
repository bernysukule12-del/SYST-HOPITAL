# Docker - Hospital API

This document explains how to build and run the project using Docker on Windows.

## Prerequisites
- Docker Desktop installed and running (Windows). Enable WSL2 backend recommended.
- At least 4GB free disk space.

## Files added
- `Dockerfile` - image build
- `docker-compose.yml` - services: `web` and `db`
- `entrypoint.sh` - runs migrations and `collectstatic` before starting gunicorn
- `.env.example` - example environment variables
- `.env` - development environment variables (created)
- `run_docker.bat` - helper to launch compose on Windows

## Quick start (Windows)
1. Open PowerShell (Run as Administrator if needed).
2. Ensure Docker Desktop is running.
3. From project root:

```powershell
cd /d "C:\Users\pc\Desktop\SYST HOPITAL"
.\run_docker.bat
```

Or run directly:

```powershell
docker-compose up --build --force-recreate --remove-orphans
# or, if you have the new docker CLI
docker compose up --build --force-recreate --remove-orphans
```

The web service will be available at: `http://127.0.0.1:8000/`.

## Environment
- If you want to change DB credentials or allowed hosts, edit the `.env` file.
- For production, set `DJANGO_DEBUG=False` and `DJANGO_SECRET_KEY` to a secure value.

## Common issues
- `docker-compose` not found: use `docker compose` (new CLI). If neither exists, install Docker Desktop.
- Permission issues with `entrypoint.sh`: Windows will ignore chmod; container runs Linux and will execute the script from the image.
- Ports already in use: change `ports` mapping in `docker-compose.yml`.

## Stopping containers

```powershell
# stop and remove containers
docker-compose down
# or with new CLI
docker compose down
```

## Debugging
- View logs for web:

```powershell
docker-compose logs -f web
# or
docker compose logs -f web
```

If you want, I can also:
- Convert `docker-compose.yml` to use a separate `Dockerfile` stage for production optimizations.
- Add a `Makefile` to simplify common tasks.
- Prepare a small CI pipeline (GitHub Actions) to build and push images.

