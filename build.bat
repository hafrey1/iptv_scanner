@echo off
echo ================================
echo IPTV Scanner 打包工具
echo ================================
echo.

echo 正在安装依赖...
pip install pyinstaller aiohttp requests eventlet

echo.
echo 正在打包程序...
pyinstaller --onefile --name="IPTV_Scanner" iptv_scanner.py

echo.
echo ================================
echo 打包完成！
echo 可执行文件位于: dist\IPTV_Scanner.exe
echo 请将 config.json 复制到 exe 同目录
echo ================================
pause
