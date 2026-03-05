@echo off
echo Fixing JWT package issue...
echo.
pip uninstall jwt -y
pip uninstall PyJWT -y
pip install PyJWT
echo.
echo Done! Now restart your backend server.
pause
