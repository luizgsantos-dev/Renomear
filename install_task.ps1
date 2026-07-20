<#
.SYNOPSIS
    Registra a tarefa agendada que inicia o watcher de renomeacao de
    comprovantes automaticamente ao logar no Windows.

.NOTES
    O pythonw.exe desta maquina vem da Microsoft Store (App Execution Alias).
    Por isso o trigger usa -AtLogOn no contexto da sessao do usuario, em vez
    de "executar estando o usuario logado ou nao" (modo nao suportado de
    forma confiavel pelos aliases do Store).
#>

$ErrorActionPreference = "Stop"

$TaskName    = "RenomeacaoComprovantes"
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptPath  = Join-Path $ScriptDir "run_watcher.pyw"
$PythonwExe  = "$env:LOCALAPPDATA\Microsoft\WindowsApps\pythonw.exe"

if (-not (Test-Path $ScriptPath)) {
    throw "Nao encontrei $ScriptPath. Rode este script a partir da pasta do projeto."
}
if (-not (Test-Path $PythonwExe)) {
    throw "Nao encontrei $PythonwExe. Ajuste a variavel `$PythonwExe neste script para o caminho correto do pythonw.exe."
}

$Action = New-ScheduledTaskAction -Execute $PythonwExe `
    -Argument "`"$ScriptPath`"" -WorkingDirectory $ScriptDir

$Trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$Settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 2) `
    -ExecutionTimeLimit ([TimeSpan]::Zero) `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Write-Host "Tarefa '$TaskName' ja existe. Removendo antes de recriar."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
    -Settings $Settings -RunLevel Limited `
    -Description "Watcher de renomeacao automatica de comprovantes bancarios" | Out-Null

Write-Host "Tarefa '$TaskName' registrada com sucesso."
Write-Host ""
Write-Host "Para testar agora sem esperar o proximo logon, rode:"
Write-Host "    schtasks /run /tn `"$TaskName`""
Write-Host "e confira o arquivo logs\app.log para ver se o watcher iniciou."
