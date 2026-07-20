@echo off
setlocal

set "LAUNCHER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\RenomeadorComprovantes.bat"

taskkill /IM RenomeadorComprovantes.exe /F >nul 2>&1

if exist "%LAUNCHER%" (
    del "%LAUNCHER%"
    echo Removido. O programa nao vai mais iniciar sozinho no login.
) else (
    echo Nao estava instalado para iniciar automaticamente.
)

echo.
pause
