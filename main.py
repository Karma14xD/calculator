import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget,
    QToolButton, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy,
    QHBoxLayout, QSpinBox, QPushButton, QLineEdit, QFrame,QFormLayout,QComboBox
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import re
import numpy as np
from sympy import Matrix,sympify,simplify,symbols,diff,integrate,lambdify

# ------------------------- CLASE BASE PARA SUBMENÚS -------------------------
class SubmenuBase(QWidget):
    def __init__(self, stack=None, menu_widget=None):
        super().__init__()
        self.stack = stack
        self.menu_widget = menu_widget

    def add_back_button(self, layout):
        back_btn = QToolButton()
        back_btn.setText("Volver al Menú")
        back_btn.setIcon(QIcon("imagenes/volver.png"))
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

# ------------------------- CLASE SUBMENÚ MATRICES -------------------------
class SubmenuMatrices(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_resta, go_to_multiplicacion, go_to_determinante, go_to_inversa_matriz, go_to_sistema,menu_widget):
        super().__init__(stack, menu_widget)
        self.go_to_suma = go_to_suma
        self.go_to_resta = go_to_resta
        self.go_to_multiplicacion = go_to_multiplicacion
        self.go_to_determinante = go_to_determinante
        self.go_to_inversa_matriz = go_to_inversa_matriz
        self.go_to_sistema = go_to_sistema
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Operaciones con Matrices")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Suma", "imagenes/suma.png"),
            ("Resta", "imagenes/resta.png"),
            ("Multiplicación", "imagenes/multiplicacion.png"),
            ("Determinante", "imagenes/determinante.png"),
            ("Inversa", "imagenes/inversa.png"),
            ("Resolver Sistema", "imagenes/ecuaciones.png"),
        ]

        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2c3e50;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #34495e;
                }
            """)
            if texto == "Suma":
                btn.clicked.connect(self.go_to_suma)
            elif texto == "Resta":
                btn.clicked.connect(self.go_to_resta)
            elif texto == "Multiplicación":
                btn.clicked.connect(self.go_to_multiplicacion)
            elif texto == "Determinante":
                btn.clicked.connect(self.go_to_determinante)
            elif texto == "Inversa":
                btn.clicked.connect(self.go_to_inversa_matriz)
            elif texto == "Resolver Sistema":
                btn.clicked.connect(self.go_to_sistema)
            else:
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Matrices", f"Operación: {x}"))
            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)
        layout.addSpacing(1)
        self.add_back_button(layout)

# ------------------------- VISTA SUMA MATRICES -------------------------
class VistaSumaMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.matriz_frames = []  # NUEVA LISTA PARA GUARDAR LOS FRAMES

        titulo = QLabel("➕ Suma de Matrices")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(titulo)

        contenedor = QVBoxLayout()
        contenedor.setAlignment(Qt.AlignCenter)

        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        self.spin_matrices = QSpinBox()
        self.spin_matrices.setMinimum(2)
        self.spin_matrices.setStyleSheet(estilo_spin)
        self.spin_filas = QSpinBox()
        self.spin_filas.setMinimum(1)
        self.spin_filas.setStyleSheet(estilo_spin)
        self.spin_columnas = QSpinBox()
        self.spin_columnas.setMinimum(1)
        self.spin_columnas.setStyleSheet(estilo_spin)

        for label_text, spin in [("Cantidad de Matrices:", self.spin_matrices),
                                 ("Cantidad de Filas:", self.spin_filas),
                                 ("Cantidad de Columnas:", self.spin_columnas)]:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            self.controles.addWidget(label, alignment=Qt.AlignCenter)
            self.controles.addWidget(spin, alignment=Qt.AlignCenter)

        contenedor.addLayout(self.controles)

        self.btn_generar = QPushButton("Generar Matrices")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matrices)
        contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid_matrices = QHBoxLayout()
        self.grid_matrices.setSpacing(15)
        contenedor.addLayout(self.grid_matrices)

        self.btn_sumar = QPushButton("Sumar")
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_sumar.clicked.connect(self.realizar_suma)
        contenedor.addWidget(self.btn_sumar, alignment=Qt.AlignCenter)

        self.resultado_grid = QGridLayout()
        contenedor.addLayout(self.resultado_grid)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.layout.addLayout(contenedor)
        self.matriz_inputs = []

    def generar_matrices(self):
        for frame in self.matriz_frames:
            self.grid_matrices.removeWidget(frame)
            frame.deleteLater()
        self.matriz_frames.clear()
        self.matriz_inputs.clear()

        n = self.spin_matrices.value()
        f = self.spin_filas.value()
        c = self.spin_columnas.value()

        for _ in range(n):
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")
            grid = QGridLayout(frame)
            inputs = []
            for i in range(f):
                row_inputs = []
                for j in range(c):
                    input_field = QLineEdit("0")
                    input_field.setAlignment(Qt.AlignCenter)
                    input_field.setFixedWidth(40)
                    input_field.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                    grid.addWidget(input_field, i, j)
                    row_inputs.append(input_field)
                inputs.append(row_inputs)
            self.grid_matrices.addWidget(frame)
            self.matriz_inputs.append(inputs)
            self.matriz_frames.append(frame)

    def interpretar_valor(self, texto):
        texto = texto.strip().lower()
        if re.fullmatch(r"[-+]?\d+(\.\d+)?", texto):
            return float(texto)
        elif re.fullmatch(r"[-+]?\d*(x|y|z)", texto):
            coef = texto[:-1] if texto[-1] in "xyz" else texto
            if coef in ("", "+"):
                return 1.0
            elif coef == "-":
                return -1.0
            return float(coef)
        raise ValueError("No interpretable")

    def realizar_suma(self):
        if len(self.matriz_inputs) < 2:
            QMessageBox.warning(self, "Error", "Debes tener al menos dos matrices para sumar.")
            return

        filas = len(self.matriz_inputs[0])
        columnas = len(self.matriz_inputs[0][0])

        for matriz in self.matriz_inputs:
            if len(matriz) != filas or any(len(row) != columnas for row in matriz):
                QMessageBox.critical(self, "Error", "Todas las matrices deben tener la misma dimensión.")
                return

        resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

        try:
            for matriz in self.matriz_inputs:
                for i in range(filas):
                    for j in range(columnas):
                        texto = matriz[i][j].text().strip()
                        if texto == "":
                            raise ValueError("Campo vacío")
                        valor = self.interpretar_valor(texto)
                        resultado[i][j] += valor
        except Exception:
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(filas):
            for j in range(columnas):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)

# ------------------------- VISTA RESTA MATRICES -------------------------
class VistaRestaMatrices(VistaSumaMatrices):
    def __init__(self, volver_callback):
        super().__init__(volver_callback)
        self.findChild(QLabel).setText("➖ Resta de Matrices")
        self.btn_sumar.setText("Restar")
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.btn_sumar.clicked.disconnect()
        self.btn_sumar.clicked.connect(self.realizar_resta)

    def realizar_resta(self):
        if len(self.matriz_inputs) != 2:
            QMessageBox.warning(self, "Error", "Solo se pueden restar dos matrices.")
            return

        filas = len(self.matriz_inputs[0])
        columnas = len(self.matriz_inputs[0][0])

        for matriz in self.matriz_inputs:
            if len(matriz) != filas or any(len(row) != columnas for row in matriz):
                QMessageBox.critical(self, "Error", "Ambas matrices deben tener la misma dimensión.")
                return

        resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

        try:
            for i in range(filas):
                for j in range(columnas):
                    val1 = self.interpretar_valor(self.matriz_inputs[0][i][j].text())
                    val2 = self.interpretar_valor(self.matriz_inputs[1][i][j].text())
                    resultado[i][j] = val1 - val2
        except Exception:
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(filas):
            for j in range(columnas):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)

# ------------------------- FUNCIÓN GLOBAL PARA INTERPRETAR VALORES -------------------------
def interpretar_valor(texto):
    texto = texto.strip().lower()
    if re.fullmatch(r"[-+]?\d+(\.\d+)?", texto):
        return float(texto)
    elif re.fullmatch(r"[-+]?\d*(x|y|z)", texto):
        coef = texto[:-1] if texto[-1] in "xyz" else texto
        if coef in ("", "+"):
            return 1.0
        elif coef == "-":
            return -1.0
        return float(coef)
    raise ValueError("No interpretable")

# ------------------------- FUNCIÓN GLOBAL PARA INTERPRETAR VALORES SYMPY-------------------------
def interpretar_valor_simbolico(texto):
    texto = texto.strip().lower()
    # Inserta * entre número y letra: 3x → 3*x, -4y → -4*y
    texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
    try:
        return sympify(texto)
    except Exception:
        raise ValueError("Expresión simbólica no válida")

# ------------------------- FUNCION LIMPIAR POLINOMIOS -------------------------
def limpiar_expresion(texto):
    texto = texto.strip().lower()
    texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
    texto = texto.replace('^', '**')
    return texto

# ------------------------- VISTA MULTIPLICACIÓN MATRICES -------------------------
class VistaMultiplicacionMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("✖️ Multiplicación de Matrices")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filasA = QSpinBox(); self.filasA.setMinimum(1)
        self.colsA = QSpinBox(); self.colsA.setMinimum(1)
        self.filasB = QSpinBox(); self.filasB.setMinimum(1)
        self.colsB = QSpinBox(); self.colsB.setMinimum(1)

        estilo_spin = "QSpinBox { background: white; font-size: 14px; padding: 4px; }"
        for spin in [self.filasA, self.colsA, self.filasB, self.colsB]:
            spin.setStyleSheet(estilo_spin)

        for label, spin in [("Filas A:", self.filasA), ("Columnas A:", self.colsA),
                            ("Filas B:", self.filasB), ("Columnas B:", self.colsB)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Matrices")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matrices)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QHBoxLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.grid)

        self.btn_multiplicar = QPushButton("Multiplicar")
        self.btn_multiplicar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_multiplicar.clicked.connect(self.realizar_multiplicacion)
        self.layout.addWidget(self.btn_multiplicar, alignment=Qt.AlignCenter)

        self.resultado_grid = QGridLayout()
        self.layout.addLayout(self.resultado_grid)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def generar_matrices(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        self.matrices = []

        fA, cA, fB, cB = self.filasA.value(), self.colsA.value(), self.filasB.value(), self.colsB.value()
        if cA != fB:
            QMessageBox.critical(self, "Error", "Columnas de A deben coincidir con filas de B.")
            return

        for dims in [(fA, cA), (fB, cB)]:
            frame = QFrame()
            frame.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 6px;")
            grid = QGridLayout(frame)
            matriz = []
            for i in range(dims[0]):
                fila = []
                for j in range(dims[1]):
                    campo = QLineEdit("0")
                    campo.setAlignment(Qt.AlignCenter)
                    campo.setFixedWidth(40)
                    campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                    grid.addWidget(campo, i, j)
                    fila.append(campo)
                matriz.append(fila)
            self.grid.addWidget(frame)
            self.matrices.append(matriz)

    def realizar_multiplicacion(self):
        if len(self.matrices) != 2:
            QMessageBox.warning(self, "Error", "Debes generar dos matrices primero.")
            return

        A, B = self.matrices
        try:
            matA = [[interpretar_valor(cell.text()) for cell in row] for row in A]
            matB = [[interpretar_valor(cell.text()) for cell in row] for row in B]
        except ValueError:
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        fA, cB, cA = len(matA), len(matB[0]), len(matA[0])
        resultado = [[0] * cB for _ in range(fA)]
        for i in range(fA):
            for j in range(cB):
                for k in range(cA):
                    resultado[i][j] += matA[i][k] * matB[k][j]

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(fA):
            for j in range(cB):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)

# ------------------------- VISTA DETERMINANTE MATRICES -------------------------
class VistaDeterminanteMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("🧮 Determinante de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filas = QSpinBox(); self.filas.setMinimum(1); self.filas.setValue(2)
        self.columnas = QSpinBox(); self.columnas.setMinimum(1); self.columnas.setValue(2)

        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matriz)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.layout.addLayout(self.grid)

        self.btn_determinante = QPushButton("Calcular Determinante")
        self.btn_determinante.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_determinante.clicked.connect(self.calcular_determinante)
        self.layout.addWidget(self.btn_determinante, alignment=Qt.AlignCenter)

        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 10px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.inputs = []

    def generar_matriz(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        self.inputs.clear()

        f, c = self.filas.value(), self.columnas.value()
        for i in range(f):
            fila = []
            for j in range(c):
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)
                campo.setFixedWidth(40)
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)
                fila.append(campo)
            self.inputs.append(fila)

    def calcular_determinante(self):
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular el determinante.")
            return

        try:
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            determinante = Matrix(matriz).det()
            self.resultado.setText(f"Determinante: {determinante}")
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean expresiones simbólicas válidas.")


# ------------------------- VISTA INVERSA MATRICES -------------------------
class VistaInversaMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("🔄 Inversa de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filas = QSpinBox(); self.filas.setMinimum(1); self.filas.setValue(2)
        self.columnas = QSpinBox(); self.columnas.setMinimum(1); self.columnas.setValue(2)

        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_matriz)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.layout.addLayout(self.grid)

        self.btn_inversa = QPushButton("Calcular Inversa")
        self.btn_inversa.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_inversa.clicked.connect(self.calcular_inversa)
        self.layout.addWidget(self.btn_inversa, alignment=Qt.AlignCenter)

        self.resultado_grid = QGridLayout()
        self.resultado_grid.setSpacing(6)
        self.layout.addLayout(self.resultado_grid)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.inputs = []

    def generar_matriz(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        self.inputs.clear()

        f, c = self.filas.value(), self.columnas.value()
        for i in range(f):
            fila = []
            for j in range(c):
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)
                campo.setFixedWidth(40)
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)
                fila.append(campo)
            self.inputs.append(fila)

    def calcular_inversa(self):
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular la inversa.")
            return

        try:
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            M = Matrix(matriz)
            if M.det() == 0:
                QMessageBox.critical(self, "Error", "La matriz no tiene inversa (determinante = 0).")
                return
            inversa = M.inv()
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean numéricos o simbólicos válidos.")
            return

        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        for i in range(inversa.rows):
            for j in range(inversa.cols):
                res = QLineEdit(str(inversa[i, j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)


# ------------------------- VISTA SISTEMA DE ECUACIONES MATRICES -------------------------
class VistaSistemaEcuaciones(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        titulo = QLabel("🧩 Resolver Sistema de Ecuaciones")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(titulo)

        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        self.filas = QSpinBox()
        self.filas.setMinimum(2)
        self.filas.setValue(2)
        self.filas.setStyleSheet("QSpinBox { background-color: white; font-size: 14px; padding: 4px; }")

        label = QLabel("Número de ecuaciones:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")

        controles.addWidget(label)
        controles.addWidget(self.filas)
        self.layout.addLayout(controles)

        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_campos)
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.layout.addLayout(self.grid)

        self.btn_resolver = QPushButton("Resolver Sistema")
        self.btn_resolver.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_resolver.clicked.connect(self.resolver_sistema)
        self.layout.addWidget(self.btn_resolver, alignment=Qt.AlignCenter)

        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("font-size: 18px; color: #2c3e50; margin-top: 10px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.inputs_A = []
        self.inputs_B = []

    def generar_campos(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()
        self.inputs_A.clear()
        self.inputs_B.clear()

        n = self.filas.value()
        for i in range(n):
            fila_A = []
            for j in range(n):
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)
                campo.setFixedWidth(40)
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)
                fila_A.append(campo)
            self.inputs_A.append(fila_A)

            campo_b = QLineEdit("0")
            campo_b.setAlignment(Qt.AlignCenter)
            campo_b.setFixedWidth(40)
            campo_b.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
            self.grid.addWidget(campo_b, i, n)
            self.inputs_B.append(campo_b)

    def resolver_sistema(self):
        try:
            A = [[interpretar_valor_simbolico(cell.text()) for cell in fila] for fila in self.inputs_A]
            B = [interpretar_valor_simbolico(cell.text()) for cell in self.inputs_B]
            M = Matrix(A)
            v = Matrix(B)
            if M.det() == 0:
                self.resultado.setText("No tiene solución única (determinante = 0).")
                return
            solucion = M.inv() * v
            resultado_texto = "<b>Solución:</b><br>" + "<br>".join([f"x{i+1} = {valor}" for i, valor in enumerate(solucion)])
            self.resultado.setText(resultado_texto)
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que los valores sean numéricos o simbólicos válidos.")


# ------------------------- CLASE SUBMENÚ POLINOMIOS -------------------------
class SubmenuPolinomios(SubmenuBase):
    def __init__(self, stack, go_to_suma,go_to_multiplicacion, go_to_derivacion,go_to_integracion,go_to_evaluacion, menu_widget):
        super().__init__(stack, menu_widget)
        self.go_to_suma = go_to_suma
        self.go_to_multiplicacion = go_to_multiplicacion
        self.go_to_derivacion = go_to_derivacion
        self.go_to_integracion = go_to_integracion
        self.go_to_evaluacion = go_to_evaluacion
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel("Operaciones con Polinomios")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Suma", "imagenes/suma.png"),
            ("Multiplicación", "imagenes/multiplicacion.png"),
            ("Derivación", "imagenes/derivada.png"),
            ("Integración", "imagenes/integral.png"),
            ("Evaluación", "imagenes/evaluar.png"),
        ]

        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2c3e50;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #34495e;
                }
            """)
            if texto == "Suma":
                btn.clicked.connect(self.go_to_suma)
            elif texto == "Multiplicación":
                btn.clicked.connect(self.go_to_multiplicacion)
            elif texto == "Derivación":
                btn.clicked.connect(self.go_to_derivacion)
            elif texto == "Integración":
                btn.clicked.connect(self.go_to_integracion)
            elif texto == "Evaluación":
                btn.clicked.connect(self.go_to_evaluacion)
            else:
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Polinomios", f"Operación: {x}"))

            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)
        layout.addSpacing(1)
        self.add_back_button(layout)

# ------------------------- CLASE VISTA SUMA POLINOMIOS -------------------------
class VistaSumaPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("➕ Suma de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.contenedor = QVBoxLayout()
        self.contenedor.setAlignment(Qt.AlignCenter)

        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setStyleSheet(estilo_spin)

        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)

        self.contenedor.addLayout(self.controles)

        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_campos)
        self.contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.campos_layout = QFormLayout()
        self.contenedor.addLayout(self.campos_layout)

        self.btn_sumar = QPushButton("Sumar Polinomios")
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_sumar.clicked.connect(self.sumar_polinomios)
        self.contenedor.addWidget(self.btn_sumar, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.contenedor.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.layout.addLayout(self.contenedor)
        self.campos = []

    def generar_campos(self):
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Polinomio {i+1} (ej: x^2 + 3x - 4)")
            campo.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Polinomio {i+1}:", campo)
            self.campos.append(campo)

    def sumar_polinomios(self):
        try:
            suma = sum(sympify(limpiar_expresion(campo.text())) for campo in self.campos)
            self.resultado.setText(str(simplify(suma)))
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que todos los polinomios sean expresiones válidas.")


#--------------- CLASE VISTA MULTIPLICACION POLINOMIOS-----------
class VistaMultiplicacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("✖ Multiplicación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.contenedor = QVBoxLayout()
        self.contenedor.setAlignment(Qt.AlignCenter)

        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)
        self.spin_cantidad.setStyleSheet(estilo_spin)

        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)
        self.contenedor.addLayout(self.controles)

        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        self.btn_generar.clicked.connect(self.generar_campos)
        self.contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        self.campos_layout = QFormLayout()
        self.contenedor.addLayout(self.campos_layout)

        self.btn_multiplicar = QPushButton("Multiplicar Polinomios")
        self.btn_multiplicar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.btn_multiplicar.clicked.connect(self.multiplicar_polinomios)
        self.contenedor.addWidget(self.btn_multiplicar, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.contenedor.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.btn_volver.clicked.connect(self.volver_callback)
        self.contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.layout.addLayout(self.contenedor)
        self.campos = []

    def generar_campos(self):
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Polinomio {i+1} (ej: x^2 + 3x - 4)")
            campo.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Polinomio {i+1}:", campo)
            self.campos.append(campo)

    def multiplicar_polinomios(self):
        try:
            producto = sympify("1")
            for campo in self.campos:
                texto = campo.text().strip().lower()
                texto = re.sub(r"(?<=\d)(?=[a-z])", "*", texto)  # 3x → 3*x
                producto *= sympify(texto)
            self.resultado.setText(str(simplify(producto)))
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica que todos los polinomios sean expresiones válidas.")

# ------------------------- CLASE VISTA DERIVACION POLINOMIOS -------------------------
class VistaDerivacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("📐 Derivación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        contenedor = QVBoxLayout()
        contenedor.setAlignment(Qt.AlignCenter)

        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)

        label1 = QLabel("Ingrese el polinomio:")
        label1.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^3 + 2x^2 + 5")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")

        label2 = QLabel("Variable:")
        label2.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.variable_input = QLineEdit()
        self.variable_input.setPlaceholderText("Variable (ej: x)")
        self.variable_input.setMaxLength(1)
        self.variable_input.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")

        self.controles.addWidget(label1, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.entrada, alignment=Qt.AlignCenter)
        self.controles.addWidget(label2, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.variable_input, alignment=Qt.AlignCenter)

        contenedor.addLayout(self.controles)

        self.boton = QPushButton("Derivar")
        self.boton.clicked.connect(self.derivar)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        contenedor.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        contenedor.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.layout.addLayout(contenedor)

    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var_texto = self.variable_input.text().strip().lower()

        if not texto or not var_texto:
            QMessageBox.warning(self, "Error", "Debes ingresar un polinomio y una variable.")
            return

        if not re.fullmatch(r"[a-z]", var_texto):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra (ej: x, y, z).")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)  # convierte 3x → 3*x
            var = symbols(var_texto)
            polinomio = sympify(texto)

            if var not in polinomio.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var_texto}' no está en el polinomio.")
                return

            derivada = diff(polinomio, var)
            self.resultado.setText(str(derivada))
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 1")


# ------------------------- CLASE VISTA INTEGRACIÓN POLINOMIOS -------------------------
class VistaIntegracionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("∫ Integración de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.variable)

        self.boton = QPushButton("Integrar")
        self.boton.clicked.connect(self.integrar)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def integrar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            integral = integrate(expr, simb)
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE VISTA EVALUACIÓN POLINOMIOS -------------------------
class VistaEvaluacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("📊 Evaluación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.variable)

        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor numérico (ej: 2)")
        self.valor.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.valor)

        self.boton = QPushButton("Evaluar")
        self.boton.clicked.connect(self.evaluar)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
        """)
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def evaluar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()
        val = self.valor.text().strip()

        if not texto or not var or not val:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            val = float(val)
        except ValueError:
            QMessageBox.warning(self, "Error", "El valor de evaluación debe ser un número.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            resultado = expr.subs(simb, val)
            self.resultado.setText(str(resultado))
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE SUBMENÚSVECTORES -------------------------
class SubmenuVectores(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_resta, go_to_magnitud, go_to_producto_punto,go_to_producto_cruzado, menu_widget):
        super().__init__(stack, menu_widget)
        self.go_to_suma = go_to_suma
        self.go_to_resta = go_to_resta
        self.go_to_magnitud = go_to_magnitud
        self.go_to_producto_punto = go_to_producto_punto
        self.go_to_producto_cruzado = go_to_producto_cruzado
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Operaciones con Vectores")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b3f42;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Suma", "imagenes/suma.png"),
            ("Resta", "imagenes/resta.png"),
            ("Magnitud", "imagenes/magnitud.png"),
            ("Producto Punto", "imagenes/punto.png"),
            ("Producto Cruzado", "imagenes/cruzado.png"),
        ]

        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #3b3f42;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #4d5257;
                }
            """)
            if texto == "Suma":
                btn.clicked.connect(self.go_to_suma)
            elif texto == "Resta":
                btn.clicked.connect(self.go_to_resta)
            elif texto == "Magnitud":
                btn.clicked.connect(self.go_to_magnitud)
            elif texto == "Producto Punto":
                btn.clicked.connect(self.go_to_producto_punto)
            elif texto == "Producto Cruzado":
                btn.clicked.connect(self.go_to_producto_cruzado)
            else:
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Vectores", f"Operación: {x}"))
            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)

        layout.addSpacing(30)

        volver_btn = QToolButton()
        volver_btn.setText("Volver al Menú")
        volver_btn.setIcon(QIcon("imagenes/salir.png"))
        volver_btn.setIconSize(QSize(24, 24))
        volver_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        volver_btn.setStyleSheet("""
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
        volver_btn.clicked.connect(self.go_back)
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

# ------------------------- CLASE VISTA SUMA VECTORES -------------------------
class VistaSumaVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("➕ Suma de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.selector_layout = QVBoxLayout()

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)
        self.spin_cantidad.setStyleSheet("background-color: white; padding: 4px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.selector_layout.addWidget(QLabel("Cantidad de Vectores:"))
        self.selector_layout.addWidget(self.spin_cantidad)

        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.clicked.connect(self.generar_campos)
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.selector_layout.addWidget(self.btn_generar)
        self.layout.addLayout(self.selector_layout)

        self.campos_layout = QFormLayout()
        self.layout.addLayout(self.campos_layout)

        self.btn_sumar = QPushButton("Sumar Vectores")
        self.btn_sumar.clicked.connect(self.sumar_vectores)
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.layout.addWidget(self.btn_sumar)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.campos = []

    def generar_campos(self):
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Vector {i+1} (ej: 1,2,3 o 4,+5,-6)")
            campo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Vector {i+1}:", campo)
            self.campos.append(campo)

    def sumar_vectores(self):
        try:
            vectores = []
            for campo in self.campos:
                texto = campo.text().strip().replace(" ", "")
                vector = self.convertir_a_numerico(texto)
                vectores.append(vector)

            longitud = len(vectores[0])
            for vector in vectores:
                if len(vector) != longitud:
                    raise ValueError("Todos los vectores deben tener la misma cantidad de componentes.")

            suma = [sum(x) for x in zip(*vectores)]
            self.resultado.setText(str(suma))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al sumar los vectores: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

# ------------------------- CLASE VISTA RESTA VECTORES -------------------------
class VistaRestaVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("➖ Resta de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.selector_layout = QVBoxLayout()

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)
        self.spin_cantidad.setStyleSheet("background-color: white; padding: 4px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.selector_layout.addWidget(QLabel("Cantidad de Vectores:"))
        self.selector_layout.addWidget(self.spin_cantidad)

        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.clicked.connect(self.generar_campos)
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.selector_layout.addWidget(self.btn_generar)

        self.layout.addLayout(self.selector_layout)

        self.campos_layout = QFormLayout()
        self.layout.addLayout(self.campos_layout)

        self.btn_rest = QPushButton("Restar Vectores")
        self.btn_rest.clicked.connect(self.restar_vectores)
        self.btn_rest.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        self.layout.addWidget(self.btn_rest)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        self.campos = []

    def generar_campos(self):
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Vector {i+1} (ej: 1,2,3 o 4,+5,-6)")
            campo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Vector {i+1}:", campo)
            self.campos.append(campo)

    def restar_vectores(self):
        try:
            vectores = []
            for campo in self.campos:
                texto = campo.text().strip().replace(" ", "")
                vector = self.convertir_a_numerico(texto)
                vectores.append(vector)

            longitud = len(vectores[0])
            for vector in vectores:
                if len(vector) != longitud:
                    raise ValueError("Todos los vectores deben tener la misma cantidad de componentes.")

            resta = vectores[0]
            for v in vectores[1:]:
                resta = [a - b for a, b in zip(resta, v)]

            self.resultado.setText(str(resta))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al restar los vectores: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False


# ------------------------- CLASE VISTA MAGNITUD VECTORES -------------------------
class VistaMagnitudVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("🔢 Magnitud de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: 3,4 o 1,2,3")
        self.entrada.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        self.boton = QPushButton("Calcular Magnitud")
        self.boton.clicked.connect(self.calcular_magnitud)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def calcular_magnitud(self):
        try:
            texto = self.entrada.text().strip().replace(" ", "")
            vector = self.convertir_a_numerico(texto)
            magnitud = sum([x ** 2 for x in vector]) ** 0.5
            self.resultado.setText(f"MAGNITUD: {magnitud}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular la magnitud: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False


# ------------------------- CLASE VISTA PRODUCTO PUNTO VECTORES -------------------------
class VistaProductoPuntoVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("⚡ Producto Punto de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada_vector1 = QLineEdit()
        self.entrada_vector1.setPlaceholderText("Vector 1 (ej: 1, 2, 3)")
        self.entrada_vector1.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector1)

        self.entrada_vector2 = QLineEdit()
        self.entrada_vector2.setPlaceholderText("Vector 2 (ej: 4, 5, 6)")
        self.entrada_vector2.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector2)

        self.boton = QPushButton("Calcular Producto Punto")
        self.boton.clicked.connect(self.calcular_producto_punto)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def calcular_producto_punto(self):
        try:
            texto_vector1 = self.entrada_vector1.text().strip().replace(" ", "")
            texto_vector2 = self.entrada_vector2.text().strip().replace(" ", "")

            vector1 = self.convertir_a_numerico(texto_vector1)
            vector2 = self.convertir_a_numerico(texto_vector2)

            if len(vector1) != len(vector2):
                raise ValueError("Los vectores deben tener la misma cantidad de componentes.")

            producto_punto = sum(x * y for x, y in zip(vector1, vector2))
            self.resultado.setText(f"Producto Punto: {producto_punto}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular el producto punto: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

# ------------------------- CLASE VISTA PRODUCTO CRUZADO VECTORES -------------------------
class VistaProductoCruzadoVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("✖️ Producto Cruzado de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada1 = QLineEdit()
        self.entrada1.setPlaceholderText("Vector 1 (ej: 1, 2, 3)")
        self.entrada1.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada1)

        self.entrada2 = QLineEdit()
        self.entrada2.setPlaceholderText("Vector 2 (ej: 4, -5, 6)")
        self.entrada2.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada2)

        self.boton = QPushButton("Calcular Producto Cruzado")
        self.boton.clicked.connect(self.calcular_producto_cruzado)
        self.boton.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 13px;
                padding: 8px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def calcular_producto_cruzado(self):
        try:
            vector1_texto = self.entrada1.text().strip().replace(" ", "")
            vector2_texto = self.entrada2.text().strip().replace(" ", "")

            vector1 = self.convertir_a_numerico(vector1_texto)
            vector2 = self.convertir_a_numerico(vector2_texto)

            if len(vector1) != 3 or len(vector2) != 3:
                raise ValueError("Ambos vectores deben tener exactamente 3 componentes.")

            producto_cruzado = self.producto_cruzado(vector1, vector2)
            self.resultado.setText(str(producto_cruzado))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al calcular el producto cruzado: {str(e)}")

    def convertir_a_numerico(self, texto):
        try:
            elementos = texto.split(",")
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))
            return vector
        except Exception:
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def producto_cruzado(self, v1, v2):
        i = v1[1] * v2[2] - v1[2] * v2[1]
        j = v1[2] * v2[0] - v1[0] * v2[2]
        k = v1[0] * v2[1] - v1[1] * v2[0]
        return [i, -j, k]


# ------------------------- CLASE SUBMENÚS GRAFICAS -------------------------
class SubmenuGraficas(SubmenuBase):
    def __init__(self, stack,go_to_2d, go_to_3d, menu_widget):
        super().__init__(stack, menu_widget)
        self.go_to_2d = go_to_2d
        self.go_to_3d = go_to_3d
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Gráficas 2D y 3D")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #5d6d7e;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Función 2D", "imagenes/2d.png"),
            ("Curva 3D", "imagenes/3d.png")
        ]

        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #5d6d7e;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #85929e;
                }
            """)
            if texto == "Función 2D":
                btn.clicked.connect(self.go_to_2d)
            elif texto == "Curva 3D":
                btn.clicked.connect(self.go_to_3d)
            else:           
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Gráficas", f"Operación: {x}"))
            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)
        layout.addSpacing(30)

        volver_btn = QToolButton()
        volver_btn.setText("Volver al Menú")
        volver_btn.setIcon(QIcon("imagenes/salir.png"))
        volver_btn.setIconSize(QSize(24, 24))
        volver_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        volver_btn.setStyleSheet("""
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
        volver_btn.clicked.connect(self.go_back)
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

#------------------------- CLASE VISTA GRAFICA 2D -------------------------
class VistaGrafica2D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("📊 Gráfica 2D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + 2x + 1)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x (ej: -10,10)")
        self.rango_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.rango_input)

        self.btn_graficar = QPushButton("Graficar")
        self.btn_graficar.clicked.connect(self.graficar)
        self.btn_graficar.setStyleSheet("padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;")
        self.layout.addWidget(self.btn_graficar)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

        # Para mostrar la gráfica
        self.figure = plt.figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def graficar(self):
        try:
            funcion = self.funcion_input.text().strip()
            rango = self.rango_input.text().strip()

            # Validar rango
            if "," not in rango:
                raise ValueError("El rango debe tener el formato: -5,5")

            partes = rango.split(",")
            x_min = float(partes[0])
            x_max = float(partes[1])

            # Procesar expresión
            funcion = re.sub(r'(?<=\d)(?=x)', '*', funcion)  # 3x -> 3*x
            x = symbols('x')
            expr = sympify(funcion)
            f = lambdify(x, expr, 'numpy')

            # Crear valores y evaluar
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = f(x_vals)

            # Limpiar gráfica anterior
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x_vals, y_vals, label=str(expr))
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Gráfica de {funcion}")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

#-------------------------- CLASE VISTA GRAFICA 3D -------------------------
class VistaGrafica3D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("\ud83d\udcca Gráfica 3D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + y^2)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x, y (ej: -10,10)")
        self.rango_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.rango_input)

        self.btn_graficar = QPushButton("Graficar")
        self.btn_graficar.clicked.connect(self.graficar)
        self.btn_graficar.setStyleSheet("padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;")
        self.layout.addWidget(self.btn_graficar)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    def graficar(self):
        try:
            funcion = self.funcion_input.text().strip().lower().replace("^", "**")
            rango = self.rango_input.text().strip()

            partes = rango.split(",")
            if len(partes) != 2:
                raise ValueError("El rango debe tener dos números separados por coma.")

            x_min = float(partes[0])
            x_max = float(partes[1])
            y_min = x_min
            y_max = x_max

            x = np.linspace(x_min, x_max, 100)
            y = np.linspace(y_min, y_max, 100)
            X, Y = np.meshgrid(x, y)

            x_sym, y_sym = symbols("x y")
            expr = sympify(funcion)
            f = lambdify((x_sym, y_sym), expr, "numpy")
            Z = f(X, Y)

            self.figure.clear()
            ax = self.figure.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
            ax.set_title(f"Gráfica de {funcion}")
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

# ------------------------- CLASE SUBMENÚ CÁLCULO -------------------------
class SubmenuCalculo(SubmenuBase):
    def __init__(self, stack,go_to_derivada, go_to_integral_indefinida, go_to_integral_definida, menu_widget):
        super().__init__(stack, menu_widget)
        self.go_to_derivada = go_to_derivada
        self.go_to_integral_indefinida = go_to_integral_indefinida
        self.go_to_integral_definida = go_to_integral_definida
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Operaciones de Cálculo")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f618d;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        operaciones = [
            ("Derivada", "imagenes/derivada.png"),
            ("Integral Indefinida", "imagenes/integral.png"),
            ("Integral Definida", "imagenes/definida.png")
        ]

        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #1f618d;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    border-radius: 10px;
                    padding: 15px;
                }
                QToolButton:hover {
                    background-color: #2980b9;
                }
            """)
            if texto == "Integral Definida":
                btn.clicked.connect(self.go_to_integral_definida)
            elif texto == "Integral Indefinida":
                btn.clicked.connect(self.go_to_integral_indefinida)
            elif texto == "Derivada":
                btn.clicked.connect(self.go_to_derivada)
            else:
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Cálculo", f"Operación: {x}"))

            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)
        layout.addSpacing(30)

        volver_btn = QToolButton()
        volver_btn.setText("Volver al Menú")
        volver_btn.setIcon(QIcon("imagenes/salir.png"))
        volver_btn.setIconSize(QSize(24, 24))
        volver_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        volver_btn.setStyleSheet("""
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
        volver_btn.clicked.connect(self.go_back)
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

# ------------------------- CLASE VISTA INTEGRAL DEFINIDA -------------------------
class VistaIntegralDefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("∫ Integral Definida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        self.limite_inferior = QLineEdit()
        self.limite_inferior.setPlaceholderText("Límite inferior (ej: 0)")
        self.limite_inferior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_inferior)

        self.limite_superior = QLineEdit()
        self.limite_superior.setPlaceholderText("Límite superior (ej: 5)")
        self.limite_superior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_superior)

        self.boton = QPushButton("Calcular Integral Definida")
        self.boton.clicked.connect(self.integrar_definida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #3498db; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    def integrar_definida(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()
        inferior = self.limite_inferior.text().strip()
        superior = self.limite_superior.text().strip()

        if not texto or not var or not inferior or not superior:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        if not re.fullmatch(r"[-+]?\d+(\.\d+)?", inferior) or not re.fullmatch(r"[-+]?\d+(\.\d+)?", superior):
            QMessageBox.warning(self, "Error", "Los límites deben ser números reales válidos.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)  # 3x -> 3*x
            expr = sympify(texto)
            simb = symbols(var)
            a = float(inferior)
            b = float(superior)
            integral_definida = integrate(expr, (simb, a, b))
            self.resultado.setText(str(integral_definida))
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE VISTA INTEGRAL INDEFINIDA -------------------------
class VistaIntegralIndefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("∫ Integral Indefinida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        self.boton = QPushButton("Integrar")
        self.boton.clicked.connect(self.integrar_indefinida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    def integrar_indefinida(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            integral = integrate(expr, simb)
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE VISTA DERIVACIÓN POLINOMIOS -------------------------
class VistaDerivacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        self.titulo = QLabel("📐 Derivación")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: sin(x) + ln(x^2) + x^3")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        self.boton = QPushButton("Derivar")
        self.boton.clicked.connect(self.derivar)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #2980b9; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)  # convierte 3x → 3*x
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            derivada = diff(expr, simb)
            self.resultado.setText(str(derivada))
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 1")

#-------------------------------- CLASE VISTA ACERCA DE -------------------------
class AcercaDe(SubmenuBase):
    def __init__(self, stack, menu_widget):
        super().__init__(stack, menu_widget)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("font-family: 'Segoe UI'; background-color: #f0f3f4;")

        titulo = QLabel("📘 Acerca del Proyecto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(titulo)

        # Cuadro de descripción del proyecto
        cuadro_proyecto = QFrame()
        cuadro_proyecto.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        proyecto_layout = QVBoxLayout(cuadro_proyecto)
        descripcion = QLabel("""
            <p style="font-size: 16px; color: #2c3e50;">
            Esta <b>Calculadora Científica Interactiva</b> fue desarrollada como una herramienta educativa 
            completa que permite al usuario realizar operaciones avanzadas como el manejo de 
            <i>matrices, vectores, polinomios, derivadas, integrales</i> y representación gráfica en 2D y 3D.<br><br>
            El propósito principal es facilitar el aprendizaje de conceptos matemáticos de forma visual y práctica.
            </p>
        """)
        descripcion.setWordWrap(True)
        proyecto_layout.addWidget(descripcion)
        layout.addWidget(cuadro_proyecto)

        # Cuadro de información personal
        cuadro_autor = QFrame()
        cuadro_autor.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #7f8c8d;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        autor_layout = QVBoxLayout(cuadro_autor)
        info = QLabel("""
            <p style="font-size: 16px; color: #34495e;">
            <b>Autor:</b> ADAN ALI ESCANDON ROCA<br>
            <b>Carrera:</b> Ingeniería en Software<br>
            <b>Facultad:</b> Facultad de Ingeniería<br>
            <b>Universidad:</b> Universidad Estatal de Milagro<br>
            <b>Semestre:</b> Sexto<br>
            <b>Materia:</b> Modelos matematicos y simulación de software<br>
            <b>Año:</b> Abril 2025 - Julio 2025<br>
            </p>
        """)
        info.setAlignment(Qt.AlignCenter)
        autor_layout.addWidget(info)
        layout.addWidget(cuadro_autor)

        # Botón de volver
        volver_btn = QPushButton("Volver al Menú Principal")
        volver_btn.clicked.connect(self.go_back)
        volver_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)



# ------------------------- MÉTODO PARA VISTA PRINCIPAL -------------------------
class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")
        self.setGeometry(300, 50, 800, 600)
        self.stack = QStackedWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.menu_widget = QWidget()
        self.stack.addWidget(self.menu_widget)

        self.vista_suma_matrices = VistaSumaMatrices(self.volver_a_matrices)
        self.vista_resta_matrices = VistaRestaMatrices(self.volver_a_matrices)
        self.vista_multiplicacion = VistaMultiplicacionMatrices(self.volver_a_matrices)
        self.vista_determinante = VistaDeterminanteMatrices(self.volver_a_matrices)
        self.vista_inversa = VistaInversaMatrices(self.volver_a_matrices)
        self.vista_sistema = VistaSistemaEcuaciones(self.volver_a_matrices)

        self.stack.addWidget(self.vista_suma_matrices)
        self.stack.addWidget(self.vista_resta_matrices)
        self.stack.addWidget(self.vista_multiplicacion)
        self.stack.addWidget(self.vista_determinante)
        self.stack.addWidget(self.vista_inversa)
        self.stack.addWidget(self.vista_sistema)

        self.vista_suma_polinomios = VistaSumaPolinomios(self.volver_a_polinomios)
        self.vista_multiplicacion_polinomios = VistaMultiplicacionPolinomios(self.volver_a_polinomios)
        self.vista_derivacion_polinomios = VistaDerivacionPolinomios(self.volver_a_polinomios)
        self.vista_integracion_polinomios = VistaIntegracionPolinomios(self.volver_a_polinomios)
        self.vista_evaluacion_polinomios = VistaEvaluacionPolinomios(self.volver_a_polinomios)

        self.stack.addWidget(self.vista_suma_polinomios)
        self.stack.addWidget(self.vista_multiplicacion_polinomios)
        self.stack.addWidget(self.vista_derivacion_polinomios)
        self.stack.addWidget(self.vista_integracion_polinomios)
        self.stack.addWidget(self.vista_evaluacion_polinomios)

        self.vista_suma_vectores = VistaSumaVectores(self.volver_a_vectores)
        self.vista_resta_vectores = VistaRestaVectores(self.volver_a_vectores)
        self.vista_magnitud_vectores = VistaMagnitudVectores(self.volver_a_vectores)
        self.VistaProductoPuntoVectores = VistaProductoPuntoVectores(self.volver_a_vectores)
        self.vista_producto_cruz_vectores = VistaProductoCruzadoVectores(self.volver_a_vectores)

        
        self.stack.addWidget(self.vista_suma_vectores)
        self.stack.addWidget(self.vista_resta_vectores)
        self.stack.addWidget(self.vista_magnitud_vectores)
        self.stack.addWidget(self.VistaProductoPuntoVectores)
        self.stack.addWidget(self.vista_producto_cruz_vectores)
        
        self.vista_grafica_2d = VistaGrafica2D(self.volver_a_graficas)
        self.vista_grafica_3d = VistaGrafica3D(self.volver_a_graficas)

        self.stack.addWidget(self.vista_grafica_2d)
        self.stack.addWidget(self.vista_grafica_3d)

        self.vista_derivada = VistaDerivacionPolinomios(self.volver_a_calculo)
        self.vista_integral_indefinida = VistaIntegralIndefinida(self.volver_a_calculo)
        self.vista_integral_definida = VistaIntegralDefinida(self.volver_a_calculo)

        self.stack.addWidget(self.vista_derivada)
        self.stack.addWidget(self.vista_integral_indefinida)
        self.stack.addWidget(self.vista_integral_definida)

        self.vista_acercade = AcercaDe(self.stack, self.menu_widget)
        self.stack.addWidget(self.vista_acercade)



        self.submenu_matrices = SubmenuMatrices(
            self.stack,
            self.ir_a_suma_matrices,
            self.ir_a_resta_matrices,
            self.ir_a_multiplicacion_matrices,
            self.ir_a_determinante_matrices,
            self.ir_a_inversa_matrices,
            self.ir_a_sistema_matrices,

            self.menu_widget
        )
        self.stack.addWidget(self.submenu_matrices)

        self.submenu_polinomios = SubmenuPolinomios(
            self.stack,
            self.ir_a_suma_polinomios,
            self.ir_a_multiplicacion_polinomios,
            self.ir_a_derivacion_polinomios,
            self.ir_a_integracion_polinomios,
            self.ir_a_evaluacion_polinomios,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_polinomios)

        self.submenu_vectores = SubmenuVectores(
            self.stack,
            self.ir_a_suma_vectores,
            self.ir_a_resta_vectores,
            self.ir_a_magnitud_vectores,
            self.ir_a_producto_punto_vectores,
            self.ir_a_producto_cruzado_vectores,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_vectores)

        self.submenu_graficas = SubmenuGraficas(
            self.stack,
            self.ir_a_grafica_2d,
            self.ir_a_grafica_3d,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_graficas)

        self.submenu_calculo = SubmenuCalculo(
            self.stack,
            self.ir_a_derivada,
            self.ir_a_integral_indefinida,
            self.ir_a_integral_definida,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_calculo)


        self.init_menu()

    def init_menu(self):
        layout = QVBoxLayout(self.menu_widget)
        title = QLabel("Calculadora Científica")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)
        modules = [
            ("Matrices", "imagenes/matrices.png"),
            ("Polinomios", "imagenes/polinomios.png"),
            ("Vectores", "imagenes/vectores.png"),
            ("Gráficas", "imagenes/graficas.png"),
            ("Cálculo", "imagenes/calculo.png"),
            ("AcercaDe", "imagenes/acercade.png")
        ]
        for i, (name, icon_path) in enumerate(modules):
            btn = QToolButton()
            btn.setText(name)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(48, 48))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                background: #2c3e50; color: white;
                font-weight: bold; font-size: 14px;
                border-radius: 10px; padding: 15px;
            """)
            if name == "Matrices":
                btn.clicked.connect(lambda _, x=self.submenu_matrices: self.stack.setCurrentWidget(x))
            elif name == "Polinomios":
                btn.clicked.connect(lambda _, x=self.submenu_polinomios: self.stack.setCurrentWidget(x))
            elif name == "Vectores":
                btn.clicked.connect(lambda _, x=self.submenu_vectores: self.stack.setCurrentWidget(x))
            elif name == "Gráficas":
                btn.clicked.connect(lambda _, x=self.submenu_graficas: self.stack.setCurrentWidget(x))
            elif name == "Cálculo":
                btn.clicked.connect(lambda _, x=self.submenu_calculo: self.stack.setCurrentWidget(x))
            elif name == "AcercaDe":
                btn.clicked.connect(lambda _, x=self.vista_acercade: self.stack.setCurrentWidget(x))
            grid.addWidget(btn, i // 3, i % 3)

        layout.addLayout(grid)
        self.stack.setCurrentWidget(self.menu_widget)

    def ir_a_suma_matrices(self):
        self.stack.setCurrentWidget(self.vista_suma_matrices)

    def ir_a_resta_matrices(self):
        self.stack.setCurrentWidget(self.vista_resta_matrices)

    def ir_a_multiplicacion_matrices(self):
        self.stack.setCurrentWidget(self.vista_multiplicacion)

    def ir_a_determinante_matrices(self):
        self.stack.setCurrentWidget(self.vista_determinante)

    def ir_a_inversa_matrices(self):
        self.stack.setCurrentWidget(self.vista_inversa)

    def ir_a_sistema_matrices(self):
        self.stack.setCurrentWidget(self.vista_sistema)

    def volver_a_matrices(self):
        self.stack.setCurrentWidget(self.submenu_matrices)
    
    def ir_a_suma_polinomios(self):
        self.stack.setCurrentWidget(self.vista_suma_polinomios)

    def ir_a_multiplicacion_polinomios(self):
        self.stack.setCurrentWidget(self.vista_multiplicacion_polinomios)

    def ir_a_derivacion_polinomios(self):
        self.stack.setCurrentWidget(self.vista_derivacion_polinomios)

    def ir_a_integracion_polinomios(self):
        self.stack.setCurrentWidget(self.vista_integracion_polinomios)

    def ir_a_evaluacion_polinomios(self):
        self.stack.setCurrentWidget(self.vista_evaluacion_polinomios)

    def volver_a_polinomios(self):
        self.stack.setCurrentWidget(self.submenu_polinomios)

    def ir_a_suma_vectores(self):
        self.stack.setCurrentWidget(self.vista_suma_vectores)
    
    def ir_a_resta_vectores(self):
        self.stack.setCurrentWidget(self.vista_resta_vectores)

    def ir_a_magnitud_vectores(self):
        self.stack.setCurrentWidget(self.vista_magnitud_vectores)
    
    def ir_a_producto_punto_vectores(self):
        self.stack.setCurrentWidget(self.VistaProductoPuntoVectores)

    def ir_a_producto_cruzado_vectores(self):
        self.stack.setCurrentWidget(self.vista_producto_cruz_vectores)
    
    def volver_a_vectores(self):
        self.stack.setCurrentWidget(self.submenu_vectores)

    def ir_a_grafica_2d(self):
        self.stack.setCurrentWidget(self.vista_grafica_2d)
    
    def ir_a_grafica_3d(self):
        self.stack.setCurrentWidget(self.vista_grafica_3d)

    def volver_a_graficas(self):
        self.stack.setCurrentWidget(self.submenu_graficas)

    def ir_a_derivada(self):
        self.stack.setCurrentWidget(self.vista_derivada)

    def ir_a_integral_indefinida(self):
        self.stack.setCurrentWidget(self.vista_integral_indefinida)

    def ir_a_integral_definida(self):
        self.stack.setCurrentWidget(self.vista_integral_definida)

    def volver_a_calculo(self):
        self.stack.setCurrentWidget(self.submenu_calculo)
    
# ------------------------- EJECUCIÓN -------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuPrincipal()
    window.show()
    sys.exit(app.exec_())

