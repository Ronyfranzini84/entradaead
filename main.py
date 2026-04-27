from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
import pcomm
from ui_main import Ui_EntradaEAD
import sys
import icons_qrc


class AutomacaoWorker(QObject):
    finalizado = Signal(list)
    erro = Signal(str)
    status = Signal(str)

    def __init__(self, empresa, filial, tipo, matricula, senha):
        super().__init__()
        self.empresa = empresa
        self.filial = filial
        self.tipo = tipo
        self.matricula = matricula
        self.senha = senha
        self._cancelado = False

    def cancelar(self):
        self._cancelado = True

    def deve_parar(self):
        return self._cancelado

    def atualizar_status(self, mensagem):
        self.status.emit(mensagem)

    def run(self):
        try:
            registros = pcomm.iniciar_pcomm(
                self.empresa,
                self.filial,
                self.tipo,
                self.matricula,
                self.senha,
                should_stop=self.deve_parar,
                on_status=self.atualizar_status,
            )
            self.finalizado.emit(registros)
        except Exception as exc:
            self.erro.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_EntradaEAD()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/icons/Imagem1.png"))

        self.worker_thread = None
        self.worker = None
        self.parando = False

        self.ui.btn_iniciar.clicked.connect(self.on_btn_iniciar_clicked)

    def on_btn_iniciar_clicked(self):
        if self.worker_thread is None:
            self.iniciar_automacao()
        else:
            self.parar_automacao()

    def campos_preenchidos(self, exibir_alerta=False):
        empresa = self.ui.empresa_text.text().strip()
        filial = self.ui.filial_text.text().strip()
        tipo = self.ui.tipo_text.text().strip()
        matricula = self.ui.matricula_text.text().strip()
        senha = self.ui.senha_text.text().strip()

        ok = all([empresa, filial, tipo, matricula, senha])
        if not ok and exibir_alerta:
            QMessageBox.warning(self, "Campos obrigatorios", "Preencha todos os campos antes de iniciar.")
        return ok

    def iniciar_automacao(self):
        if self.worker_thread is not None:
            QMessageBox.information(self, "Em execucao", "A automacao ja esta em execucao.")
            return

        self.parando = False

        if not self.campos_preenchidos(exibir_alerta=True):
            return

        empresa = self.ui.empresa_text.text().strip()
        filial = self.ui.filial_text.text().strip()
        tipo = self.ui.tipo_text.text().strip()
        matricula = self.ui.matricula_text.text().strip()
        senha = self.ui.senha_text.text().strip()

        self.ui.btn_iniciar.setEnabled(True)
        self.ui.btn_iniciar.setText("STOP")

        self.worker_thread = QThread(self)
        self.worker = AutomacaoWorker(empresa, filial, tipo, matricula, senha)
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finalizado.connect(self.on_automacao_finalizada)
        self.worker.erro.connect(self.on_automacao_erro)
        self.worker.status.connect(self.on_status_atualizado)
        self.worker.finalizado.connect(self.worker_thread.quit)
        self.worker.erro.connect(self.worker_thread.quit)
        self.worker_thread.finished.connect(self.limpar_thread)

        self.worker_thread.start()

    def parar_automacao(self):
        if self.worker is None or self.worker_thread is None:
            return

        self.parando = True
        self.worker.cancelar()
        self.ui.btn_iniciar.setEnabled(False)
        self.ui.btn_iniciar.setText("PARANDO...")
        self.ui.btn_iniciar.setToolTip("Aguardando o PCOMM concluir a etapa atual.")

    def on_status_atualizado(self, mensagem):
        self.ui.btn_iniciar.setToolTip(mensagem)

    def on_automacao_finalizada(self, registros):
        QMessageBox.information(self, "Concluido", f"Automacao finalizada. {len(registros)} Entradas.")

    def on_automacao_erro(self, mensagem):
        if self.parando and "interrompida" in mensagem.lower():
            QMessageBox.information(self, "Parada", "Automacao interrompida.")
            return

        QMessageBox.critical(self, "Erro", mensagem)

    def limpar_thread(self):
        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

        if self.worker_thread is not None:
            self.worker_thread.deleteLater()
            self.worker_thread = None

        self.parando = False
        self.ui.btn_iniciar.setEnabled(True)
        self.ui.btn_iniciar.setText("INICIAR")
        self.ui.btn_iniciar.setToolTip("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())