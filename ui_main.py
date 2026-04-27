# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'entrada_ead.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)
import icons_qrc

class Ui_EntradaEAD(object):
    def setupUi(self, EntradaEAD):
        if not EntradaEAD.objectName():
            EntradaEAD.setObjectName(u"EntradaEAD")
        EntradaEAD.resize(461, 338)
        EntradaEAD.setMinimumSize(QSize(461, 0))
        EntradaEAD.setStyleSheet(u"background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 37, 180, 255), stop:0.227273 rgba(0, 97, 216, 255), stop:0.454545 rgba(87, 143, 223, 255), stop:0.75 rgba(153, 177, 198, 255));")
        self.centralwidget = QWidget(EntradaEAD)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")


        self.empresa_text = QLineEdit(self.frame)
        self.empresa_text.setObjectName(u"empresa_text")
        self.empresa_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.empresa_text, 0, 0, 1, 1)

        self.filial_text = QLineEdit(self.frame)
        self.filial_text.setObjectName(u"filial_text")
        self.filial_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.filial_text, 0, 1, 1, 1)

        self.tipo_text = QLineEdit(self.frame)
        self.tipo_text.setObjectName(u"tipo_text")
        self.tipo_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.tipo_text, 0, 2, 1, 1)

        self.matricula_text = QLineEdit(self.frame)
        self.matricula_text.setObjectName(u"matricula_text")
        self.matricula_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.matricula_text, 1, 0, 1, 1)

        self.senha_text = QLineEdit(self.frame)
        self.senha_text.setObjectName(u"senha_text")
        self.senha_text.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")

        self.gridLayout.addWidget(self.senha_text, 1, 1, 1, 1)

        self.verticalLayout.addWidget(self.frame)

        self.btn_iniciar = QPushButton(self.centralwidget)
        self.btn_iniciar.setObjectName(u"btn_iniciar")
        self.btn_iniciar.setMinimumSize(QSize(160, 25))
        font = QFont()
        font.setBold(False)
        font.setItalic(False)
        self.btn_iniciar.setFont(font)
        self.btn_iniciar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_iniciar.setStyleSheet(u"QPushButton{\n"
"	background-color: #fff;\n"
"	color:black;border:solid 0px;\n"
"	font: 75 14px;\n"
"	border-radius:10px;\n"
"}\n"
"QPushButton:hover{\n"
"	background-color:rgb(227, 74, 54);\n"
"	color:#fff\n"
"}	\n"
"")

        self.verticalLayout.addWidget(self.btn_iniciar, 0, Qt.AlignHCenter)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setFamilies([u"Brush Script MT"])
        font1.setItalic(True)
        self.label_2.setFont(font1)
        self.label_2.setStyleSheet(u"color: black; background-color: None;")

        self.verticalLayout.addWidget(self.label_2, 0, Qt.AlignLeft|Qt.AlignBottom)

        EntradaEAD.setCentralWidget(self.centralwidget)

        self.retranslateUi(EntradaEAD)

        QMetaObject.connectSlotsByName(EntradaEAD)
    # setupUi

    def retranslateUi(self, EntradaEAD):
        EntradaEAD.setWindowTitle(QCoreApplication.translate("EntradaEAD", u"EntradaEAD", None))
        self.label_3.setText(QCoreApplication.translate("EntradaEAD", u"<html><head/><body><p align=\"center\"><img src=\":/icons/Imagem1.png\"/><br/><span style=\" font-size:14pt; font-weight:600; color:#d5d5d5;\">ENTRADA EAD</span></p></body></html>", None))
        self.empresa_text.setPlaceholderText(QCoreApplication.translate("EntradaEAD", u"Empresa", None))
        self.filial_text.setPlaceholderText(QCoreApplication.translate("EntradaEAD", u"Filial", None))
        self.tipo_text.setPlaceholderText(QCoreApplication.translate("EntradaEAD", u"Tipo", None))        
        self.matricula_text.setPlaceholderText(QCoreApplication.translate("EntradaEAD", u"Matricula", None))
        self.senha_text.setPlaceholderText(QCoreApplication.translate("EntradaEAD", u"Senha", None))
        
        self.btn_iniciar.setText(QCoreApplication.translate("EntradaEAD", u"INICIAR", None))
        self.label_2.setText(QCoreApplication.translate("EntradaEAD", u"<html><head/><body><p><span style=\" font-size:12pt;\">Rony Franzini 2026</span></p></body></html>", None))
    # retranslateUi

