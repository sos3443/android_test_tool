echo
for /f "delims=" %%i in ('dir /s /b *.pickle') do echo.>%%i
pause