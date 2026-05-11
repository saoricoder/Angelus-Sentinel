@echo off
title Angelus Sentinel - Launcher
echo =========================================
echo       INICIANDO ANGELUS SENTINEL
echo =========================================
echo.

echo [1/3] Iniciando Backend (FastAPI - Puerto 8000)...
start "Angelus Backend" cmd /c "python -m uvicorn backend.main:app --reload --port 8000"

echo [2/3] Iniciando Frontend (Next.js - Puerto 3000)...
start "Angelus Frontend" cmd /c "cd frontend && npm run dev"

echo [3/3] Iniciando Vercel Serverless Functions (API)...
start "Angelus API" cmd /c "cd api && python -m http.server 8001"

echo.
echo =========================================
echo  Servicios lanzados en ventanas separadas.
echo  - Backend estara en: http://localhost:8000
echo  - Frontend estara en: http://localhost:3000
echo  - Vercel API Functions: http://localhost:8001
echo  - Produccion: https://angelus-sentinel.vercel.app
echo =========================================
echo.
pause
