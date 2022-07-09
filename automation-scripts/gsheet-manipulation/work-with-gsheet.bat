:: work with gsheet

@echo off

:: parameters
set GSHEET=%1

pushd .\src
.\work-with-gsheet.py  --gsheet "%GSHEET%"
if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
