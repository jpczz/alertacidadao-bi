@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python nao encontrado. Instale Python 3.12 ou superior e tente novamente.
  echo Guia: LEIA-ME.md
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
if errorlevel 1 goto :error
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto :error
start "" "http://127.0.0.1:8000"
echo Aplicacao local em http://127.0.0.1:8000 . Mantenha esta janela aberta.
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1
exit /b
:error
echo A instalacao falhou. Confira sua conexao e a versao do Python.
pause
exit /b 1
