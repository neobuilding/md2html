@echo off
REM md2html - Markdown to HTML converter (Windows wrapper)
REM Usage: md2html.bat input.md [-o output.html] [--theme dark|light] [--title "Title"] [-w 860px|none|1200px]
REM  If -o is omitted, output defaults to input.html (same dir as source)
REM  Requires: pip install -e . (or pip install -r requirements.txt)

setlocal
set VENV_PYTHON=%~dp0venv\Scripts\python.exe

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Virtual environment not found at venv\Scripts\python.exe
    echo Please run: python -m venv venv  ^&^&  venv\Scripts\pip install -e .
    exit /b 1
)

"%VENV_PYTHON%" -m md2html %*
endlocal
