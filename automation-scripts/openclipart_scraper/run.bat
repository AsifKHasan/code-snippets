@echo off
set PROJECT_ROOT=%~dp0
set PYTHONPATH=%PROJECT_ROOT%src

python -m openclipart.cli --config conf\config.yml %*
