import sys,math,random,re,os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget,
    QToolButton, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy,
    QHBoxLayout, QSpinBox, QPushButton, QLineEdit, QFrame,QFormLayout,QComboBox,QTableWidget,QTableWidgetItem,QScrollArea,QHeaderView,QGroupBox,QTextEdit,QDoubleSpinBox,QDialog,QTextBrowser
)
import tempfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon,QPixmap
import uuid

from PyQt5.QtCore import Qt, QSize
import numpy as np
import webbrowser
from matplotlib.figure import Figure
from sympy import Matrix,sympify,simplify,symbols,diff,integrate,lambdify
import sympy as sp

def obtener_ruta_recurso(rel_path):
    """Devuelve la ruta absoluta al recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

class SubmenuBase(QWidget):
    def __init__(self, stack=None, menu_widget=None):
        super().__init__()
        self.stack = stack
        self.menu_widget = menu_widget

    def add_back_button(self, layout):
        back_btn = QToolButton()
        back_btn.setText("Volver al Menú")
        back_btn.setIcon(QIcon(obtener_ruta_recurso(os.path.join("imagenes", "volver.png"))))
        back_btn.setIconSize(QSize(24, 24))
        back_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        back_btn.setStyleSheet("""
            QToolButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 14px;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QToolButton:hover {
                background-color: #95a5a6;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

    def go_back(self):
        if self.stack and self.menu_widget:
            self.stack.setCurrentWidget(self.menu_widget)
def interpretar_valor(texto):
    # Elimina espacios al inicio y al final, y convierte todo a minúsculas
    texto = texto.strip().lower()

    # Si el texto es un número (entero o decimal, con o sin signo)
    if re.fullmatch(r"[-+]?\d+(\.\d+)?", texto):
        return float(texto)  # Lo convierte a float y lo devuelve

    # Si el texto es una variable con coeficiente, como "x", "2x", "-4.5y", "+z"
    elif re.fullmatch(r"[-+]?\d*(x|y|z)", texto):
        # Extrae solo el coeficiente (todo menos la letra)
        coef = texto[:-1] if texto[-1] in "xyz" else texto

        # Si no hay coeficiente o es un signo, asume 1 o -1
        if coef in ("", "+"):
            return 1.0
        elif coef == "-":
            return -1.0

        # Convierte el coeficiente a número
        return float(coef)

    # Si no se puede interpretar, lanza un error
    raise ValueError("No interpretable")

# ------------------------- FUNCIÓN GLOBAL PARA INTERPRETAR VALORES SYMPY-------------------------
def interpretar_valor_simbolico(texto):
    # Elimina espacios al principio y al final, y convierte todo a minúsculas
    texto = texto.strip().lower()

    # Inserta un "*" entre números y letras (esto es para asegurar que las expresiones sean válidas para sympy)
    # Ejemplo: "3x" se convierte en "3*x", "-4y" en "-4*y"
    texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

    try:
        # Intenta convertir el texto a una expresión simbólica utilizando sympify de sympy
        return sympify(texto)
    except Exception:
        # Si ocurre un error al convertir, lanza una excepción con un mensaje
        raise ValueError("Expresión simbólica no válida")

# ------------------------- FUNCION LIMPIAR POLINOMIOS -------------------------
def limpiar_expresion(texto):
    # Elimina los espacios al principio y al final, y convierte todo a minúsculas
    texto = texto.strip().lower()

    # Inserta un "*" entre números y letras si es necesario (por ejemplo, "3x" se convierte en "3*x")
    texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

    # Reemplaza los "^" con "**" para que sea compatible con la sintaxis de Python (ejemplo: 2^3 -> 2**3)
    texto = texto.replace('^', '**')

    # Devuelve la cadena ya formateada
    return texto