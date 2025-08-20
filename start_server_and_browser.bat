@echo off
echo Starting Django development server...

REM 激活虚拟环境 (如果存在)
REM 如果你的项目使用了虚拟环境，请将下一行的 "venv\Scripts\activate" 替换为你虚拟环境的实际路径
REM 例如：call C:\Users\YourUser\project_name\venv\Scripts\activate
REM 如果没有使用虚拟环境，请删除或注释掉这一行
REM call envs\Scripts\activate

REM 启动 Django 开发服务器
start python manage.py runserver

timeout /t 8 >nul
REM 等待服务器启动，这里等待 5 秒，你可以根据需要调整

echo Opening browser...
start http://127.0.0.1:8000

echo Script finished.