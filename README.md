# EntradaEAD

Aplicacao desktop em PySide6 para automatizar a rotina de entrada EAD no PCOMM. A interface coleta os dados da operacao, executa a automacao em segundo plano e permite interromper o processamento com seguranca.

## Funcionalidades

- Conecta na sessao `A` do PCOMM.
- Abre a rotina `S6CA`.
- Preenche empresa, filial, tipo, matricula e senha.
- Consulta notas pendentes e processa as entradas encontradas.
- Exibe mensagens de status durante a execucao.
- Salva um print da tela em `Downloads/EntradaEAD/print.png`.

## Requisitos

- Windows.
- Python 3.12 ou versao compativel com as dependencias do projeto.
- IBM Personal Communications (PCOMM) instalado e configurado.
- Sessao `A` disponivel no PCOMM.
- Credenciais validas para a rotina automatizada.

## Instalacao

Crie o ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual no PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

## Execucao

Com o ambiente virtual ativo:

```powershell
python main.py
```

Fluxo esperado de uso:

1. Abra o PCOMM e deixe a sessao `A` pronta para uso.
2. Execute a aplicacao.
3. Preencha os campos `empresa`, `filial`, `tipo`, `matricula` e `senha`.
4. Clique em `INICIAR`.
5. Use `STOP` para solicitar a parada segura da automacao.

## Build do executavel

O projeto possui configuracao pronta do PyInstaller em `EntradaEAD.spec`.

```powershell
pyinstaller EntradaEAD.spec
```

## Estrutura principal

- `main.py`: inicializa a interface e controla a thread da automacao.
- `pcomm.py`: contem o fluxo de automacao no PCOMM.
- `ui_main.py`: codigo gerado da interface Qt.
- `entrada_ead.ui`: layout da tela.
- `EntradaEAD.spec`: configuracao de empacotamento com PyInstaller.
- `requirements.txt`: dependencias congeladas do ambiente.

## Observacoes

- A automacao depende das mensagens e coordenadas da tela do host. Se o layout do PCOMM mudar, o fluxo pode precisar de ajuste.
- O projeto usa `pywin32` e automacao COM, entao a execucao fora do Windows nao e suportada.
