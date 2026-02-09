@echo off
REM Script to build and run docker-compose on Windows (run as normal user)
cd /d "%~dp0"







)  docker-compose up --build --force-recreate --remove-orphans) else (  docker compose up --build --force-recreate --remove-orphanswhere docker compose >nul 2>&1
nif %ERRORLEVEL%==0 (REM Use `docker compose` if available, otherwise `docker-compose`necho Building and starting containers...