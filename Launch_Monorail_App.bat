@echo off
title Monorail LCA/LCCA Assessment Tool
color 0A

echo.
echo ============================================================
echo     🚀 Monorail LCA/LCCA Assessment Tool Launcher
echo ============================================================
echo.
echo Starting the Enhanced Application...
echo.

cd /d "%~dp0"
python run_enhanced_app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================================
    echo     ❌ Error occurred! Check if Python is installed.
    echo ============================================================
    pause
)
