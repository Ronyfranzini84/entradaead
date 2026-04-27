import time
import unicodedata
import pandas as pd
import requests
import win32com.client
import pythoncom
import openpyxl

class PCOMAutomation:
    def __init__(self, sessao_nome="A"):
        self.sessao = win32com.client.Dispatch("PCOMM.autECLPS")
        self.sessao.SetConnectionByName(sessao_nome)
        time.sleep(1)

    def wait_for_input_ready(self, timeout=10000):
        self.sessao.WaitForInputReady(timeout)

    def send_keys(self, valor, linha=None, coluna=None):
        if isinstance(valor, (int, float)):
            valor = str(valor)

        if linha and coluna:
            self.sessao.SetCursorPos(linha, coluna)

        self.sessao.SendKeys(valor)
        time.sleep(0.3)

    def get_text(self, linha, coluna, tamanho):
        return self.sessao.GetText(linha, coluna, tamanho).strip()


def pause(seconds, should_stop=None, step=0.1):
    if should_stop is None:
        time.sleep(seconds)
        return

    fim = time.perf_counter() + seconds
    while True:
        if should_stop():
            raise RuntimeError("Automacao interrompida pelo usuario.")

        restante = fim - time.perf_counter()
        if restante <= 0:
            return

        time.sleep(min(step, restante))


def enviar_com_cancelamento(pcomm, valor, should_stop=None, linha=None, coluna=None):
    if should_stop and should_stop():
        raise RuntimeError("Automacao interrompida pelo usuario.")

    pcomm.send_keys(valor, linha=linha, coluna=coluna)

    if should_stop and should_stop():
        raise RuntimeError("Automacao interrompida pelo usuario.")
    
def sair_pcomm(pcomm, should_stop=None):
    enviar_com_cancelamento(pcomm, "[PF9]", should_stop=should_stop)
    enviar_com_cancelamento(pcomm, "DISC", should_stop=should_stop)
    enviar_com_cancelamento(pcomm, "[ENTER]", should_stop=should_stop)

def extrair_notas(pcomm):
    lista = []

    # linhas onde comecam os dados (ajuste conforme necessario)
    for linha in range(9, 23):
        numero = pcomm.get_text(linha, 17, 10).strip()

        # se nao tem numero, acabou a lista
        if not numero:
            break

        registro = {
            "empr": pcomm.get_text(linha, 3, 2).strip(),
            "fil": pcomm.get_text(linha, 10, 4).strip(),
            "numero": numero,
            "carga": pcomm.get_text(linha, 64, 8).strip(),
        }

        lista.append(registro)

    return lista

def voltar_tela(pcomm, vezes=2, should_stop=None):
    for _ in range(vezes):
        enviar_com_cancelamento(pcomm, "[PF3]", should_stop=should_stop)
        pause(0.5, should_stop=should_stop)

def iniciar_pcomm(empresa, filial, tipo_atividade, matricula, senha, should_stop=None, on_status=None):
    if should_stop is None:
        should_stop = lambda: False

    if on_status is None:
        on_status = lambda mensagem: None

    def check_stop():
        if should_stop():
            raise RuntimeError("Automacao interrompida pelo usuario.")

    def report_status(mensagem):
        on_status(mensagem)

    pythoncom.CoInitialize()
    pcomm = None
    try:
        report_status("Conectando ao PCOMM...")
        pcomm = PCOMAutomation()
        dados_execucoes = []

        check_stop()
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        tela_conectada = False
        for tela in [1, 2, 3]:
            check_stop()
            try:
                report_status(f"Tentando conectar na tela {tela}...")
                enviar_com_cancelamento(pcomm, str(tela), should_stop=should_stop)
                enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)
                pause(2, should_stop=should_stop)
                # Varre as linhas 18 a 24 onde o erro EMS aparece na tela ZOS
                tela_inteira = " ".join(
                    pcomm.get_text(linha, 1, 80).upper() for linha in range(18, 25)
                )
                # Se ainda mostra o menu ZOS com erro, a conexao falhou
                falhou = "EMS" in tela_inteira or "FAILED" in tela_inteira
                if not falhou:
                    tela_conectada = True
                    break
                else:
                    print(f"Tela {tela} falhou, tentando proxima...")
                    enviar_com_cancelamento(pcomm, "[PF9]", should_stop=should_stop)
                    pause(1, should_stop=should_stop)
            except Exception as e:
                print(f"Tela {tela} erro exception: {e}")
                enviar_com_cancelamento(pcomm, "[PF9]", should_stop=should_stop)
                pause(1, should_stop=should_stop)

        if not tela_conectada:
            raise ConnectionError("Nao foi possivel conectar em nenhuma tela do PCOMM.")

        check_stop()
        report_status("Abrindo rotina S6CA...")
        enviar_com_cancelamento(pcomm, "S6CA", should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        pause(1, should_stop=should_stop)

        report_status("Preenchendo filtros iniciais...")
        enviar_com_cancelamento(pcomm, empresa, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, filial, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, tipo_atividade, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, 6, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        if len(matricula) != 10:
            enviar_com_cancelamento(pcomm, matricula, should_stop=should_stop)
            enviar_com_cancelamento(pcomm, "[tab]", should_stop=should_stop)
        else:
            enviar_com_cancelamento(pcomm, matricula, should_stop=should_stop)

        if len(senha) != 10:
            enviar_com_cancelamento(pcomm, senha, should_stop=should_stop)
            enviar_com_cancelamento(pcomm, "[tab]", should_stop=should_stop)
        else:
            enviar_com_cancelamento(pcomm, senha, should_stop=should_stop)

        enviar_com_cancelamento(pcomm, 4, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, 1, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        enviar_com_cancelamento(pcomm, 4, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        pause(1, should_stop=should_stop)
        check_stop()
        rodape = pcomm.get_text(24, 8, 50).strip().upper()

        if "NAO ENCONTRADO NOTAS FISCAIS SEM DAR ENTRADA" in rodape:
            sair_pcomm(pcomm, should_stop=should_stop)
            return dados_execucoes

        report_status("Lendo notas pendentes...")
        notas = extrair_notas(pcomm)
        dados_execucoes.extend(notas)

        # Continua o fluxo do app para processar cada nota na tela seguinte.
        voltar_tela(pcomm, vezes=2, should_stop=should_stop)

        enviar_com_cancelamento(pcomm, senha, should_stop=should_stop)

        enviar_com_cancelamento(pcomm, 4, should_stop=should_stop, linha=6, coluna=26)
        enviar_com_cancelamento(pcomm, 2, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        enviar_com_cancelamento(pcomm, 3, should_stop=should_stop)
        enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)

        enviar_com_cancelamento(pcomm, senha, should_stop=should_stop)

        for indice, nota in enumerate(notas, start=1):
            check_stop()
            empr = nota["empr"]
            fil = nota["fil"]
            numero = nota["numero"]
            carga = nota["carga"]

            report_status(f"Processando nota {indice} de {len(notas)}...")

            print(f"Processando nota {indice}/{len(notas)}: EMP={empr} FIL={fil} NF={numero} CARGA={carga}")

            concluida = False
            for tentativa in range(1, 3):
                check_stop()

                # Limpa campos antes de preencher para evitar resquicio de valor anterior.
                enviar_com_cancelamento(pcomm, "[PA1]", should_stop=should_stop)
                pause(0.3, should_stop=should_stop)

                enviar_com_cancelamento(pcomm, str(empr), should_stop=should_stop, linha=9, coluna=20)
                enviar_com_cancelamento(pcomm, str(fil), should_stop=should_stop, linha=9, coluna=23)
                enviar_com_cancelamento(pcomm, str(numero), should_stop=should_stop, linha=9, coluna=31)
                enviar_com_cancelamento(pcomm, str(carga), should_stop=should_stop, linha=9, coluna=46)
                enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)
                pause(0.7, should_stop=should_stop)

                rodape = pcomm.get_text(24, 7, 17).strip().upper()
              

                if "CAMPO OBRIGATORIO" in rodape:
                    print(f"NF {numero}: pedido de senha (tentativa {tentativa}).")
                    enviar_com_cancelamento(pcomm, str(senha), should_stop=should_stop, linha=4, coluna=69)
                    enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)
                    pause(0.7, should_stop=should_stop)
                    continue

                if "OPERACAO EFETUADA" in rodape:
                    enviar_com_cancelamento(pcomm, "[enter]", should_stop=should_stop)
                    print(f"NF {numero}: ja possui entrada. Indo para a proxima.")
                    concluida = True
                    break

                
            if not concluida:
                print(f"NF {numero}: nao concluiu apos 2 tentativas. Seguindo fluxo.")

        sair_pcomm(pcomm, should_stop=should_stop)

        return dados_execucoes
    except Exception:
        raise
    finally:
        if pcomm is not None:
            pcomm = None

        try:
            pythoncom.CoUninitialize()
        except Exception:
            pass

