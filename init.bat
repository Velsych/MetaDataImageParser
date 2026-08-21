@echo off
uv sync
uv build
uv tool install dist/meta_shit-0.1.0-py3-none-any.whl
echo MODEL_NAME= > .env
echo API_LINK= >> .env
setenv %cd%\.env
uv run pyinstaller --distpath "%cd%" --onefile images_parser/scripts/app.py
md %cd%\images_parser\images
echo Exe file created