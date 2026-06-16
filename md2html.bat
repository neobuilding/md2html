@echo off
REM md2html - Markdown to HTML converter (Windows wrapper)
REM Usage: md2html.bat input.md [-o output.html] [--theme dark|light] [--title "Title"] [-w 860px|none|1200px]
REM  If -o is omitted, output defaults to input.html (same dir as source)

setlocal
set VENV_PYTHON=%~dp0venv\Scripts\python.exe
set SCRIPT=%~dp0md2html.py

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Virtual environment not found. Please run setup first.
    exit /b 1
)

"%VENV_PYTHON%" "%SCRIPT%" %*
endlocal
