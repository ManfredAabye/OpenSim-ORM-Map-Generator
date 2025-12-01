#!/bin/bash

echo "================================================"
echo "ORM Map Generator - Linux Binary Builder"
echo "================================================"
echo

# Prüfe ob Python3 installiert ist
if ! command -v python3 &> /dev/null; then
    echo "FEHLER: Python3 ist nicht installiert!"
    echo "Installieren Sie Python3 mit:"
    echo "  sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Prüfe ob Virtual Environment existiert
if [ -d ".venv" ]; then
    echo "Virtual Environment gefunden."
    PYTHON_CMD=".venv/bin/python3"
    PIP_CMD=".venv/bin/pip3"
    
    # Aktiviere Virtual Environment
    source .venv/bin/activate
else
    echo "Kein Virtual Environment gefunden."
    echo "Erstelle Virtual Environment..."
    python3 -m venv .venv
    
    if [ $? -ne 0 ]; then
        echo "FEHLER: Virtual Environment konnte nicht erstellt werden!"
        echo "Installieren Sie python3-venv mit:"
        echo "  sudo apt install python3-venv"
        exit 1
    fi
    
    source .venv/bin/activate
    PYTHON_CMD=".venv/bin/python3"
    PIP_CMD=".venv/bin/pip3"
    echo
fi

# Prüfe ob PyInstaller installiert ist
echo "Prüfe Abhängigkeiten..."
$PIP_CMD show pyinstaller > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "PyInstaller nicht gefunden. Installiere PyInstaller..."
    $PIP_CMD install pyinstaller
    echo
fi

# Prüfe ob Pillow installiert ist
$PIP_CMD show Pillow > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Pillow nicht gefunden. Installiere Pillow..."
    $PIP_CMD install Pillow
    echo
fi

# Prüfe ob tkinter verfügbar ist
$PYTHON_CMD -c "import tkinter" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "WARNUNG: tkinter ist nicht installiert!"
    echo "Installieren Sie tkinter mit:"
    echo "  sudo apt install python3-tk"
    echo
    read -p "Trotzdem fortfahren? (j/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Jj]$ ]]; then
        exit 1
    fi
fi

echo "Erstelle Binary-Datei..."
echo
$PYTHON_CMD -m PyInstaller --onefile --windowed --name "ORM-Map-Generator" --clean orm-maps-generator.py

if [ $? -ne 0 ]; then
    echo
    echo "================================================"
    echo "FEHLER: Build fehlgeschlagen!"
    echo "================================================"
    exit 1
fi

# Mache die Binary ausführbar
chmod +x dist/ORM-Map-Generator 2>/dev/null

echo
echo "================================================"
echo "Build erfolgreich abgeschlossen!"
echo "================================================"
echo
echo "Binary-Datei: dist/ORM-Map-Generator"
echo
echo "Ausführen mit: ./dist/ORM-Map-Generator"
echo
echo "HINWEIS: Die Binary funktioniert nur auf ähnlichen"
echo "Linux-Systemen (gleiche Architektur und Bibliotheken)."
echo "Für andere Systeme muss neu kompiliert werden."
echo
