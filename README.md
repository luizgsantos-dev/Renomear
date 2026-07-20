# Renomeação automática de comprovantes bancários

Monitora uma pasta em segundo plano, extrai data de pagamento, recebedor e
valor de cada comprovante em PDF, e move o arquivo já renomeado para
`Renomeados\<EMPRESA>\`, no padrão:

```
DD.MM.AAAA - RECEBEDOR EM MAIÚSCULAS - VALOR,00.pdf
```

Bancos/layouts suportados hoje:
- **Itaú** — comprovante de pagamento de boleto via Sispag (`src/parsers/itau_boleto.py`)
- **Itaú** — comprovante de pagamento de concessionárias via Sispag, ex. contas de telefone/energia (`src/parsers/itau_concessionaria.py`)
- **Banco Inter** — Pix enviado (`src/parsers/inter_pix.py`)
- **Banco Inter** — pagamento de boleto ("Pagamento efetuado") (`src/parsers/inter_boleto.py`)

Quando um comprovante não é reconhecido, ou o recebedor não pôde ser
identificado, ele ainda é movido e renomeado, com `DESCONHECIDO` no(s)
campo(s) que faltou, e cai em `Renomeados\_REVISAR\` — nada fica travado na
pasta de entrada.

Existem duas formas de instalar: **pacote portátil** (recomendado para um
computador que não tem Python nem PowerShell liberado — ex.: o PC do
financeiro) ou **rodando com Python** (para esta máquina de desenvolvimento).

---

## Opção 1 — Pacote portátil (`.exe`, sem instalar nada)

Use esta opção em qualquer computador Windows, mesmo sem Python instalado e
sem permissão para rodar scripts PowerShell. Tudo roda a partir da pasta
`pacote_instalacao\`, que contém um executável standalone
(`RenomeadorComprovantes.exe`) com Python e todas as bibliotecas já
embutidas.

1. Copie a pasta `pacote_instalacao\` inteira para o computador de destino
   (pen-drive, rede, etc.) — pode deixá-la em qualquer lugar (Área de
   Trabalho, Documentos...).
2. Renomeie `.env.example` para `.env` e preencha `PASTA_ENTRADA` com o
   caminho real da pasta onde os comprovantes são salvos hoje nesse
   computador.
3. Dê dois cliques em `instalar.bat`. Isso:
   - cria um pequeno atalho na pasta de Inicialização do Windows
     (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`), sem
     precisar de admin nem de PowerShell — o programa passa a iniciar
     sozinho a cada login;
   - já inicia o programa imediatamente, para teste.
4. Solte um PDF de comprovante na pasta de entrada configurada e confira,
   depois de alguns segundos, se ele aparece renomeado dentro de
   `Renomeados\` (criada automaticamente do lado do `.exe`).

Para desinstalar (parar de iniciar sozinho e encerrar o programa), dois
cliques em `desinstalar.bat`.

Instruções resumidas também estão em `pacote_instalacao\LEIAME.txt`.

### Gerar/atualizar o `.exe` (só nesta máquina de desenvolvimento)

Sempre que o código em `src/` mudar, gere um `.exe` novo e recopie a pasta
`pacote_instalacao\` para os PCs que já a usam:

```powershell
.\build_exe.ps1
```

Isso roda o PyInstaller e já atualiza
`pacote_instalacao\RenomeadorComprovantes.exe`.

---

## Opção 2 — Rodando com Python (esta máquina)

Útil para desenvolvimento/depuração, já que aqui o Python e as dependências
já estão instalados.

### Configuração inicial

1. Abra o arquivo `.env` (já criado a partir de `.env.example`) e preencha
   `PASTA_ENTRADA` com o caminho real da pasta onde os comprovantes são
   salvos hoje. O programa se recusa a iniciar enquanto esse valor contiver
   `PREENCHER`.
2. (Opcional) Ajuste `PASTA_SAIDA`, `CAMINHO_RELATORIO` e `CAMINHO_LOG` se
   quiser outro destino.

### Rodar manualmente (teste / debug)

```powershell
python run_watcher.py
```

Deixa uma janela de console aberta com os logs em tempo real (`Ctrl+C` para
parar).

### Instalar para iniciar sozinho ao logar no Windows (via Task Scheduler)

```powershell
.\install_task.ps1
```

Isso registra a tarefa agendada `RenomeacaoComprovantes`, que roda
`run_watcher.pyw` (sem janela) via `pythonw.exe` toda vez que você fizer
logon no Windows. Para testar sem esperar o próximo logon:

```powershell
schtasks /run /tn "RenomeacaoComprovantes"
```

e depois conferir `logs\app.log`. Para remover a tarefa:

```powershell
.\uninstall_task.ps1
```

**Nota**: esta opção exige PowerShell liberado para rodar scripts e um
Python já instalado — se o PC de destino não tem isso, use a Opção 1.

---

## Relatório

A cada comprovante processado, uma linha é adicionada em
`relatorio_processamento.xlsx` com o arquivo original, o nome novo, os
campos extraídos, o layout detectado e o status (`OK` ou
`REVISAR: <motivo>`). Se a planilha estiver aberta no Excel no momento em
que o watcher tenta salvar, ele tenta de novo automaticamente no próximo
ciclo — nenhum registro é perdido.

## Adicionar um novo banco

1. Crie `src/parsers/novo_banco.py` implementando `BaseParser`
   (`detect(texto)` para reconhecer o layout pelo texto característico do
   PDF, e `extract(texto)` retornando `ExtractedData`).
2. Registre a nova classe na lista `PARSERS` em `src/parsers/__init__.py`.
3. Adicione um PDF de exemplo em `tests/fixtures/` e um teste em
   `tests/` seguindo o padrão de `test_parsers_itau.py`.
4. Gere um `.exe` novo com `.\build_exe.ps1` se for distribuir a pasta
   portátil atualizada.

Nenhum outro arquivo precisa mudar.

## Testes

```powershell
pip install -r requirements-dev.txt
pytest
```

## Solução de problemas

- **(Opção 1 - pacote portátil) `instalar.bat` reclama de "PREENCHER"**:
  o `.env` ainda tem o caminho de exemplo. Abra-o e coloque o caminho real
  da pasta de entrada.
- **(Opção 1) Comprovante não processa**: confira se o processo
  `RenomeadorComprovantes.exe` está rodando (Gerenciador de Tarefas). Se
  não estiver, dê dois cliques em `instalar.bat` novamente — ele também
  inicia o programa na hora.
- **(Opção 2 - Task Scheduler) A tarefa "roda" mas nada acontece**:
  confirme que `pythonw.exe` está acessível em
  `%LOCALAPPDATA%\Microsoft\WindowsApps\pythonw.exe` (Python instalado via
  Microsoft Store usa *App Execution Aliases*, que às vezes não funcionam
  em modo "executar estando o usuário logado ou não"). Rode
  `schtasks /run /tn "RenomeacaoComprovantes"` e confira `logs\app.log`. Se
  continuar sem gerar log nenhum, considere instalar o Python padrão
  (python.org) e ajustar o caminho de `pythonw.exe` em `install_task.ps1`
  — ou simplesmente use a Opção 1 (pacote portátil), que não depende disso.
- **Comprovante caiu em `_REVISAR`**: abra `relatorio_processamento.xlsx`
  para ver qual campo não foi extraído. Geralmente indica um layout de
  banco novo, ainda sem parser, ou um comprovante onde o nome do
  recebedor não pôde ser lido.


