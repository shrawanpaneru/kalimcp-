@echo off
echo Starting LM Studio Server...
lms server start

echo.
echo Starting Unrestricted Kali Agent...
python "c:\Users\ACER\Desktop\Quasar-1.4.1\kali-mcp\kali_agent.py"

echo.
echo Session ended.
pause
