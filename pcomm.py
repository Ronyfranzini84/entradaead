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
    
def sair_pcomm(pcomm):
    pcomm.send_keys("[PF9]")
    pcomm.send_keys("DISC")
    pcomm.send_keys("[ENTER]")

def extrair_notas(pcomm):
    lista = []

    # linhas onde comecam os dados (ajuste conforme necessario)
    for linha in range(9, 23):
        numero = pcomm.get_text(linha, 18, 8).strip()

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

def voltar_tela(pcomm, vezes=2):
    for _ in range(vezes):
        pcomm.send_keys("[PF3]")
        time.sleep(0.5)    

def iniciar_pcomm(empresa, filial, tipo_atividade, matricula, senha, should_stop=None):
    if should_stop is None:
        should_stop = lambda: False

    def check_stop():
        if should_stop():
            raise RuntimeError("Automacao interrompida pelo usuario.")

    pythoncom.CoInitialize()
    pcomm = None
    try:
        pcomm = PCOMAutomation()
        dados_execucoes = []

        check_stop()
        pcomm.send_keys("[enter]")

        tela_conectada = False
        for tela in [1, 2, 3]:
            check_stop()
            try:
                pcomm.send_keys(str(tela))
                pcomm.send_keys("[enter]")
                time.sleep(2)
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
                    pcomm.send_keys("[PF9]")
                    time.sleep(1)
            except Exception as e:
                print(f"Tela {tela} erro exception: {e}")
                pcomm.send_keys("[PF9]")
                time.sleep(1)

        if not tela_conectada:
            raise ConnectionError("Nao foi possivel conectar em nenhuma tela do PCOMM.")

        check_stop()
        pcomm.send_keys("S6CA")
        pcomm.send_keys("[enter]")

        time.sleep(1)

        pcomm.send_keys(empresa)
        pcomm.send_keys(filial)
        pcomm.send_keys(tipo_atividade)
        pcomm.send_keys(6)
        pcomm.send_keys("[enter]")

        if len(matricula) != 10:
            pcomm.send_keys(matricula)
            pcomm.send_keys("[tab]")
        else:
            pcomm.send_keys(matricula)

        if len(senha) != 10:
            pcomm.send_keys(senha)
            pcomm.send_keys("[tab]")
        else:
            pcomm.send_keys(senha)

        pcomm.send_keys(4)
        pcomm.send_keys(1)
        pcomm.send_keys("[enter]")

        pcomm.send_keys(4)
        pcomm.send_keys("[enter]")

        time.sleep(1)
        check_stop()
        rodape = pcomm.get_text(24, 8, 50).strip().upper()

        if "NAO ENCONTRADO NOTAS FISCAIS SEM DAR ENTRADA" in rodape:
            sair_pcomm(pcomm)
            return dados_execucoes

        notas = extrair_notas(pcomm)
        dados_execucoes.extend(notas)

        # Continua o fluxo do app para processar cada nota na tela seguinte.
        voltar_tela(pcomm, vezes=2)

        pcomm.send_keys(senha)

        pcomm.send_keys(4, 6, 26)
        pcomm.send_keys(2)
        pcomm.send_keys("[enter]")

        pcomm.send_keys(3)
        pcomm.send_keys("[enter]")

        pcomm.send_keys(senha)

        for indice, nota in enumerate(notas, start=1):
            check_stop()
            empr = nota["empr"]
            fil = nota["fil"]
            numero = nota["numero"]
            carga = nota["carga"]

            print(f"Processando nota {indice}/{len(notas)}: EMP={empr} FIL={fil} NF={numero} CARGA={carga}")

            concluida = False
            for tentativa in range(1, 6):
                check_stop()

                # Limpa campos antes de preencher para evitar resquicio de valor anterior.
                pcomm.send_keys("[PA1]")
                time.sleep(0.3)

                pcomm.send_keys(str(empr), 9, 20)
                pcomm.send_keys(str(fil), 9, 23)
                pcomm.send_keys(str(numero), 9, 31)
                pcomm.send_keys(str(carga), 9, 46)
                pcomm.send_keys("[enter]")
                time.sleep(0.7)

                rodape = pcomm.get_text(24, 7, 17).strip().upper()
              

                if "CAMPO OBRIGATORIO" in rodape:
                    print(f"NF {numero}: pedido de senha (tentativa {tentativa}).")
                    pcomm.send_keys(str(senha), 4, 69)
                    pcomm.send_keys("[enter]")
                    time.sleep(0.7)
                    continue

                if "JA FOI DADO ENTRADA" in rodape:
                    print(f"NF {numero}: ja possui entrada. Indo para a proxima.")
                    concluida = True
                    break

                if "ERRO" in rodape:
                    print(f"NF {numero}: erro de tela na tentativa {tentativa}: {rodape}")
                    continue

                print(f"NF {numero}: processada (tentativa {tentativa}).")
                concluida = True
                break

            if not concluida:
                print(f"NF {numero}: nao concluiu apos 5 tentativas. Seguindo fluxo.")
            else:
                sair_pcomm(pcomm)

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

