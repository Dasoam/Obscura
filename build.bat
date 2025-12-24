@REM This Source Code Form is subject to the terms of the Mozilla Public
@REM License, v. 2.0. If a copy of the MPL was not distributed with this
@REM file, You can obtain one at https://mozilla.org/MPL/2.0/.
@REM
@REM Copyright (c) 2025 Obscura Contributors

@echo off
REM Build Obscura Windows Application
REM This script builds a single EXE using PyInstaller

echo Building Obscura...
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --timeout 300
echo.

REM Build with PyInstaller
echo Building executable...
pyinstaller obscura.spec
echo.

REM Check if build was successful
if exist dist\Obscura.exe (
    echo Build successful!
    echo Executable: dist\Obscura.exe
) else (
    echo Build failed!
    exit /b 1
)

echo.
echo Done!
pause
