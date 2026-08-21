@echo off
uv sync
uv build
uv tool install dist/*.whl
uv run pyinstaller --distpath "%cd%" --onefile images_parser/scripts/app.py
echo Exe file created