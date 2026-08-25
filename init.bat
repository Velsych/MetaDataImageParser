@echo off
uv sync
uv build
uv tool install dist/meta_shit-0.1.0-py3-none-any.whl
if not exist %cd%\.env (
    echo MODEL_NAME=> .env
    echo API_LINK=>> .env
) else (
    echo .env file already exists
)
md %cd%\images_parser\images
pause