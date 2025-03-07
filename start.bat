@echo off
cd /d "C:\Users\CMUTI\Desktop\Joguinho"
call .\.venv\Scripts\activate
python run.py &
sleep 5
start chrome.exe http://172.20.21.104:3000/  