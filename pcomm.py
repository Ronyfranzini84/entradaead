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

        # linhas onde começam os dados (ajuste conforme necessário)
        for linha in range(9, 2):  
            numero = pcomm.get_text(linha, 18, 8).strip()

            # se não tem número, acabou a lista
            if not numero:
                break

            registro = {
                "empr": pcomm.get_text(linha, 1, 3).strip(),
                "fil": pcomm.get_text(linha, 10, 4).strip(),
                "numero": numero,
                "carga": pcomm.get_text(linha, 64, 10).strip(),
            }

            lista.append(registro)

        return lista

def iniciar_pcomm(empresa, filial, tipo_atividade, matricula, senha):
    pythoncom.CoInitialize()
    pcomm = None
    try:
        pcomm = PCOMAutomation()
        dados_execucoes = []

        pcomm.send_keys("[enter]")

        tela_conectada = False
        for tela in [1, 2, 3]:
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
        rodape = pcomm.get_text(24, 8, 50).strip().upper()

        if "NAO ENCONTRADO NOTAS FISCAIS SEM DAR ENTRADA" in rodape:
            sair_pcomm(pcomm)
        
        else:
            notas = extrair_notas(pcomm)
            dados_execucoes.extend(notas)

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


if __name__ == "__main__":
    empresa = "21"
    filial = "1200"
    tipo_atividade = "d"
    matricula = "2903471500"
    senha = "varejo1289"

    try:
        notas = iniciar_pcomm(empresa, filial, tipo_atividade, matricula, senha)
        print("Conexao PCOMM e login executados com sucesso.")
        print(f"Notas processadas: {len(notas)}")
    except Exception as e:
        print(f"Falha na conexao/login PCOMM: {e}")