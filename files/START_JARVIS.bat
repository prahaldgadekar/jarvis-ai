@echo off
title JARVIS Launcher
color 0B

echo.
echo  ============================================
echo    J.A.R.V.I.S  --  Starting Up...
echo  ============================================
echo.

:: ── Step 1: Start Ollama no matter what ─────────────────────
echo  [1/3] Starting Ollama...

:: Try all possible Ollama locations
set OLLAMA_EXE=

if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
    set OLLAMA_EXE=%LOCALAPPDATA%\Programs\Ollama\ollama.exe
)
if exist "%PROGRAMFILES%\Ollama\ollama.exe" (
    set OLLAMA_EXE=%PROGRAMFILES%\Ollama\ollama.exe
)
if exist "%PROGRAMFILES(X86)%\Ollama\ollama.exe" (
    set OLLAMA_EXE=%PROGRAMFILES(X86)%\Ollama\ollama.exe
)

:: Also try if ollama is just in PATH
where ollama >nul 2>&1
if %errorlevel% == 0 (
    set OLLAMA_EXE=ollama
)

if "%OLLAMA_EXE%"=="" (
    echo  [!] Ollama not found. Please install from https://ollama.com
    pause
    exit /b 1
)

:: Kill any stuck ollama processes and restart fresh
taskkill /f /im ollama.exe >nul 2>&1
timeout /t 1 /nobreak >nul

:: Start Ollama serve
if "%OLLAMA_EXE%"=="ollama" (
    start "" /B ollama serve
) else (
    start "" /B "%OLLAMA_EXE%" serve
)

echo        Waiting for Ollama to come online...

:: Wait up to 20 seconds
set /a tries=0
:WAIT_LOOP
timeout /t 1 /nobreak >nul
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% == 0 goto OLLAMA_READY
set /a tries+=1
if %tries% LSS 20 goto WAIT_LOOP

echo  [!] Ollama took too long to start. Trying anyway...
goto LAUNCH

:OLLAMA_READY
echo        Ollama is online. OK.

:: ── Step 2: Check models ─────────────────────────────────────
echo  [2/3] Checking AI models...
curl -s http://localhost:11434/api/tags | findstr /i "llama\|qwen\|phi\|mistral" >nul 2>&1
if %errorlevel% == 0 (
    echo        Models found. OK.
) else (
    echo  [!] No models found. Pulling llama3.1...
    ollama pull llama3.1
)

:: ── Step 3: Launch JARVIS ────────────────────────────────────
:LAUNCH
echo  [3/3] Launching JARVIS...
echo.
echo  ============================================
echo    JARVIS is starting!
echo  ============================================

cd /d E:\jarvis
start "" pythonw jarvis.py

timeout /t 2 /nobreak >nul
exit