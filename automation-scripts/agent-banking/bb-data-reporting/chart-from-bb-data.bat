:: bb-data->chart

@echo off

:: bb-data-to-chart
pushd .\src
python bb-data-to-chart.py

if errorlevel 1 (
  popd
  exit /b %errorlevel%
)

popd
