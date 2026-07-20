@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "LAUNCHER=%STARTUP%\RenomeadorComprovantes.bat"

if not exist "%SCRIPT_DIR%RenomeadorComprovantes.exe" (
    echo ERRO: RenomeadorComprovantes.exe nao encontrado nesta pasta.
    echo Verifique se copiou a pasta inteira, nao so o instalar.bat.
    pause
    exit /b 1
)

if not exist "%SCRIPT_DIR%.env" (
    echo ERRO: arquivo .env nao encontrado nesta pasta.
    echo Copie .env.example para .env e preencha PASTA_ENTRADA antes de instalar.
    pause
    exit /b 1
)

findstr /C:"PREENCHER" "%SCRIPT_DIR%.env" >nul
if not errorlevel 1 (
    echo ERRO: o arquivo .env ainda tem "PREENCHER" em algum campo.
    echo Abra o .env e coloque o caminho real da pasta de entrada antes de instalar.
    pause
    exit /b 1
)

(
    echo @echo off
    echo start "" "%SCRIPT_DIR%RenomeadorComprovantes.exe"
) > "%LAUNCHER%"

echo.
echo Instalado com sucesso!
echo O programa vai iniciar sozinho sempre que este usuario fizer login no Windows.
echo.
echo Iniciando agora, para testar...
start "" "%SCRIPT_DIR%RenomeadorComprovantes.exe"
echo Pronto. Coloque um comprovante na pasta de entrada configurada no .env
echo e confira se ele aparece renomeado na pasta de saida em alguns segundos.
echo.
pause
