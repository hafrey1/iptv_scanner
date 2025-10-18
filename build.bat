@echo off
chcp 65001 >nul
echo ================================
echo IPTV Scanner Build Tool (Nuitka)
echo ================================
echo.

echo Installing dependencies...
pip install nuitka ordered-set zstandard
pip install aiohttp requests eventlet

echo.
echo Building optimized executable (this may take 5-10 minutes)...
nuitka --standalone --onefile --assume-yes-for-downloads --windows-console-mode=attach --output-filename=IPTV_Scanner.exe iptv_scanner.py

echo.
echo ================================
echo Build completed!
echo EXE location: IPTV_Scanner.exe
echo Please copy config.json to the same directory
echo ================================
pause
