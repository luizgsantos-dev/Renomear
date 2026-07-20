<#
.SYNOPSIS
    Gera o executavel standalone (RenomeadorComprovantes.exe) e o coloca
    dentro de pacote_instalacao/, pronto para copiar para outro PC.

.NOTES
    Rode isto SOMENTE nesta maquina de desenvolvimento (que ja tem Python
    e as dependencias instaladas). O .exe gerado e' o que vai para o PC
    novo - o PC novo nao precisa rodar este script.
#>

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

python -m PyInstaller --onefile --noconsole --name RenomeadorComprovantes `
    --collect-all pdfplumber --collect-all pdfminer --collect-all pypdfium2 `
    --hidden-import dotenv `
    run_watcher.py

Copy-Item -Path "dist\RenomeadorComprovantes.exe" `
    -Destination "pacote_instalacao\RenomeadorComprovantes.exe" -Force

Write-Host ""
Write-Host "Executavel atualizado em pacote_instalacao\RenomeadorComprovantes.exe"
Write-Host "Copie a pasta 'pacote_instalacao' inteira para o PC novo."
