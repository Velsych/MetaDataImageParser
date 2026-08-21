@echo off
uv sync
uv build
uv tool install dist/meta_shit-0.1.0-py3-none-any.whl
uv run pyinstaller --distpath "%cd%" --onefile images_parser/scripts/app.py
md %cd%\images_parser\test
echo MODEL_NAME= > .env
echo API_LINK= >> .env
echo Exe file created