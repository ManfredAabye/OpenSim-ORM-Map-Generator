@echo off
echo ================================================
echo ORM Map Generator - EXE Builder
echo ================================================
echo.

REM Prüfe ob Virtual Environment existiert
if exist ".venv\Scripts\python.exe" (
    echo Virtual Environment gefunden.
    set PYTHON_CMD=.venv\Scripts\python.exe
) else (
    echo Kein Virtual Environment gefunden, verwende System-Python.
    set PYTHON_CMD=python
)

REM Prüfe ob PyInstaller installiert ist
%PYTHON_CMD% -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller nicht gefunden. Installiere PyInstaller...
    %PYTHON_CMD% -m pip install pyinstaller
    echo.
)

REM Prüfe ob Pillow installiert ist
%PYTHON_CMD% -m pip show Pillow >nul 2>&1
if errorlevel 1 (
    echo Pillow nicht gefunden. Installiere Pillow...
    %PYTHON_CMD% -m pip install Pillow
    echo.
)

echo Erstelle EXE-Datei...
echo.
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "ORM-Map-Generator" --clean orm-maps-generator.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo FEHLER: Build fehlgeschlagen!
    echo ================================================
    pause
    exit /b 1
)

echo.
echo ================================================
echo Build erfolgreich abgeschlossen!
echo ================================================
echo.
echo EXE-Datei: dist\ORM-Map-Generator.exe
echo.
echo Sie können die EXE-Datei jetzt verwenden oder verteilen.
echo Die Datei benötigt keine Python-Installation.
echo.
pause
