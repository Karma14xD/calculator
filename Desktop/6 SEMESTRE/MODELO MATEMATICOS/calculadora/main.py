import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget,
    QToolButton, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy,
    QHBoxLayout, QSpinBox, QPushButton, QLineEdit, QFrame,QFormLayout,QComboBox,QTableWidget,QTableWidgetItem,QScrollArea
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import re
import numpy as np
from sympy import Matrix,sympify,simplify,symbols,diff,integrate,lambdify
import os

def obtener_ruta_recurso(rel_path):
    """Devuelve la ruta absoluta al recurso, compatible con PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

# ------------------------- CLASE BASE PARA SUBMENÚS -------------------------
# Esta clase sirve como base para crear submenús en la interfaz.
# Proporciona una función común para agregar un botón "Volver al Menú".
class SubmenuBase(QWidget):
    def __init__(self, stack=None, menu_widget=None):
        super().__init__()
        self.stack = stack  # Referencia al QStackedWidget que maneja el cambio de vistas.
        self.menu_widget = menu_widget  # Referencia al menú principal (para volver a él).

    # Método para agregar un botón "Volver al Menú" a un layout dado.
    def add_back_button(self, layout):
        back_btn = QToolButton()  # Crea un botón tipo ToolButton.
        back_btn.setText("Volver al Menú")  # Texto del botón.
        back_btn.setIcon(QIcon(obtener_ruta_recurso(os.path.join("imagenes", "volver.png"))))
        back_btn.setIconSize(QSize(24, 24))  # Tamaño del ícono.
        back_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)  # Ícono a la izquierda del texto.
        
        # Estilo visual con CSS: color, bordes, fuente, etc.
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

        back_btn.clicked.connect(self.go_back)  # Conecta el botón a la función que vuelve al menú.
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)  # Agrega el botón al layout centrado.

    # Función que cambia la vista al menú principal.
    def go_back(self):
        if self.stack and self.menu_widget:
            self.stack.setCurrentWidget(self.menu_widget)

# ------------------------- CLASE SUBMENÚ MATRICES -------------------------
# Esta clase representa el submenú de operaciones con matrices.
# Hereda de SubmenuBase para tener acceso al botón "Volver al Menú".
class SubmenuMatrices(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_resta, go_to_multiplicacion, go_to_determinante, go_to_inversa_matriz, go_to_sistema, menu_widget):
        # Llama al constructor de SubmenuBase para configurar stack y menú principal
        super().__init__(stack, menu_widget)

        # Guarda las funciones que abren las diferentes vistas de operaciones
        self.go_to_suma = go_to_suma
        self.go_to_resta = go_to_resta
        self.go_to_multiplicacion = go_to_multiplicacion
        self.go_to_determinante = go_to_determinante
        self.go_to_inversa_matriz = go_to_inversa_matriz
        self.go_to_sistema = go_to_sistema

        # Inicializa la interfaz del submenú
        self.init_ui()

    # Configura el diseño visual del submenú
    def init_ui(self):
        layout = QVBoxLayout(self)  # Layout principal vertical

        # Título
        title = QLabel("Operaciones con Matrices")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid layout para los botones de operaciones
        grid = QGridLayout()
        grid.setSpacing(20)  # Espaciado entre botones
        grid.setAlignment(Qt.AlignCenter)

        # Lista de operaciones con sus respectivos íconos
        operaciones = [
            ("Suma", obtener_ruta_recurso(os.path.join("imagenes", "suma.png"))),
            ("Resta", obtener_ruta_recurso(os.path.join("imagenes", "resta.png"))),
            ("Multiplicación", obtener_ruta_recurso(os.path.join("imagenes", "multiplicacion.png"))),
            ("Determinante", obtener_ruta_recurso(os.path.join("imagenes", "determinante.png"))),
            ("Inversa", obtener_ruta_recurso(os.path.join("imagenes", "inversa.png"))),
            ("Resolver Sistema", obtener_ruta_recurso(os.path.join("imagenes", "ecuaciones.png"))),
        ]


        # Crea un botón para cada operación
        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Texto debajo del ícono
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

            # Conecta cada botón con su respectiva función
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
                # En caso de que se agregue una operación nueva no reconocida
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Matrices", f"Operación: {x}"))

            # Agrega el botón a la grilla en posición fila/columna
            grid.addWidget(btn, idx // 3, idx % 3)

        # Añade la grilla al layout principal
        layout.addLayout(grid)

        # Espaciado opcional visual
        layout.addSpacing(1)

        # Botón para volver al menú principal (heredado)
        self.add_back_button(layout)

# ------------------------- VISTA SUMA MATRICES -------------------------
class VistaSumaMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función que se ejecuta cuando el usuario quiere volver al menú anterior
        self.volver_callback = volver_callback

        # Estilo general del fondo y fuente
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        # Lista para guardar los frames de matrices generadas (permite eliminarlas después)
        self.matriz_frames = []

        # Título principal
        titulo = QLabel("➕ Suma de Matrices")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(titulo)

        # Contenedor principal vertical
        contenedor = QVBoxLayout()
        contenedor.setAlignment(Qt.AlignCenter)

        # Layout que contiene los controles para generar matrices
        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)

        # Estilo común para todos los QSpinBox
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        # SpinBoxes para configurar cantidad de matrices, filas y columnas
        self.spin_matrices = QSpinBox()
        self.spin_matrices.setMinimum(2)
        self.spin_matrices.setStyleSheet(estilo_spin)

        self.spin_filas = QSpinBox()
        self.spin_filas.setMinimum(1)
        self.spin_filas.setStyleSheet(estilo_spin)

        self.spin_columnas = QSpinBox()
        self.spin_columnas.setMinimum(1)
        self.spin_columnas.setStyleSheet(estilo_spin)

        # Añadir etiquetas y SpinBoxes al layout de controles
        for label_text, spin in [("Cantidad de Matrices:", self.spin_matrices),
                                 ("Cantidad de Filas:", self.spin_filas),
                                 ("Cantidad de Columnas:", self.spin_columnas)]:
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            self.controles.addWidget(label, alignment=Qt.AlignCenter)
            self.controles.addWidget(spin, alignment=Qt.AlignCenter)

        contenedor.addLayout(self.controles)

        # Botón para generar los campos de las matrices
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

        # Layout horizontal donde se mostrarán las matrices generadas
        self.grid_matrices = QHBoxLayout()
        self.grid_matrices.setSpacing(15)
        contenedor.addLayout(self.grid_matrices)

        # Botón para realizar la suma
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

        # Grid para mostrar el resultado de la suma
        self.resultado_grid = QGridLayout()
        contenedor.addLayout(self.resultado_grid)

        # Botón para volver al menú principal
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

        # Agrega todo al layout principal
        self.layout.addLayout(contenedor)

        # Lista para almacenar los inputs de cada matriz
        self.matriz_inputs = []

    def generar_matrices(self):
        # Limpia matrices anteriores si las hay
        for frame in self.matriz_frames:
            self.grid_matrices.removeWidget(frame)
            frame.deleteLater()
        self.matriz_frames.clear()
        self.matriz_inputs.clear()

        # Obtener datos del usuario
        n = self.spin_matrices.value()
        f = self.spin_filas.value()
        c = self.spin_columnas.value()

        # Generar n matrices de tamaño f x c
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
        # Limpia espacios y convierte a minúsculas
        texto = texto.strip().lower()

        # Si es un número decimal o entero válido
        if re.fullmatch(r"[-+]?\d+(\.\d+)?", texto):
            return float(texto)

        # Si es un término con variable tipo x, y, z
        elif re.fullmatch(r"[-+]?\d*(x|y|z)", texto):
            coef = texto[:-1] if texto[-1] in "xyz" else texto
            if coef in ("", "+"):
                return 1.0
            elif coef == "-":
                return -1.0
            return float(coef)

        # Si no es interpretable
        raise ValueError("No interpretable")

    def realizar_suma(self):
        if len(self.matriz_inputs) < 2:
            QMessageBox.warning(self, "Error", "Debes tener al menos dos matrices para sumar.")
            return

        filas = len(self.matriz_inputs[0])
        columnas = len(self.matriz_inputs[0][0])

        # Validar que todas las matrices tengan el mismo tamaño
        for matriz in self.matriz_inputs:
            if len(matriz) != filas or any(len(row) != columnas for row in matriz):
                QMessageBox.critical(self, "Error", "Todas las matrices deben tener la misma dimensión.")
                return

        # Inicializar matriz resultado con ceros
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

        # Limpiar resultados anteriores
        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        # Mostrar matriz resultado
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
        # Hereda toda la funcionalidad de VistaSumaMatrices
        super().__init__(volver_callback)

        # Cambia el título del QLabel para mostrar "Resta de Matrices"
        self.findChild(QLabel).setText("➖ Resta de Matrices")

        # Cambia el texto del botón de "Sumar" a "Restar"
        self.btn_sumar.setText("Restar")

        # Cambia el estilo del botón para diferenciarlo (color rojo)
        self.btn_sumar.setStyleSheet("""
            QPushButton {
                background-color: #c0392b; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)

        # Desconecta la función de suma anterior
        self.btn_sumar.clicked.disconnect()

        # Conecta el botón al nuevo método para realizar la resta
        self.btn_sumar.clicked.connect(self.realizar_resta)

    def realizar_resta(self):
        # Solo permite restar dos matrices
        if len(self.matriz_inputs) != 2:
            QMessageBox.warning(self, "Error", "Solo se pueden restar dos matrices.")
            return

        # Verifica dimensiones
        filas = len(self.matriz_inputs[0])
        columnas = len(self.matriz_inputs[0][0])

        # Asegura que ambas matrices tengan la misma forma
        for matriz in self.matriz_inputs:
            if len(matriz) != filas or any(len(row) != columnas for row in matriz):
                QMessageBox.critical(self, "Error", "Ambas matrices deben tener la misma dimensión.")
                return

        # Inicializa la matriz resultado
        resultado = [[0 for _ in range(columnas)] for _ in range(filas)]

        try:
            # Resta celda por celda: resultado = matriz1 - matriz2
            for i in range(filas):
                for j in range(columnas):
                    val1 = self.interpretar_valor(self.matriz_inputs[0][i][j].text())
                    val2 = self.interpretar_valor(self.matriz_inputs[1][i][j].text())
                    resultado[i][j] = val1 - val2
        except Exception:
            # Si hay error al interpretar valores
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        # Limpia cualquier resultado anterior en el grid
        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        # Muestra la nueva matriz resultado
        for i in range(filas):
            for j in range(columnas):
                res = QLineEdit(str(resultado[i][j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")
                self.resultado_grid.addWidget(res, i, j)

# ------------------------- FUNCIÓN GLOBAL PARA INTERPRETAR VALORES -------------------------
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

# ------------------------- VISTA MULTIPLICACIÓN MATRICES -------------------------
class VistaMultiplicacionMatrices(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver a la vista anterior
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("✖️ Multiplicación de Matrices")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout para los controles de entrada
        controles = QHBoxLayout()
        controles.setAlignment(Qt.AlignCenter)

        # Definición de los SpinBoxes para filtrar las dimensiones de las matrices
        self.filasA = QSpinBox(); self.filasA.setMinimum(1)
        self.colsA = QSpinBox(); self.colsA.setMinimum(1)
        self.filasB = QSpinBox(); self.filasB.setMinimum(1)
        self.colsB = QSpinBox(); self.colsB.setMinimum(1)

        # Estilo de los SpinBoxes
        estilo_spin = "QSpinBox { background: white; font-size: 14px; padding: 4px; }"
        for spin in [self.filasA, self.colsA, self.filasB, self.colsB]:
            spin.setStyleSheet(estilo_spin)

        # Labels y SpinBoxes para las dimensiones de las matrices
        for label, spin in [("Filas A:", self.filasA), ("Columnas A:", self.colsA),
                            ("Filas B:", self.filasB), ("Columnas B:", self.colsB)]:
            l = QLabel(label)
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
            controles.addWidget(l)
            controles.addWidget(spin)

        self.layout.addLayout(controles)

        # Botón para generar las matrices
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

        # Grid donde se mostrarán las matrices generadas
        self.grid = QHBoxLayout()
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(self.grid)

        # Botón para realizar la multiplicación
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

        # Layout para mostrar el resultado de la multiplicación
        self.resultado_grid = QGridLayout()
        self.layout.addLayout(self.resultado_grid)

        # Botón para volver a la vista anterior
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

    # Método para generar las matrices basadas en las dimensiones
    def generar_matrices(self):
        # Limpia la vista previa de las matrices si existen
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)
                widget.deleteLater()

        self.matrices = []  # Lista que almacenará las matrices generadas

        # Obtiene las dimensiones de las matrices A y B
        fA, cA, fB, cB = self.filasA.value(), self.colsA.value(), self.filasB.value(), self.colsB.value()

        # Verifica si las matrices son multiplicables (Columnas de A deben ser iguales a las filas de B)
        if cA != fB:
            QMessageBox.critical(self, "Error", "Columnas de A deben coincidir con filas de B.")
            return

        # Genera las matrices con los tamaños especificados
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

    # Método para realizar la multiplicación de matrices
    def realizar_multiplicacion(self):
        # Verifica que se hayan generado exactamente dos matrices
        if len(self.matrices) != 2:
            QMessageBox.warning(self, "Error", "Debes generar dos matrices primero.")
            return

        A, B = self.matrices  # A y B son las matrices a multiplicar
        try:
            # Convierte las entradas de texto a valores numéricos
            matA = [[interpretar_valor(cell.text()) for cell in row] for row in A]
            matB = [[interpretar_valor(cell.text()) for cell in row] for row in B]
        except ValueError:
            # En caso de que haya valores inválidos
            QMessageBox.critical(self, "Error", "Todos los valores deben ser numéricos válidos (ej: 3, -2.5, x, 4x).")
            return

        # Realiza la multiplicación de matrices
        fA, cB, cA = len(matA), len(matB[0]), len(matA[0])
        resultado = [[0] * cB for _ in range(fA)]
        for i in range(fA):
            for j in range(cB):
                for k in range(cA):
                    resultado[i][j] += matA[i][k] * matB[k][j]

        # Limpia el resultado anterior
        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        # Muestra el resultado de la multiplicación en la interfaz
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
        # Constructor de la clase, se inicializan los elementos de la interfaz
        super().__init__()
        self.volver_callback = volver_callback  # Callback para regresar a la vista anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Estilo general de la interfaz
        self.layout = QVBoxLayout(self)  # Layout principal vertical

        # Título de la vista
        self.titulo = QLabel("🧮 Determinante de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centrado del título
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")  # Estilo del título
        self.layout.addWidget(self.titulo)  # Añadir título al layout

        # Controles para especificar las dimensiones de la matriz (filas y columnas)
        controles = QHBoxLayout()  # Layout horizontal para controles de filas y columnas
        controles.setAlignment(Qt.AlignCenter)  # Centrado de los controles

        self.filas = QSpinBox()  # Spin box para el número de filas
        self.filas.setMinimum(1)  # Número mínimo de filas
        self.filas.setValue(2)  # Valor inicial (2 filas)
        self.columnas = QSpinBox()  # Spin box para el número de columnas
        self.columnas.setMinimum(1)  # Número mínimo de columnas
        self.columnas.setValue(2)  # Valor inicial (2 columnas)

        # Estilo para los spin boxes
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        # Crear etiquetas y añadir los spin boxes al layout
        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)  # Crear etiqueta
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")  # Estilo de la etiqueta
            controles.addWidget(l)  # Añadir etiqueta al layout
            controles.addWidget(spin)  # Añadir spin box al layout

        self.layout.addLayout(controles)  # Añadir los controles de filas y columnas al layout principal

        # Botón para generar la matriz con las dimensiones indicadas por el usuario
        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)  # Estilo del botón
        self.btn_generar.clicked.connect(self.generar_matriz)  # Conectar el botón a la función de generación de matriz
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)  # Añadir botón al layout principal

        # Layout para los campos de la matriz
        self.grid = QGridLayout()  # Grid layout para organizar las celdas de la matriz
        self.grid.setSpacing(10)  # Espaciado entre celdas
        self.layout.addLayout(self.grid)  # Añadir el grid al layout principal

        # Botón para calcular el determinante
        self.btn_determinante = QPushButton("Calcular Determinante")
        self.btn_determinante.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)  # Estilo del botón
        self.btn_determinante.clicked.connect(self.calcular_determinante)  # Conectar el botón a la función de cálculo del determinante
        self.layout.addWidget(self.btn_determinante, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Etiqueta para mostrar el resultado del determinante
        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)  # Centrado del texto
        self.resultado.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-top: 10px;")  # Estilo de la etiqueta
        self.layout.addWidget(self.resultado)  # Añadir la etiqueta al layout

        # Botón para volver a la vista anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)  # Estilo del botón
        self.btn_volver.clicked.connect(self.volver_callback)  # Conectar el botón a la función de volver
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        self.inputs = []  # Lista para almacenar las entradas de la matriz

    # Función para generar la matriz según el tamaño especificado
    def generar_matriz(self):
        # Limpiar cualquier campo previamente generado
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)  # Eliminar widget del grid
                widget.deleteLater()  # Eliminar widget de memoria
        self.inputs.clear()  # Limpiar la lista de entradas

        # Obtener las dimensiones de la matriz (filas y columnas)
        f, c = self.filas.value(), self.columnas.value()

        # Generar las celdas de la matriz
        for i in range(f):
            fila = []
            for j in range(c):
                # Crear un campo de texto para cada elemento de la matriz
                campo = QLineEdit("0")  # Valor inicial en cada campo
                campo.setAlignment(Qt.AlignCenter)  # Alineación centrada del texto
                campo.setFixedWidth(40)  # Ancho fijo para cada campo
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")  # Estilo del campo
                self.grid.addWidget(campo, i, j)  # Añadir campo al grid
                fila.append(campo)  # Añadir campo a la fila
            self.inputs.append(fila)  # Añadir fila a la lista de entradas

    # Función para calcular el determinante de la matriz
    def calcular_determinante(self):
        # Verificar si la matriz es cuadrada
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            # Mostrar un mensaje de advertencia si la matriz no es cuadrada
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular el determinante.")
            return

        try:
            # Intentar convertir los valores de la matriz a expresiones simbólicas
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            # Calcular el determinante usando la clase Matrix
            determinante = Matrix(matriz).det()
            # Mostrar el determinante en la etiqueta
            self.resultado.setText(f"Determinante: {determinante}")
        except Exception:
            # Mostrar un mensaje de error si la conversión o el cálculo fallan
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean expresiones simbólicas válidas.")

# ------------------------- VISTA INVERSA MATRICES -------------------------
class VistaInversaMatrices(QWidget):
    def __init__(self, volver_callback):
        # Constructor de la clase, inicializa los elementos de la interfaz
        super().__init__()
        self.volver_callback = volver_callback  # Callback para regresar a la vista anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Estilo general de la interfaz
        self.layout = QVBoxLayout(self)  # Layout principal vertical

        # Título de la vista
        self.titulo = QLabel("🔄 Inversa de una Matriz")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centrado del título
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")  # Estilo del título
        self.layout.addWidget(self.titulo)  # Añadir título al layout

        # Controles para especificar las dimensiones de la matriz (filas y columnas)
        controles = QHBoxLayout()  # Layout horizontal para controles de filas y columnas
        controles.setAlignment(Qt.AlignCenter)  # Centrado de los controles

        self.filas = QSpinBox()  # Spin box para el número de filas
        self.filas.setMinimum(1)  # Número mínimo de filas
        self.filas.setValue(2)  # Valor inicial (2 filas)
        self.columnas = QSpinBox()  # Spin box para el número de columnas
        self.columnas.setMinimum(1)  # Número mínimo de columnas
        self.columnas.setValue(2)  # Valor inicial (2 columnas)

        # Estilo para los spin boxes
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"
        self.filas.setStyleSheet(estilo_spin)
        self.columnas.setStyleSheet(estilo_spin)

        # Crear etiquetas y añadir los spin boxes al layout
        for label, spin in [("Filas:", self.filas), ("Columnas:", self.columnas)]:
            l = QLabel(label)  # Crear etiqueta
            l.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")  # Estilo de la etiqueta
            controles.addWidget(l)  # Añadir etiqueta al layout
            controles.addWidget(spin)  # Añadir spin box al layout

        self.layout.addLayout(controles)  # Añadir los controles de filas y columnas al layout principal

        # Botón para generar la matriz con las dimensiones indicadas por el usuario
        self.btn_generar = QPushButton("Generar Matriz")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)  # Estilo del botón
        self.btn_generar.clicked.connect(self.generar_matriz)  # Conectar el botón a la función de generación de matriz
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)  # Añadir botón al layout principal

        # Layout para los campos de la matriz
        self.grid = QGridLayout()  # Grid layout para organizar las celdas de la matriz
        self.grid.setSpacing(10)  # Espaciado entre celdas
        self.layout.addLayout(self.grid)  # Añadir el grid al layout principal

        # Botón para calcular la inversa de la matriz
        self.btn_inversa = QPushButton("Calcular Inversa")
        self.btn_inversa.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)  # Estilo del botón
        self.btn_inversa.clicked.connect(self.calcular_inversa)  # Conectar el botón a la función de cálculo de la inversa
        self.layout.addWidget(self.btn_inversa, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Layout para mostrar los resultados (inversa)
        self.resultado_grid = QGridLayout()  # Grid layout para mostrar la inversa calculada
        self.resultado_grid.setSpacing(6)  # Espaciado entre celdas
        self.layout.addLayout(self.resultado_grid)  # Añadir el grid de resultados al layout principal

        # Botón para volver a la vista anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)  # Estilo del botón
        self.btn_volver.clicked.connect(self.volver_callback)  # Conectar el botón a la función de volver
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        self.inputs = []  # Lista para almacenar las entradas de la matriz

    # Función para generar la matriz según el tamaño especificado
    def generar_matriz(self):
        # Limpiar cualquier campo previamente generado
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)  # Eliminar widget del grid
                widget.deleteLater()  # Eliminar widget de memoria
        self.inputs.clear()  # Limpiar la lista de entradas

        # Obtener las dimensiones de la matriz (filas y columnas)
        f, c = self.filas.value(), self.columnas.value()

        # Generar las celdas de la matriz
        for i in range(f):
            fila = []
            for j in range(c):
                # Crear un campo de texto para cada elemento de la matriz
                campo = QLineEdit("0")  # Valor inicial en cada campo
                campo.setAlignment(Qt.AlignCenter)  # Alineación centrada del texto
                campo.setFixedWidth(40)  # Ancho fijo para cada campo
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")  # Estilo del campo
                self.grid.addWidget(campo, i, j)  # Añadir campo al grid
                fila.append(campo)  # Añadir campo a la fila
            self.inputs.append(fila)  # Añadir fila a la lista de entradas

    # Función para calcular la inversa de la matriz
    def calcular_inversa(self):
        # Verificar si la matriz es cuadrada
        f, c = self.filas.value(), self.columnas.value()
        if f != c:
            # Mostrar un mensaje de advertencia si la matriz no es cuadrada
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada para calcular la inversa.")
            return

        try:
            # Intentar convertir los valores de la matriz a expresiones simbólicas
            matriz = [[interpretar_valor_simbolico(cell.text()) for cell in row] for row in self.inputs]
            M = Matrix(matriz)
            # Verificar si el determinante de la matriz es 0 (no tiene inversa)
            if M.det() == 0:
                QMessageBox.critical(self, "Error", "La matriz no tiene inversa (determinante = 0).")
                return
            # Calcular la inversa de la matriz
            inversa = M.inv()
        except Exception:
            # Mostrar un mensaje de error si la conversión o el cálculo fallan
            QMessageBox.critical(self, "Error", "Verifica que todos los valores sean numéricos o simbólicos válidos.")
            return

        # Limpiar cualquier resultado previo en el grid de resultados
        for i in reversed(range(self.resultado_grid.count())):
            widget = self.resultado_grid.itemAt(i).widget()
            if widget:
                self.resultado_grid.removeWidget(widget)
                widget.deleteLater()

        # Mostrar los valores de la inversa en el grid de resultados
        for i in range(inversa.rows):
            for j in range(inversa.cols):
                # Crear un campo de texto de solo lectura para cada valor de la inversa
                res = QLineEdit(str(inversa[i, j]))
                res.setReadOnly(True)
                res.setAlignment(Qt.AlignCenter)  # Alineación centrada del texto
                res.setStyleSheet("background-color: #ecf0f1; border: 1px solid #bbb; padding: 4px;")  # Estilo del campo
                self.resultado_grid.addWidget(res, i, j)  # Añadir el campo al grid de resultados

# ------------------------- VISTA SISTEMA DE ECUACIONES MATRICES -------------------------
class VistaSistemaEcuaciones(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Callback para regresar a la vista anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Estilo general de la interfaz
        self.layout = QVBoxLayout(self)  # Layout principal vertical

        # Título de la vista
        titulo = QLabel("🧩 Resolver Sistema de Ecuaciones")
        titulo.setAlignment(Qt.AlignCenter)  # Centrado del título
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")  # Estilo del título
        self.layout.addWidget(titulo)  # Añadir título al layout

        # Controles para especificar el número de ecuaciones (filas)
        controles = QHBoxLayout()  # Layout horizontal para el número de ecuaciones
        controles.setAlignment(Qt.AlignCenter)  # Centrado de los controles

        self.filas = QSpinBox()  # Spin box para el número de ecuaciones
        self.filas.setMinimum(2)  # Número mínimo de ecuaciones
        self.filas.setValue(2)  # Valor inicial (2 ecuaciones)
        self.filas.setStyleSheet("QSpinBox { background-color: white; font-size: 14px; padding: 4px; }")

        # Etiqueta para el número de ecuaciones
        label = QLabel("Número de ecuaciones:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")

        controles.addWidget(label)  # Añadir etiqueta al layout
        controles.addWidget(self.filas)  # Añadir spin box al layout
        self.layout.addLayout(controles)  # Añadir controles al layout principal

        # Botón para generar los campos de entrada para el sistema
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)  # Estilo del botón
        self.btn_generar.clicked.connect(self.generar_campos)  # Conectar el botón a la función de generación de campos
        self.layout.addWidget(self.btn_generar, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Layout para los campos de las matrices A y B (coeficientes y resultados)
        self.grid = QGridLayout()  # Grid layout para organizar los campos
        self.grid.setSpacing(10)  # Espaciado entre celdas
        self.layout.addLayout(self.grid)  # Añadir el grid al layout principal

        # Botón para resolver el sistema de ecuaciones
        self.btn_resolver = QPushButton("Resolver Sistema")
        self.btn_resolver.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)  # Estilo del botón
        self.btn_resolver.clicked.connect(self.resolver_sistema)  # Conectar el botón a la función de resolución
        self.layout.addWidget(self.btn_resolver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        # Etiqueta para mostrar el resultado
        self.resultado = QLabel("")
        self.resultado.setAlignment(Qt.AlignCenter)  # Centrado del texto del resultado
        self.resultado.setStyleSheet("font-size: 18px; color: #2c3e50; margin-top: 10px;")
        self.layout.addWidget(self.resultado)  # Añadir la etiqueta de resultado al layout

        # Botón para volver a la vista anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)  # Estilo del botón
        self.btn_volver.clicked.connect(self.volver_callback)  # Conectar el botón a la función de volver
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)  # Añadir botón al layout

        self.inputs_A = []  # Lista para almacenar las entradas de la matriz A
        self.inputs_B = []  # Lista para almacenar las entradas de la matriz B

    # Función para generar los campos de entrada de la matriz A (coeficientes) y la matriz B (resultados)
    def generar_campos(self):
        # Limpiar cualquier campo previamente generado
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                self.grid.removeWidget(widget)  # Eliminar widget del grid
                widget.deleteLater()  # Eliminar widget de memoria
        self.inputs_A.clear()  # Limpiar la lista de entradas de A
        self.inputs_B.clear()  # Limpiar la lista de entradas de B

        n = self.filas.value()  # Número de ecuaciones (filas)

        # Generar las celdas de la matriz A (coeficientes) y la matriz B (resultados)
        for i in range(n):
            fila_A = []  # Lista para almacenar los campos de la fila de la matriz A
            for j in range(n):
                # Crear un campo de texto para cada coeficiente de la matriz A
                campo = QLineEdit("0")
                campo.setAlignment(Qt.AlignCenter)  # Alineación centrada
                campo.setFixedWidth(40)  # Ancho fijo de cada campo
                campo.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
                self.grid.addWidget(campo, i, j)  # Añadir campo al grid
                fila_A.append(campo)  # Añadir campo a la fila de la matriz A
            self.inputs_A.append(fila_A)  # Añadir fila a la lista de entradas de la matriz A

            # Crear un campo de texto para el resultado de la ecuación (matriz B)
            campo_b = QLineEdit("0")
            campo_b.setAlignment(Qt.AlignCenter)  # Alineación centrada
            campo_b.setFixedWidth(40)  # Ancho fijo de cada campo
            campo_b.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px;")
            self.grid.addWidget(campo_b, i, n)  # Añadir campo al grid
            self.inputs_B.append(campo_b)  # Añadir campo a la lista de entradas de la matriz B

    # Función para resolver el sistema de ecuaciones
    def resolver_sistema(self):
        try:
            # Convertir los valores de los campos de entrada en matrices simbólicas
            A = [[interpretar_valor_simbolico(cell.text()) for cell in fila] for fila in self.inputs_A]
            B = [interpretar_valor_simbolico(cell.text()) for cell in self.inputs_B]
            M = Matrix(A)  # Crear la matriz A
            v = Matrix(B)  # Crear la matriz B

            # Verificar si el determinante de la matriz A es 0 (sistema no tiene solución única)
            if M.det() == 0:
                self.resultado.setText("No tiene solución única (determinante = 0).")
                return

            # Resolver el sistema de ecuaciones
            solucion = M.inv() * v
            resultado_texto = "<b>Solución:</b><br>" + "<br>".join([f"x{i+1} = {valor}" for i, valor in enumerate(solucion)])
            self.resultado.setText(resultado_texto)  # Mostrar la solución en el label de resultados
        except Exception:
            # Mostrar un mensaje de error si algo falla en el proceso de resolución
            QMessageBox.critical(self, "Error", "Verifica que los valores sean numéricos o simbólicos válidos.")

# ------------------------- CLASE SUBMENÚ POLINOMIOS -------------------------
class SubmenuPolinomios(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_multiplicacion, go_to_derivacion, go_to_integracion, go_to_evaluacion, menu_widget):
        super().__init__(stack, menu_widget)  # Llamada al constructor de la clase base
        self.go_to_suma = go_to_suma  # Callback para ir a la vista de suma
        self.go_to_multiplicacion = go_to_multiplicacion  # Callback para ir a la vista de multiplicación
        self.go_to_derivacion = go_to_derivacion  # Callback para ir a la vista de derivación
        self.go_to_integracion = go_to_integracion  # Callback para ir a la vista de integración
        self.go_to_evaluacion = go_to_evaluacion  # Callback para ir a la vista de evaluación
        self.init_ui()  # Inicializar la interfaz de usuario

    def init_ui(self):
        layout = QVBoxLayout(self)  # Layout principal vertical

        # Título del submenú
        title = QLabel("Operaciones con Polinomios")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)  # Centrado del título
        layout.addWidget(title)  # Añadir título al layout

        # Layout para las operaciones
        grid = QGridLayout()  # Grid layout para organizar los botones
        grid.setSpacing(20)  # Espaciado entre los botones
        grid.setAlignment(Qt.AlignCenter)  # Centrado de los botones en el grid

        # Lista de operaciones con texto y sus respectivos iconos
        operaciones = [
            ("Suma", obtener_ruta_recurso(os.path.join("imagenes", "suma.png"))),
            ("Multiplicación", obtener_ruta_recurso(os.path.join("imagenes", "multiplicacion.png"))),
            ("Derivación", obtener_ruta_recurso(os.path.join("imagenes", "derivada.png"))),
            ("Integración", obtener_ruta_recurso(os.path.join("imagenes", "integral.png"))),
            ("Evaluación", obtener_ruta_recurso(os.path.join("imagenes", "evaluar.png"))),
        ]


        # Crear un botón para cada operación
        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()  # Crear un QToolButton para cada operación
            btn.setText(texto)  # Establecer el texto del botón
            btn.setIcon(QIcon(icono))  # Establecer el icono del botón
            btn.setIconSize(QSize(40, 40))  # Tamaño del icono
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Estilo con texto debajo del icono
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
            """)  # Estilo del botón

            # Conectar cada botón con su correspondiente función (callback)
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
                # Si no coincide con ninguna de las operaciones, mostrar un mensaje por defecto
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Polinomios", f"Operación: {x}"))

            # Añadir el botón al grid en la posición correspondiente
            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)  # Añadir el grid de botones al layout
        layout.addSpacing(1)  # Espaciado adicional después de los botones
        self.add_back_button(layout)  # Añadir el botón para volver al menú principal

# ------------------------- CLASE VISTA SUMA POLINOMIOS -------------------------
class VistaSumaPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("➕ Suma de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout contenedor principal
        self.contenedor = QVBoxLayout()
        self.contenedor.setAlignment(Qt.AlignCenter)

        # Layout para los controles (como el número de polinomios)
        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        # Spinner para elegir la cantidad de polinomios
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)  # Número mínimo de polinomios
        self.spin_cantidad.setStyleSheet(estilo_spin)

        # Etiqueta que indica el propósito del spinner
        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)

        # Agregar los controles al contenedor
        self.contenedor.addLayout(self.controles)

        # Botón para generar los campos de los polinomios
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
        # Conectar el botón a la función que genera los campos
        self.btn_generar.clicked.connect(self.generar_campos)
        self.contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        # Layout para los campos de entrada de los polinomios
        self.campos_layout = QFormLayout()
        self.contenedor.addLayout(self.campos_layout)

        # Botón para sumar los polinomios
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
        # Conectar el botón a la función que suma los polinomios
        self.btn_sumar.clicked.connect(self.sumar_polinomios)
        self.contenedor.addWidget(self.btn_sumar, alignment=Qt.AlignCenter)

        # Campo para mostrar el resultado de la suma
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.contenedor.addWidget(self.resultado)

        # Botón para volver al menú anterior
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

        # Agregar todo al layout principal
        self.layout.addLayout(self.contenedor)
        self.campos = []  # Lista para almacenar los campos de entrada de los polinomios

    # Método para generar los campos de entrada para los polinomios
    def generar_campos(self):
        # Eliminar los campos existentes antes de generar nuevos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()  # Obtener la cantidad de polinomios
        # Crear los campos de texto para los polinomios
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Polinomio {i+1} (ej: x^2 + 3x - 4)")
            campo.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Polinomio {i+1}:", campo)
            self.campos.append(campo)

    # Método para sumar los polinomios
    def sumar_polinomios(self):
        try:
            # Sumar todos los polinomios introducidos
            suma = sum(sympify(limpiar_expresion(campo.text())) for campo in self.campos)
            # Mostrar el resultado simplificado
            self.resultado.setText(str(simplify(suma)))
        except Exception:
            # Si hay algún error (como una expresión inválida), mostrar mensaje de error
            QMessageBox.critical(self, "Error", "Verifica que todos los polinomios sean expresiones válidas.")

#--------------- CLASE VISTA MULTIPLICACION POLINOMIOS-----------
class VistaMultiplicacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("✖ Multiplicación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout contenedor principal
        self.contenedor = QVBoxLayout()
        self.contenedor.setAlignment(Qt.AlignCenter)

        # Layout para los controles (como el número de polinomios)
        self.controles = QVBoxLayout()
        self.controles.setSpacing(10)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; }"

        # Etiqueta y spinner para elegir la cantidad de polinomios
        label = QLabel("Cantidad de Polinomios:")
        label.setStyleSheet("font-size: 14px; font-weight: bold; color: #34495e;")
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)  # Número mínimo de polinomios
        self.spin_cantidad.setValue(2)  # Valor inicial en 2 polinomios
        self.spin_cantidad.setStyleSheet(estilo_spin)

        # Agregar el label y el spinner al layout
        self.controles.addWidget(label, alignment=Qt.AlignCenter)
        self.controles.addWidget(self.spin_cantidad, alignment=Qt.AlignCenter)
        self.contenedor.addLayout(self.controles)

        # Botón para generar los campos de los polinomios
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
        # Conectar el botón a la función que genera los campos
        self.btn_generar.clicked.connect(self.generar_campos)
        self.contenedor.addWidget(self.btn_generar, alignment=Qt.AlignCenter)

        # Layout para los campos de entrada de los polinomios
        self.campos_layout = QFormLayout()
        self.contenedor.addLayout(self.campos_layout)

        # Botón para multiplicar los polinomios
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
        # Conectar el botón a la función que realiza la multiplicación
        self.btn_multiplicar.clicked.connect(self.multiplicar_polinomios)
        self.contenedor.addWidget(self.btn_multiplicar, alignment=Qt.AlignCenter)

        # Campo para mostrar el resultado de la multiplicación
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.contenedor.addWidget(self.resultado)

        # Botón para volver al menú anterior
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
        # Conectar el botón "Volver" al callback para regresar
        self.btn_volver.clicked.connect(self.volver_callback)
        self.contenedor.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

        # Agregar todo el contenedor al layout principal
        self.layout.addLayout(self.contenedor)
        self.campos = []  # Lista para almacenar los campos de entrada de los polinomios

    # Método para generar los campos de entrada para los polinomios
    def generar_campos(self):
        # Eliminar los campos existentes antes de generar nuevos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()

        cantidad = self.spin_cantidad.value()  # Obtener la cantidad de polinomios
        # Crear los campos de texto para los polinomios
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Polinomio {i+1} (ej: x^2 + 3x - 4)")
            campo.setStyleSheet("padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Polinomio {i+1}:", campo)
            self.campos.append(campo)

    # Método para multiplicar los polinomios
    def multiplicar_polinomios(self):
        try:
            # Comenzar con el valor "1" (identidad multiplicativa)
            producto = sympify("1")
            for campo in self.campos:
                texto = campo.text().strip().lower()
                # Asegurarse de que la multiplicación se aplique correctamente (ej: "3x" → "3*x")
                texto = re.sub(r"(?<=\d)(?=[a-z])", "*", texto)  # 3x → 3*x
                producto *= sympify(texto)  # Multiplicar el polinomio actual con el producto acumulado
            # Mostrar el resultado simplificado
            self.resultado.setText(str(simplify(producto)))
        except Exception:
            # Si hay algún error (como una expresión inválida), mostrar mensaje de error
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

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 1")
        self.entrada.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 6px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 6px;
                min-width: 280px;
            }
        """)
        self.layout.addWidget(self.entrada, alignment=Qt.AlignCenter)

        self.variable_input = QLineEdit()
        self.variable_input.setPlaceholderText("Variable (ej: x)")
        self.variable_input.setMaxLength(1)
        self.variable_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                padding: 6px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 6px;
                min-width: 100px;
            }
        """)
        self.layout.addWidget(self.variable_input, alignment=Qt.AlignCenter)

        self.boton = QPushButton("Derivar")
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
        self.boton.clicked.connect(self.derivar)
        self.layout.addWidget(self.boton, alignment=Qt.AlignCenter)

        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("""
            QLineEdit {
                background-color: #ecf0f1;
                font-weight: bold;
                font-size: 16px;
                border: 1px solid #bbb;
                border-radius: 6px;
                padding: 6px;
                min-width: 300px;
            }
        """)
        self.layout.addWidget(self.resultado, alignment=Qt.AlignCenter)

        self.btn_volver = QPushButton("Volver")
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
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver, alignment=Qt.AlignCenter)

    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var_texto = self.variable_input.text().strip().lower()

        if not texto or not var_texto:
            QMessageBox.warning(self, "Error", "Debes ingresar un polinomio y una variable.")
            return

        if not re.fullmatch(r"[a-z]", var_texto):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
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
            texto = self.formatear_expresion(texto)
            expr = sympify(texto)
            simb = symbols(var)

            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            integral = integrate(expr, simb)
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")
    
    def formatear_expresion(self, texto):
        # Reemplaza potencias con símbolo ^ por **
        texto = re.sub(r'(\w)\^(\d+)', r'\1**\2', texto)

        # Inserta * entre número y letra (2x -> 2*x)
        texto = re.sub(r'(?<=\d)(?=[a-zA-Z])', '*', texto)

        # Inserta * entre letra y letra (xy -> x*y)
        texto = re.sub(r'(?<=[a-zA-Z])(?=[a-zA-Z])', '*', texto)

        # Inserta * entre variable/potencia y paréntesis (x(y+1) -> x*(y+1))
        texto = re.sub(r'(?<=[a-zA-Z0-9\)])(?=\()', '*(', texto)

        return texto

# ------------------------- CLASE VISTA EVALUACIÓN POLINOMIOS -------------------------
class VistaEvaluacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        # Callback para volver al menú anterior
        self.volver_callback = volver_callback
        # Establecer el estilo de la vista
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        # Crear un layout vertical para la ventana principal
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("📊 Evaluación de Polinomios")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de texto para ingresar el polinomio
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        # Campo de texto para ingresar la variable
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.variable)

        # Campo de texto para ingresar el valor numérico
        self.valor = QLineEdit()
        self.valor.setPlaceholderText("Valor numérico (ej: 2)")
        self.valor.setStyleSheet("padding: 6px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.valor)

        # Botón para evaluar el polinomio
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

        # Campo de texto para mostrar el resultado de la evaluación
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setAlignment(Qt.AlignCenter)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
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

    # Método para evaluar el polinomio
    def evaluar(self):
        texto = self.entrada.text().strip().lower()  # Obtener el texto del polinomio
        var = self.variable.text().strip().lower()  # Obtener la variable
        val = self.valor.text().strip()  # Obtener el valor numérico

        # Verificar que se haya ingresado el polinomio, la variable y el valor
        if not texto or not var or not val:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Verificar que la variable sea una sola letra (ej: x, y, z)
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Convertir el valor numérico a tipo float
            val = float(val)
        except ValueError:
            QMessageBox.warning(self, "Error", "El valor de evaluación debe ser un número.")
            return

        try:
            # Reemplazar potencias con símbolo ^ por ** y añadir multiplicación entre número y variable
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)
            expr = sympify(texto)  # Convertir el texto del polinomio en una expresión simbólica
            simb = symbols(var)  # Crear el símbolo de la variable

            # Verificar que la variable esté en el polinomio
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Evaluar el polinomio al sustituir el valor en la variable
            resultado = expr.subs(simb, val)
            # Mostrar el resultado de la evaluación
            self.resultado.setText(str(resultado))
        except Exception:
            # Si ocurre un error (por ejemplo, sintaxis incorrecta), mostrar un mensaje de error
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE SUBMENÚSVECTORES -------------------------
class SubmenuVectores(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_resta, go_to_magnitud, go_to_producto_punto, go_to_producto_cruzado, menu_widget):
        # Llamamos al constructor de la clase base (SubmenuBase) y pasamos los parámetros necesarios
        super().__init__(stack, menu_widget)
        # Guardamos las funciones que se ejecutarán al hacer clic en cada botón
        self.go_to_suma = go_to_suma
        self.go_to_resta = go_to_resta
        self.go_to_magnitud = go_to_magnitud
        self.go_to_producto_punto = go_to_producto_punto
        self.go_to_producto_cruzado = go_to_producto_cruzado
        # Inicializamos la interfaz gráfica
        self.init_ui()

    def init_ui(self):
        # Layout principal de la ventana
        layout = QVBoxLayout(self)

        # Título del submenú
        title = QLabel("Operaciones con Vectores")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #3b3f42;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Layout para las operaciones en forma de cuadrícula
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        # Definir las operaciones disponibles junto con su icono
        operaciones = [
            ("Suma", obtener_ruta_recurso(os.path.join("imagenes", "suma.png"))),
            ("Resta", obtener_ruta_recurso(os.path.join("imagenes", "resta.png"))),
            ("Magnitud", obtener_ruta_recurso(os.path.join("imagenes", "magnitud.png"))),
            ("Producto Punto", obtener_ruta_recurso(os.path.join("imagenes", "punto.png"))),
            ("Producto Cruzado", obtener_ruta_recurso(os.path.join("imagenes", "cruzado.png"))),
        ]


        # Crear los botones para cada operación y asignarles el ícono y texto correspondiente
        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))  # Tamaño del ícono
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # Estilo del texto bajo el ícono
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
            # Asignar la acción correspondiente a cada botón al hacer clic
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
            # Si la operación no está definida, mostramos un mensaje de información
            else:
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Vectores", f"Operación: {x}"))
            # Añadir el botón al layout de la cuadrícula (grid)
            grid.addWidget(btn, idx // 3, idx % 3)

        # Añadir el grid de botones al layout principal
        layout.addLayout(grid)

        # Espacio adicional debajo de las operaciones
        layout.addSpacing(30)

        # Botón para volver al menú principal
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
        # Asignar la acción del botón de "Volver al Menú"
        volver_btn.clicked.connect(self.go_back)
        # Añadir el botón al layout
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

# ------------------------- CLASE VISTA SUMA VECTORES -------------------------
class VistaSumaVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función de retroceso (callback) para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("➕ Suma de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout secundario para el selector de cantidad de vectores
        self.selector_layout = QVBoxLayout()

        # Selector para la cantidad de vectores (mínimo 2)
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)  # Valor inicial es 2
        self.spin_cantidad.setStyleSheet("background-color: white; padding: 4px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.selector_layout.addWidget(QLabel("Cantidad de Vectores:"))
        self.selector_layout.addWidget(self.spin_cantidad)

        # Botón para generar los campos para ingresar los vectores
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.clicked.connect(self.generar_campos)  # Conecta al método generar_campos
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

        # Layout para los campos de entrada de los vectores
        self.campos_layout = QFormLayout()
        self.layout.addLayout(self.campos_layout)

        # Botón para realizar la suma de los vectores
        self.btn_sumar = QPushButton("Sumar Vectores")
        self.btn_sumar.clicked.connect(self.sumar_vectores)  # Conecta al método sumar_vectores
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

        # Campo para mostrar el resultado de la suma
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)  # Solo lectura, no puede modificar el resultado
        self.resultado.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)  # Conecta al callback para volver
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

        # Lista para almacenar los campos de texto (vectores)
        self.campos = []

    def generar_campos(self):
        """
        Genera los campos de entrada para los vectores según la cantidad seleccionada.
        Elimina los campos previos antes de generar nuevos.
        """
        # Elimina los widgets existentes en el layout de campos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()  # Limpia la lista de campos

        cantidad = self.spin_cantidad.value()  # Obtiene la cantidad de vectores seleccionada
        # Genera los campos de texto para cada vector
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Vector {i+1} (ej: 1,2,3 o 4,+5,-6)")  # Placeholder para cada vector
            campo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Vector {i+1}:", campo)  # Añade cada campo al layout
            self.campos.append(campo)  # Añade el campo a la lista de campos

    def sumar_vectores(self):
        """
        Suma los vectores ingresados por el usuario.
        Si ocurre algún error (vectores de diferente longitud, entradas inválidas), muestra un mensaje de error.
        """
        try:
            vectores = []
            # Convierte los textos de los campos a listas de números
            for campo in self.campos:
                texto = campo.text().strip().replace(" ", "")  # Elimina espacios y obtiene el texto
                vector = self.convertir_a_numerico(texto)  # Convierte el texto a un vector numérico
                vectores.append(vector)

            longitud = len(vectores[0])  # Longitud del primer vector
            for vector in vectores:
                if len(vector) != longitud:  # Verifica si todos los vectores tienen la misma longitud
                    raise ValueError("Todos los vectores deben tener la misma cantidad de componentes.")

            # Suma los vectores componente por componente
            suma = [sum(x) for x in zip(*vectores)]
            self.resultado.setText(str(suma))  # Muestra el resultado en el campo de texto

        except Exception as e:
            # Si ocurre un error, muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al sumar los vectores: {str(e)}")

    def convertir_a_numerico(self, texto):
        """
        Convierte una cadena de texto a un vector numérico.
        La cadena debe estar en formato "1,2,3" o "4,+5,-6".
        """
        try:
            elementos = texto.split(",")  # Divide el texto por comas
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  # Verifica que el valor sea válido
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))  # Convierte el valor a flotante y lo añade al vector
            return vector
        except Exception:
            # Si la conversión falla, lanza un error
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        """
        Verifica si un valor puede ser convertido a un número flotante.
        """
        try:
            float(valor)  # Intenta convertir el valor a flotante
            return True
        except ValueError:
            return False  # Si no se puede convertir, no es válido
        
# ------------------------- CLASE VISTA RESTA VECTORES -------------------------
class VistaRestaVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función de retroceso (callback) para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("➖ Resta de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Layout secundario para el selector de cantidad de vectores
        self.selector_layout = QVBoxLayout()

        # Selector para la cantidad de vectores (mínimo 2)
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setMinimum(2)
        self.spin_cantidad.setValue(2)  # Valor inicial es 2
        self.spin_cantidad.setStyleSheet("background-color: white; padding: 4px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.selector_layout.addWidget(QLabel("Cantidad de Vectores:"))
        self.selector_layout.addWidget(self.spin_cantidad)

        # Botón para generar los campos para ingresar los vectores
        self.btn_generar = QPushButton("Generar Campos")
        self.btn_generar.clicked.connect(self.generar_campos)  # Conecta al método generar_campos
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

        # Layout para los campos de entrada de los vectores
        self.campos_layout = QFormLayout()
        self.layout.addLayout(self.campos_layout)

        # Botón para realizar la resta de los vectores
        self.btn_rest = QPushButton("Restar Vectores")
        self.btn_rest.clicked.connect(self.restar_vectores)  # Conecta al método restar_vectores
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

        # Campo para mostrar el resultado de la resta
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)  # Solo lectura, no puede modificar el resultado
        self.resultado.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)  # Conecta al callback para volver
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

        # Lista para almacenar los campos de texto (vectores)
        self.campos = []

    def generar_campos(self):
        """
        Genera los campos de entrada para los vectores según la cantidad seleccionada.
        Elimina los campos previos antes de generar nuevos.
        """
        # Elimina los widgets existentes en el layout de campos
        for i in reversed(range(self.campos_layout.count())):
            widget = self.campos_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.campos.clear()  # Limpia la lista de campos

        cantidad = self.spin_cantidad.value()  # Obtiene la cantidad de vectores seleccionada
        # Genera los campos de texto para cada vector
        for i in range(cantidad):
            campo = QLineEdit()
            campo.setPlaceholderText(f"Vector {i+1} (ej: 1,2,3 o 4,+5,-6)")  # Placeholder para cada vector
            campo.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
            self.campos_layout.addRow(f"Vector {i+1}:", campo)  # Añade cada campo al layout
            self.campos.append(campo)  # Añade el campo a la lista de campos

    def restar_vectores(self):
        """
        Resta los vectores ingresados por el usuario.
        Si ocurre algún error (vectores de diferente longitud, entradas inválidas), muestra un mensaje de error.
        """
        try:
            vectores = []
            # Convierte los textos de los campos a listas de números
            for campo in self.campos:
                texto = campo.text().strip().replace(" ", "")  # Elimina espacios y obtiene el texto
                vector = self.convertir_a_numerico(texto)  # Convierte el texto a un vector numérico
                vectores.append(vector)

            longitud = len(vectores[0])  # Longitud del primer vector
            for vector in vectores:
                if len(vector) != longitud:  # Verifica si todos los vectores tienen la misma longitud
                    raise ValueError("Todos los vectores deben tener la misma cantidad de componentes.")

            # Resta los vectores componente por componente
            resta = vectores[0]
            for v in vectores[1:]:
                resta = [a - b for a, b in zip(resta, v)]  # Resta los componentes correspondientes

            self.resultado.setText(str(resta))  # Muestra el resultado en el campo de texto

        except Exception as e:
            # Si ocurre un error, muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al restar los vectores: {str(e)}")

    def convertir_a_numerico(self, texto):
        """
        Convierte una cadena de texto a un vector numérico.
        La cadena debe estar en formato "1,2,3" o "4,+5,-6".
        """
        try:
            elementos = texto.split(",")  # Divide el texto por comas
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  # Verifica que el valor sea válido
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))  # Convierte el valor a flotante y lo añade al vector
            return vector
        except Exception:
            # Si la conversión falla, lanza un error
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        """
        Verifica si un valor puede ser convertido a un número flotante.
        """
        try:
            float(valor)  # Intenta convertir el valor a flotante
            return True
        except ValueError:
            return False  # Si no se puede convertir, no es válido

# ------------------------- CLASE VISTA MAGNITUD VECTORES -------------------------
class VistaMagnitudVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("🔢 Magnitud de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para ingresar el vector
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: 3,4 o 1,2,3")  # Ejemplo de formato de entrada
        self.entrada.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada)

        # Botón para calcular la magnitud del vector
        self.boton = QPushButton("Calcular Magnitud")
        self.boton.clicked.connect(self.calcular_magnitud)  # Conecta al método calcular_magnitud
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

        # Campo para mostrar el resultado de la magnitud
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)  # Solo lectura, no puede modificar el resultado
        self.resultado.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)  # Conecta al callback para volver
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
        """
        Calcula la magnitud de un vector ingresado por el usuario.
        La magnitud se calcula utilizando la fórmula sqrt(x1^2 + x2^2 + ... + xn^2).
        """
        try:
            texto = self.entrada.text().strip().replace(" ", "")  # Obtiene el texto ingresado, eliminando espacios
            vector = self.convertir_a_numerico(texto)  # Convierte el texto a un vector numérico
            # Calcula la magnitud utilizando la fórmula de la norma Euclidiana
            magnitud = sum([x ** 2 for x in vector]) ** 0.5
            self.resultado.setText(f"MAGNITUD: {magnitud}")  # Muestra el resultado de la magnitud
        except Exception as e:
            # Si ocurre un error (por ejemplo, formato de entrada inválido), muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al calcular la magnitud: {str(e)}")

    def convertir_a_numerico(self, texto):
        """
        Convierte una cadena de texto a un vector numérico.
        La cadena debe estar en formato "1,2,3" o "4,+5,-6".
        """
        try:
            elementos = texto.split(",")  # Divide el texto por comas
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  # Verifica que el valor sea válido
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))  # Convierte el valor a flotante y lo añade al vector
            return vector
        except Exception:
            # Si la conversión falla, lanza un error
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        """
        Verifica si un valor puede ser convertido a un número flotante.
        """
        try:
            float(valor)  # Intenta convertir el valor a flotante
            return True
        except ValueError:
            return False  # Si no se puede convertir, no es válido

# ------------------------- CLASE VISTA PRODUCTO PUNTO VECTORES -------------------------
class VistaProductoPuntoVectores(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback  # Función para volver al menú anterior
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")  # Establece el color de fondo y la fuente

        # Layout principal que organiza los widgets de manera vertical
        self.layout = QVBoxLayout(self)

        # Título de la ventana
        self.titulo = QLabel("⚡ Producto Punto de Vectores")
        self.titulo.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para el primer vector
        self.entrada_vector1 = QLineEdit()
        self.entrada_vector1.setPlaceholderText("Vector 1 (ej: 1, 2, 3)")  # Ejemplo de formato de entrada
        self.entrada_vector1.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector1)

        # Campo de entrada para el segundo vector
        self.entrada_vector2 = QLineEdit()
        self.entrada_vector2.setPlaceholderText("Vector 2 (ej: 4, 5, 6)")  # Ejemplo de formato de entrada
        self.entrada_vector2.setStyleSheet("padding: 6px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.entrada_vector2)

        # Botón para calcular el producto punto de los dos vectores
        self.boton = QPushButton("Calcular Producto Punto")
        self.boton.clicked.connect(self.calcular_producto_punto)  # Conecta al método calcular_producto_punto
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

        # Campo para mostrar el resultado del producto punto
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)  # Solo lectura, no puede modificar el resultado
        self.resultado.setAlignment(Qt.AlignCenter)  # Centra el texto
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px; border: 1px solid #ccc; border-radius: 5px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)  # Conecta al callback para volver
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
        """
        Calcula el producto punto entre dos vectores ingresados por el usuario.
        El producto punto se calcula con la fórmula: (x1 * y1) + (x2 * y2) + ... + (xn * yn).
        """
        try:
            # Obtiene los textos ingresados por el usuario para los dos vectores
            texto_vector1 = self.entrada_vector1.text().strip().replace(" ", "")  # Elimina los espacios y obtiene el texto
            texto_vector2 = self.entrada_vector2.text().strip().replace(" ", "")  # Elimina los espacios y obtiene el texto

            # Convierte los textos en vectores numéricos
            vector1 = self.convertir_a_numerico(texto_vector1)
            vector2 = self.convertir_a_numerico(texto_vector2)

            # Verifica que los vectores tengan la misma longitud
            if len(vector1) != len(vector2):
                raise ValueError("Los vectores deben tener la misma cantidad de componentes.")

            # Calcula el producto punto utilizando la fórmula (x1 * y1) + (x2 * y2) + ... + (xn * yn)
            producto_punto = sum(x * y for x, y in zip(vector1, vector2))

            # Muestra el resultado en el campo de resultado
            self.resultado.setText(f"Producto Punto: {producto_punto}")

        except Exception as e:
            # Si ocurre un error (por ejemplo, vectores de diferente tamaño o formato incorrecto), muestra un mensaje de error
            QMessageBox.critical(self, "Error", f"Error al calcular el producto punto: {str(e)}")

    def convertir_a_numerico(self, texto):
        """
        Convierte una cadena de texto a un vector numérico.
        La cadena debe estar en formato "1,2,3" o "4,+5,-6".
        """
        try:
            elementos = texto.split(",")  # Divide el texto por comas
            vector = []
            for elem in elementos:
                if not self.es_valido(elem):  # Verifica que el valor sea válido
                    raise ValueError(f"El valor '{elem}' no es válido.")
                vector.append(float(elem))  # Convierte el valor a flotante y lo añade al vector
            return vector
        except Exception:
            # Si la conversión falla, lanza un error
            raise ValueError(f"La entrada '{texto}' no es un vector válido.")

    def es_valido(self, valor):
        """
        Verifica si un valor puede ser convertido a un número flotante.
        """
        try:
            float(valor)  # Intenta convertir el valor a flotante
            return True
        except ValueError:
            return False  # Si no se puede convertir, no es válido
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
    def __init__(self, stack, go_to_2d, go_to_3d, menu_widget):
        # Inicializa la clase base con el stack y el widget del menú
        super().__init__(stack, menu_widget)
        
        # Guarda las funciones que se ejecutarán al presionar los botones
        self.go_to_2d = go_to_2d
        self.go_to_3d = go_to_3d

        # Inicializa la interfaz de usuario
        self.init_ui()

    def init_ui(self):
        # Layout principal vertical
        layout = QVBoxLayout(self)

        # Título del submenú
        title = QLabel("Gráficas 2D y 3D")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #5d6d7e;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Layout en forma de cuadrícula para los botones
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        # Lista de operaciones disponibles con su texto e icono
        operaciones = [
            ("Función 2D", obtener_ruta_recurso(os.path.join("imagenes", "2d.png"))),
            ("Curva 3D", obtener_ruta_recurso(os.path.join("imagenes", "3d.png"))),
        ]


        # Crear botones para cada operación
        for idx, (texto, icono) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(icono))
            btn.setIconSize(QSize(40, 40))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

            # Estilo del botón
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

            # Conectar cada botón a su respectiva función
            if texto == "Función 2D":
                btn.clicked.connect(self.go_to_2d)
            elif texto == "Curva 3D":
                btn.clicked.connect(self.go_to_3d)
            else:
                # Este bloque no se usa por ahora, pero sirve como fallback
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Gráficas", f"Operación: {x}"))

            # Añadir el botón al grid
            grid.addWidget(btn, idx // 3, idx % 3)

        # Añadir el grid al layout principal
        layout.addLayout(grid)
        layout.addSpacing(30)  # Espacio debajo del grid

        # Botón para volver al menú principal
        volver_btn = QToolButton()
        volver_btn.setText("Volver al Menú")
        volver_btn.setIcon(QIcon("imagenes/salir.png"))
        volver_btn.setIconSize(QSize(24, 24))
        volver_btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Estilo del botón "Volver"
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

        # Conectar el botón a la función que navega al menú anterior
        volver_btn.clicked.connect(self.go_back)

        # Añadir el botón al layout
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

#------------------------- CLASE VISTA GRAFICA 2D -------------------------
class VistaGrafica2D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función para volver al menú anterior
        self.volver_callback = volver_callback

        # Estilo general del fondo y fuente
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la sección
        self.titulo = QLabel("📊 Gráfica 2D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función
        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + 2x + 1)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        # Campo de entrada para el rango de x
        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x (ej: -10,10)")
        self.rango_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.rango_input)

        # Botón para graficar
        self.btn_graficar = QPushButton("Graficar")
        self.btn_graficar.clicked.connect(self.graficar)
        self.btn_graficar.setStyleSheet(
            "padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;"
        )
        self.layout.addWidget(self.btn_graficar)

        # Botón para volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

        # Sección para mostrar la gráfica
        self.figure = plt.figure(figsize=(5, 3))  # Crear figura de Matplotlib
        self.canvas = FigureCanvas(self.figure)   # Integrar con PyQt5
        self.layout.addWidget(self.canvas)

    # Función para graficar la expresión ingresada
    def graficar(self):
        try:
            # Obtener texto de entradas
            funcion = self.funcion_input.text().strip()
            rango = self.rango_input.text().strip()

            # Validar el formato del rango
            if "," not in rango:
                raise ValueError("El rango debe tener el formato: -5,5")

            # Separar valores del rango
            partes = rango.split(",")
            x_min = float(partes[0])
            x_max = float(partes[1])

            # Reemplazar notaciones implícitas (ej: 3x -> 3*x)
            funcion = re.sub(r'(?<=\d)(?=x)', '*', funcion)

            # Preparar la expresión simbólica
            x = symbols('x')
            expr = sympify(funcion)  # Convertir texto a expresión simbólica
            f = lambdify(x, expr, 'numpy')  # Crear función evaluable

            # Generar valores de x y evaluar la función
            x_vals = np.linspace(x_min, x_max, 200)
            y_vals = f(x_vals)

            # Limpiar gráfica anterior
            self.figure.clear()
            ax = self.figure.add_subplot(111)  # Agregar nuevo eje

            # Dibujar la gráfica
            ax.plot(x_vals, y_vals, label=str(expr))
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title(f"Gráfica de {funcion}")
            ax.grid(True)
            ax.legend()

            # Mostrar la nueva gráfica
            self.canvas.draw()

        except Exception as e:
            # Mostrar mensaje de error si algo falla
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")
#-------------------------- CLASE VISTA GRAFICA 3D -------------------------
class VistaGrafica3D(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Callback para volver al menú anterior
        self.volver_callback = volver_callback

        # Estilo general de fondo y fuente
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título del panel
        self.titulo = QLabel("📊 Gráfica 3D")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo para ingresar la función (con x e y)
        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingresa la función (ej: x^2 + y^2)")
        self.funcion_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.funcion_input)

        # Campo para ingresar el rango de x e y
        self.rango_input = QLineEdit()
        self.rango_input.setPlaceholderText("Rango de x, y (ej: -10,10)")
        self.rango_input.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.rango_input)

        # Botón para graficar
        self.btn_graficar = QPushButton("Graficar")
        self.btn_graficar.clicked.connect(self.graficar)
        self.btn_graficar.setStyleSheet(
            "padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;"
        )
        self.layout.addWidget(self.btn_graficar)

        # Botón para volver
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

        # Área para la gráfica
        self.figure = plt.figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

    # Función para graficar la expresión ingresada
    def graficar(self):
        try:
            # Obtener función y limpiar entrada
            funcion = self.funcion_input.text().strip().lower().replace("^", "**")
            rango = self.rango_input.text().strip()

            # Separar y validar el rango
            partes = rango.split(",")
            if len(partes) != 2:
                raise ValueError("El rango debe tener dos números separados por coma.")

            x_min = float(partes[0])
            x_max = float(partes[1])
            y_min = x_min  # Se usa el mismo rango para y
            y_max = x_max

            # Generar la malla de valores x, y
            x = np.linspace(x_min, x_max, 100)
            y = np.linspace(y_min, y_max, 100)
            X, Y = np.meshgrid(x, y)

            # Crear símbolos y convertir la expresión
            x_sym, y_sym = symbols("x y")
            expr = sympify(funcion)
            f = lambdify((x_sym, y_sym), expr, "numpy")

            # Evaluar la función en la malla
            Z = f(X, Y)

            # Limpiar gráfica anterior y dibujar la nueva
            self.figure.clear()
            ax = self.figure.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis')
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_zlabel("z")
            ax.set_title(f"Gráfica de {funcion}")
            self.canvas.draw()

        except Exception as e:
            # Mostrar error si ocurre algún problema
            QMessageBox.critical(self, "Error", f"Error al graficar: {str(e)}")

# ------------------------- CLASE SUBMENÚ CÁLCULO -------------------------
# Submenú para las operaciones de cálculo: derivadas e integrales
class SubmenuCalculo(SubmenuBase):
    def __init__(self, stack, go_to_derivada, go_to_integral_indefinida, go_to_integral_definida, menu_widget):
        # Llama al constructor de la clase base
        super().__init__(stack, menu_widget)

        # Callbacks para navegar a cada vista
        self.go_to_derivada = go_to_derivada
        self.go_to_integral_indefinida = go_to_integral_indefinida
        self.go_to_integral_definida = go_to_integral_definida

        # Inicializa la interfaz
        self.init_ui()

    def init_ui(self):
        # Layout vertical principal del submenú
        layout = QVBoxLayout(self)

        # Título del submenú
        title = QLabel("Operaciones de Cálculo")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f618d;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Grid para colocar los botones de operaciones
        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        # Lista de operaciones con texto e icono
        operaciones = [
            ("Derivada", obtener_ruta_recurso(os.path.join("imagenes", "derivada.png"))),
            ("Integral Indefinida", obtener_ruta_recurso(os.path.join("imagenes", "integral.png"))),
            ("Integral Definida", obtener_ruta_recurso(os.path.join("imagenes", "definida.png"))),
        ]


        # Crear botones a partir de las operaciones
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

            # Asignar acción según el botón
            if texto == "Integral Definida":
                btn.clicked.connect(self.go_to_integral_definida)
            elif texto == "Integral Indefinida":
                btn.clicked.connect(self.go_to_integral_indefinida)
            elif texto == "Derivada":
                btn.clicked.connect(self.go_to_derivada)
            else:
                # Mensaje por defecto si se añade otra operación no esperada
                btn.clicked.connect(lambda _, x=texto: QMessageBox.information(self, "Cálculo", f"Operación: {x}"))

            # Añadir el botón al grid
            grid.addWidget(btn, idx // 3, idx % 3)

        # Añadir el grid al layout principal
        layout.addLayout(grid)
        layout.addSpacing(30)

        # Botón para volver al menú principal
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
        volver_btn.clicked.connect(self.go_back)  # Vuelve al menú anterior
        layout.addWidget(volver_btn, alignment=Qt.AlignCenter)

# ------------------------- CLASE VISTA INTEGRAL DEFINIDA -------------------------
# Vista para calcular la integral definida de una función ingresada por el usuario
class VistaIntegralDefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función que se llamará cuando el usuario presione "Volver"
        self.volver_callback = volver_callback

        # Estilo general de la ventana
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("∫ Integral Definida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo para la expresión matemática
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para indicar la variable de integración (por ejemplo, x)
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Campo para el límite inferior de integración
        self.limite_inferior = QLineEdit()
        self.limite_inferior.setPlaceholderText("Límite inferior (ej: 0)")
        self.limite_inferior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_inferior)

        # Campo para el límite superior de integración
        self.limite_superior = QLineEdit()
        self.limite_superior.setPlaceholderText("Límite superior (ej: 5)")
        self.limite_superior.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.limite_superior)

        # Botón para calcular la integral
        self.boton = QPushButton("Calcular Integral Definida")
        self.boton.clicked.connect(self.integrar_definida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #3498db; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado (solo lectura)
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función que realiza el cálculo de la integral definida
    def integrar_definida(self):
        # Obtiene y limpia los datos ingresados
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()
        inferior = self.limite_inferior.text().strip()
        superior = self.limite_superior.text().strip()

        # Validaciones básicas
        if not texto or not var or not inferior or not superior:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Verifica que la variable sea una letra válida
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        # Verifica que los límites sean números reales válidos
        if not re.fullmatch(r"[-+]?\d+(\.\d+)?", inferior) or not re.fullmatch(r"[-+]?\d+(\.\d+)?", superior):
            QMessageBox.warning(self, "Error", "Los límites deben ser números reales válidos.")
            return

        try:
            # Convierte expresiones como "3x" en "3*x"
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Intenta simbolizar la expresión y calcular la integral definida
            expr = sympify(texto)
            simb = symbols(var)
            a = float(inferior)
            b = float(superior)
            integral_definida = integrate(expr, (simb, a, b))

            # Muestra el resultado
            self.resultado.setText(str(integral_definida))
        except Exception:
            # Si hay algún error, muestra un mensaje
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE VISTA INTEGRAL INDEFINIDA -------------------------
# Vista para calcular la integral indefinida de una expresión simbólica
class VistaIntegralIndefinida(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Función que se llama al presionar "Volver"
        self.volver_callback = volver_callback

        # Estilo general de la ventana
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Layout principal vertical
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("∫ Integral Indefinida")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: x^2 + 3x + 2")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para especificar la variable de integración (como "x")
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Botón para realizar la integración
        self.boton = QPushButton("Integrar")
        self.boton.clicked.connect(self.integrar_indefinida)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #27ae60; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo para mostrar el resultado de la integral (solo lectura)
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para regresar al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función para calcular la integral indefinida
    def integrar_indefinida(self):
        # Se obtiene y limpia el texto ingresado
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        # Verifica que ambos campos estén llenos
        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        # Verifica que la variable sea una sola letra válida
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Convierte cosas como "3x" en "3*x" para que sympy lo entienda
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Convierte el texto en una expresión simbólica
            expr = sympify(texto)
            simb = symbols(var)

            # Verifica que la variable aparezca en la expresión
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Realiza la integración simbólica
            integral = integrate(expr, simb)

            # Muestra el resultado con la constante "+ C"
            self.resultado.setText(str(integral) + " + C")
        except Exception:
            # Si algo falla, muestra un error genérico
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 2")

# ------------------------- CLASE VISTA DERIVACIÓN POLINOMIOS -------------------------
# Vista para derivar expresiones simbólicas
class VistaDerivacionPolinomios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()

        # Callback para regresar al menú anterior
        self.volver_callback = volver_callback

        # Estilo visual general
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.layout = QVBoxLayout(self)

        # Título de la vista
        self.titulo = QLabel("📐 Derivación")
        self.titulo.setAlignment(Qt.AlignCenter)
        self.titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        self.layout.addWidget(self.titulo)

        # Campo de entrada para la función a derivar
        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Ej: sin(x) + ln(x^2) + x^3")
        self.entrada.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.entrada)

        # Campo para ingresar la variable de derivación
        self.variable = QLineEdit()
        self.variable.setPlaceholderText("Variable (ej: x)")
        self.variable.setMaxLength(1)  # Solo permite una letra
        self.variable.setStyleSheet("padding: 6px; font-size: 16px;")
        self.layout.addWidget(self.variable)

        # Botón para ejecutar la derivación
        self.boton = QPushButton("Derivar")
        self.boton.clicked.connect(self.derivar)
        self.boton.setStyleSheet("padding: 8px; font-size: 15px; background-color: #2980b9; color: white; border-radius: 6px;")
        self.layout.addWidget(self.boton)

        # Campo de salida para mostrar el resultado
        self.resultado = QLineEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background-color: #ecf0f1; font-weight: bold; font-size: 16px; padding: 6px;")
        self.layout.addWidget(self.resultado)

        # Botón para volver al menú anterior
        self.btn_volver = QPushButton("Volver")
        self.btn_volver.clicked.connect(self.volver_callback)
        self.layout.addWidget(self.btn_volver)

    # Función que ejecuta la derivación
    def derivar(self):
        texto = self.entrada.text().strip().lower()
        var = self.variable.text().strip().lower()

        # Validación de campos vacíos
        if not texto or not var:
            QMessageBox.warning(self, "Error", "Ambos campos son obligatorios.")
            return

        # Validación de la variable (solo una letra)
        if not re.fullmatch(r"[a-z]", var):
            QMessageBox.warning(self, "Error", "La variable debe ser una sola letra.")
            return

        try:
            # Ajusta expresiones como 3x → 3*x para que sympy lo interprete bien
            texto = re.sub(r'(?<=\d)(?=[a-z])', '*', texto)

            # Convierte el texto en una expresión simbólica
            expr = sympify(texto)
            simb = symbols(var)

            # Verifica que la variable esté presente en la expresión
            if simb not in expr.free_symbols:
                QMessageBox.warning(self, "Error", f"La variable '{var}' no se encuentra en el polinomio.")
                return

            # Calcula la derivada
            derivada = diff(expr, simb)

            # Muestra el resultado
            self.resultado.setText(str(derivada))
        except Exception:
            # Si hay un error en la expresión, muestra un mensaje
            QMessageBox.critical(self, "Error", "Expresión inválida. Usa una forma como: x^2 + 3x + 1")

#-------------------------------- CLASE VISTA ACERCA DE -------------------------
class AcercaDe(SubmenuBase):
    def __init__(self, stack, menu_widget):
        # Inicializa desde la clase base para navegación (stack y botón volver)
        super().__init__(stack, menu_widget)
        self.init_ui()

    def init_ui(self):
        # Layout principal vertical
        layout = QVBoxLayout(self)

        # Estilo general del fondo y fuente
        self.setStyleSheet("font-family: 'Segoe UI'; background-color: #f0f3f4;")

        # Título principal del módulo
        titulo = QLabel("📘 Acerca del Proyecto")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(titulo)

        # --------------------- Cuadro de descripción del proyecto ---------------------
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
        descripcion.setWordWrap(True)  # Para que el texto se ajuste al ancho
        proyecto_layout.addWidget(descripcion)
        layout.addWidget(cuadro_proyecto)

        # --------------------- Cuadro de información personal del autor ---------------------
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
            <b>Materia:</b> Modelos matemáticos y simulación de software<br>
            <b>Año:</b> Abril 2025 - Julio 2025<br>
            </p>
        """)
        info.setAlignment(Qt.AlignCenter)
        autor_layout.addWidget(info)
        layout.addWidget(cuadro_autor)

        # --------------------- Botón para volver al menú principal ---------------------
        volver_btn = QPushButton("⏪ Volver al Menú Principal")
        volver_btn.clicked.connect(self.go_back)  # Método heredado de SubmenuBase
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

# ------------------------- CLASE VISTA MÉTODOS NUMÉRICOS -------------------------
class VistaMetodosNumericos(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        # Scroll principal
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)

        contenedor = QWidget()
        layout_scroll = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)

        layout_principal = QVBoxLayout(self)
        layout_principal.addWidget(scroll)

        # Título
        titulo = QLabel("📊 Métodos Numéricos para EDO")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout_scroll.addWidget(titulo)

        # Formulario de entradas
        form = QFormLayout()
        estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """
        self.ecuacion_input = QLineEdit()
        self.ecuacion_input.setPlaceholderText("Ej: x*y")
        self.ecuacion_input.setStyleSheet(estilo_input)

        self.x0_input = QLineEdit()
        self.x0_input.setPlaceholderText("Ej: 1")
        self.x0_input.setStyleSheet(estilo_input)

        self.y0_input = QLineEdit()
        self.y0_input.setPlaceholderText("Ej: 2")
        self.y0_input.setStyleSheet(estilo_input)

        self.xf_input = QLineEdit()
        self.xf_input.setPlaceholderText("Ej: 5")
        self.xf_input.setStyleSheet(estilo_input)

        self.h_input = QLineEdit()
        self.h_input.setPlaceholderText("Ej: 0.5")
        self.h_input.setStyleSheet(estilo_input)

        form.addRow("dy/dx =", self.ecuacion_input)
        form.addRow("x₀:", self.x0_input)
        form.addRow("y₀:", self.y0_input)
        form.addRow("x final:", self.xf_input)
        form.addRow("Paso h:", self.h_input)
        layout_scroll.addLayout(form)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)
        botones = [
            ("Euler", "#2980b9"),
            ("Heun", "#16a085"),
            ("RK4", "#8e44ad"),
            ("Taylor orden 2", "#d35400"),
            ("Comparar todos", "#2c3e50")
        ]
        self.btn_euler = QPushButton(botones[0][0])
        self.btn_heun = QPushButton(botones[1][0])
        self.btn_rk4 = QPushButton(botones[2][0])
        self.btn_taylor = QPushButton(botones[3][0])
        self.btn_todos = QPushButton(botones[4][0])

        for btn, (texto, color) in zip(
            [self.btn_euler, self.btn_heun, self.btn_rk4, self.btn_taylor, self.btn_todos], botones
        ):
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color}; color: white;
                    font-size: 14px; padding: 10px 14px; border-radius: 8px;
                    outline: none;
                }}
                QPushButton:hover {{
                    background-color: {color}; opacity: 0.9;
                }}
            """)
            botones_layout.addWidget(btn)

        layout_scroll.addLayout(botones_layout)

        # Gráfica con tabla
        self.canvas = FigureCanvas(plt.Figure(figsize=(6, 5)))
        self.canvas.setMinimumHeight(400)
        self.canvas.setMaximumHeight(500)
        layout_scroll.addWidget(self.canvas)

        # Botón volver
        btn_volver = QPushButton("Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        btn_volver.clicked.connect(self.volver_y_limpiar)
        layout_scroll.addWidget(btn_volver, alignment=Qt.AlignCenter)

        # Conectar botones a funciones
        self.btn_euler.clicked.connect(lambda: self.calcular_y_mostrar("euler"))
        self.btn_heun.clicked.connect(lambda: self.calcular_y_mostrar("heun"))
        self.btn_rk4.clicked.connect(lambda: self.calcular_y_mostrar("rk4"))
        self.btn_taylor.clicked.connect(lambda: self.calcular_y_mostrar("taylor"))
        self.btn_todos.clicked.connect(self.mostrar_comparacion)


    def obtener_datos(self):
        try:
            f = lambdify(symbols('x y'), sympify(self.ecuacion_input.text()), modules=["numpy"])
            x0 = float(self.x0_input.text())
            y0 = float(self.y0_input.text())
            xf = float(self.xf_input.text())
            h = float(self.h_input.text())
            return f, x0, y0, xf, h
        except Exception:
            QMessageBox.critical(self, "Error", "Verifica los valores y la ecuación.")
            return None

    def calcular_y_mostrar(self, metodo):
        datos = self.obtener_datos()
        if not datos:
            return
        f, x0, y0, xf, h = datos
        xs, ys = self.aplicar_metodo(f, x0, y0, xf, h, metodo)
        self.mostrar_grafica([(xs, ys, metodo)])

    def mostrar_comparacion(self):
        datos = self.obtener_datos()
        if not datos:
            return
        f, x0, y0, xf, h = datos
        resultados = []
        for metodo in ["euler", "heun", "rk4", "taylor"]:
            xs, ys = self.aplicar_metodo(f, x0, y0, xf, h, metodo)
            resultados.append((xs, ys, metodo))
        self.mostrar_grafica(resultados)

    def aplicar_metodo(self, f, x0, y0, xf, h, metodo):
        xs = [x0]
        ys = [y0]
        x, y = x0, y0
        while x < xf:
            if metodo == "euler":
                y += h * f(x, y)
            elif metodo == "heun":
                k1 = f(x, y)
                k2 = f(x + h, y + h * k1)
                y += h * (k1 + k2) / 2
            elif metodo == "rk4":
                k1 = f(x, y)
                k2 = f(x + h/2, y + h*k1/2)
                k3 = f(x + h/2, y + h*k2/2)
                k4 = f(x + h, y + h*k3)
                y += (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            elif metodo == "taylor":
                x_sym, y_sym = symbols('x y')
                df = sympify(self.ecuacion_input.text())
                dfdx = diff(df, x_sym)
                dfdy = diff(df, y_sym)
                derivada_total = dfdx + dfdy * df
                f1 = lambdify((x_sym, y_sym), derivada_total, modules=["numpy"])
                y += h * f(x, y) + (h**2 / 2) * f1(x, y)
            x += h
            x = round(x, 10)
            if math.isinf(y) or math.isnan(y):
                QMessageBox.critical(self, "Error numérico", "⚠️ La solución se volvió infinita o inválida.\nReduce el paso o cambia la ecuación.")
                break
            xs.append(x)
            ys.append(y)
        return xs, ys

    def mostrar_grafica(self, datos):
        fig = self.canvas.figure
        fig.clf()
        axs = fig.subplots(2, 1, gridspec_kw={'height_ratios': [2, 1]})

        ax_plot = axs[0]
        colores = ['#FF5733', '#33FFBD', '#3380FF', '#DA33FF']
        for i, (xs, ys, metodo) in enumerate(datos):
            ax_plot.plot(xs, ys, label=metodo, marker='o', linestyle='-', color=colores[i % len(colores)])
        ax_plot.set_title("Comparación de Métodos", fontsize=12, fontweight='bold')
        ax_plot.set_xlabel("x")
        ax_plot.set_ylabel("y")
        ax_plot.grid(True, linestyle="--", alpha=0.5)
        ax_plot.legend()

        ax_tabla = axs[1]
        ax_tabla.axis('off')
        n_filas = min(len(xs) for xs, ys, m in datos)
        max_filas_mostrar = 15
        table_data = []
        for i in range(min(n_filas, max_filas_mostrar)):
            fila = [f"{datos[0][0][i]:.2f}"]
            fila.extend([f"{ys[i]:.4f}" for _, ys, _ in datos])
            table_data.append(fila)
        if n_filas > max_filas_mostrar:
            fila_final = ["..."] + ["..."] * (len(datos))
            table_data.append(fila_final)
        col_labels = ["x"] + [metodo for _, _, metodo in datos]
        tabla = ax_tabla.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center')
        tabla.scale(1.0, 1.15)
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(8)
        for key, cell in tabla.get_celld().items():
            cell.get_text().set_color('black')
        fig.tight_layout()
        self.canvas.draw()

    def volver_y_limpiar(self):
        self.canvas.figure.clf()
        self.canvas.draw()
        self.volver_callback()

# ------------------------- MENÚ DE ALGEBRA -------------------------
class SubmenuAlgebra(QWidget):
    def __init__(self, stack, ir_a_vectores_propios, volver_callback):
        super().__init__()
        self.stack = stack
        self.ir_a_vectores_propios = ir_a_vectores_propios
        self.volver_callback = volver_callback

        layout = QVBoxLayout(self)

        titulo = QLabel("Álgebra Lineal")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(titulo)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        botones = [
            ("Vectores Propios", "vectores.png", self.ir_a_vectores_propios)
        ]

        for i, (texto, icono, funcion) in enumerate(botones):
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(obtener_ruta_recurso(os.path.join("imagenes", icono))))
            btn.setIconSize(QSize(48, 48))
            btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            btn.setStyleSheet("""
                background: #34495e; color: white;
                font-weight: bold; font-size: 14px;
                border-radius: 10px; padding: 15px;
            """)
            btn.clicked.connect(funcion)
            grid.addWidget(btn, i // 2, i % 2)

        layout.addLayout(grid)

        btn_volver = QPushButton("Volver al menú")
        btn_volver.setStyleSheet("""
            background-color: #7f8c8d; color: white;
            font-size: 13px; padding: 8px 20px; border-radius: 6px;
        """)
        btn_volver.clicked.connect(volver_callback)
        layout.addWidget(btn_volver, alignment=Qt.AlignCenter)

# ------------------------- VISTA DE VECTORES PROPIOS -------------------------
class VistaVectoresPropios(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")

        layout = QVBoxLayout(self)

        # Título
        titulo = QLabel("\U0001F522 Valores y vectores Propios")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        layout.addWidget(titulo)

        # Selector de tamaño de matriz
        seleccion_layout = QHBoxLayout()
        seleccion_layout.setSpacing(15)
        estilo_spin = "QSpinBox { background-color: white; padding: 4px; font-size: 14px; border-radius: 4px; }"

        self.spin_filas = QSpinBox()
        self.spin_columnas = QSpinBox()
        for spin in [self.spin_filas, self.spin_columnas]:
            spin.setRange(2, 4)
            spin.setValue(2)
            spin.setStyleSheet(estilo_spin)

        seleccion_layout.addWidget(QLabel("Filas:"))
        seleccion_layout.addWidget(self.spin_filas)
        seleccion_layout.addWidget(QLabel("Columnas:"))
        seleccion_layout.addWidget(self.spin_columnas)

        btn_generar = QPushButton("Generar Matriz")
        btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #5dade2;
            }
        """)
        btn_generar.clicked.connect(self.generar_entradas)
        seleccion_layout.addWidget(btn_generar)
        layout.addLayout(seleccion_layout)

        # Contenedor de entradas
        self.grid_entradas = QGridLayout()
        layout.addLayout(self.grid_entradas)

        # Botón calcular
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_calcular.clicked.connect(self.calcular_vectores)
        layout.addWidget(self.btn_calcular, alignment=Qt.AlignCenter)

        # Resultados
        self.resultado_texto = QLabel()
        self.resultado_texto.setStyleSheet("font-size: 14px; color: #2c3e50; margin: 10px;")
        self.resultado_texto.setWordWrap(True)
        layout.addWidget(self.resultado_texto)

        # Botones de gráficas
        graficas_layout = QHBoxLayout()
        self.btn_grafica_2d = QPushButton("Mostrar Gráfica 2D")
        self.btn_grafica_3d = QPushButton("Mostrar Gráfica 3D")
        for btn in [self.btn_grafica_2d, self.btn_grafica_3d]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #8e44ad; color: white;
                    font-size: 13px; padding: 8px 16px; border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #9b59b6;
                }
            """)
            btn.setEnabled(False)
        self.btn_grafica_2d.clicked.connect(self.graficar_2d)
        self.btn_grafica_3d.clicked.connect(self.graficar_3d)
        graficas_layout.addWidget(self.btn_grafica_2d)
        graficas_layout.addWidget(self.btn_grafica_3d)
        layout.addLayout(graficas_layout)

        # Canvas
        self.canvas = FigureCanvas(plt.Figure(figsize=(4, 3)))
        layout.addWidget(self.canvas)

        # Botón volver
        btn_volver = QPushButton("Volver")
        btn_volver.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        btn_volver.clicked.connect(self.volver_callback)
        layout.addWidget(btn_volver, alignment=Qt.AlignCenter)

        self.entradas = []
        self.matriz_actual = None
        self.vectores_actuales = None

    def generar_entradas(self):
        for fila in self.entradas:
            for celda in fila:
                celda.deleteLater()
        self.entradas = []

        filas = self.spin_filas.value()
        columnas = self.spin_columnas.value()

        if filas != columnas:
            QMessageBox.warning(self, "Error", "La matriz debe ser cuadrada.")
            return

        for i in range(filas):
            fila_entradas = []
            for j in range(columnas):
                celda = QLineEdit("0")
                celda.setAlignment(Qt.AlignCenter)
                celda.setFixedWidth(50)
                celda.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 4px; background-color: white;")
                self.grid_entradas.addWidget(celda, i, j)
                fila_entradas.append(celda)
            self.entradas.append(fila_entradas)

    def calcular_vectores(self):
        try:
            matriz = []
            for fila in self.entradas:
                fila_valores = [float(celda.text()) for celda in fila]
                matriz.append(fila_valores)

            A = np.array(matriz)
            if A.shape[0] != A.shape[1]:
                raise ValueError("La matriz debe ser cuadrada")

            valores, vectores = np.linalg.eig(A)
            self.matriz_actual = A
            self.vectores_actuales = vectores

            self.btn_grafica_2d.setEnabled(A.shape == (2, 2))
            self.btn_grafica_3d.setEnabled(A.shape == (3, 3))

            resultado = "<b style='font-size:16px; color:#2c3e50;'>\U0001F537 Valores propios:</b><br>"
            resultado += ", ".join([f"<b>\u03bb{i+1}</b> = {val:.4f}" for i, val in enumerate(valores)]) + "<br><br>"
            resultado += "<b style='font-size:16px; color:#2c3e50;'>\U0001F537 Vectores propios asociados:</b><br>"
            for i, vec in enumerate(vectores.T):
                resultado += f"<b>v{i+1}</b> = [" + ", ".join([f"{v:.4f}" for v in vec]) + "]<br>"
            self.resultado_texto.setText(resultado)

        except Exception as e:
            if "index" in str(e).lower() or "tuple" in str(e).lower():
                QMessageBox.critical(self, "Error", "⚠️ Debes llenar todos los valores de la matriz.")
            else:
                QMessageBox.critical(self, "Error", f"Ocurrió un error inesperado: {e}")


    def graficar_2d(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        V = self.vectores_actuales
        ax.quiver(0, 0, V[0, 0], V[1, 0], angles='xy', scale_units='xy', scale=1, color='r')
        ax.quiver(0, 0, V[0, 1], V[1, 1], angles='xy', scale_units='xy', scale=1, color='g')
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True)
        ax.set_aspect('equal')
        self.canvas.draw()

    def graficar_3d(self):
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111, projection='3d')
        V = self.vectores_actuales
        colores = ['r', 'g', 'b']
        for i in range(min(3, V.shape[1])):
            ax.quiver(0, 0, 0, V[0, i], V[1, i], V[2, i], color=colores[i])
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-5, 5])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        self.canvas.draw()

# ------------------------- MÉTODO PARA VISTA PRINCIPAL -------------------------
class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Científica")  # Título de la ventana principal
        self.setGeometry(300, 50, 800, 600)  # Tamaño y posición de la ventana
        self.stack = QStackedWidget()  # Contenedor que permite cambiar entre vistas (pantallas)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.menu_widget = QWidget()  # Widget principal del menú
        self.stack.addWidget(self.menu_widget)  # Agrega el menú al stack

        # ========== VISTAS DE MATRICES ==========
        self.vista_suma_matrices = VistaSumaMatrices(self.volver_a_matrices)
        self.vista_resta_matrices = VistaRestaMatrices(self.volver_a_matrices)
        self.vista_multiplicacion = VistaMultiplicacionMatrices(self.volver_a_matrices)
        self.vista_determinante = VistaDeterminanteMatrices(self.volver_a_matrices)
        self.vista_inversa = VistaInversaMatrices(self.volver_a_matrices)
        self.vista_sistema = VistaSistemaEcuaciones(self.volver_a_matrices)

        # Añadir todas las vistas al stack
        self.stack.addWidget(self.vista_suma_matrices)
        self.stack.addWidget(self.vista_resta_matrices)
        self.stack.addWidget(self.vista_multiplicacion)
        self.stack.addWidget(self.vista_determinante)
        self.stack.addWidget(self.vista_inversa)
        self.stack.addWidget(self.vista_sistema)

        # ========== VISTAS DE POLINOMIOS ==========
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

        # ========== VISTAS DE VECTORES ==========
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

        # ========== VISTAS DE GRÁFICAS ==========
        self.vista_grafica_2d = VistaGrafica2D(self.volver_a_graficas)
        self.vista_grafica_3d = VistaGrafica3D(self.volver_a_graficas)

        self.stack.addWidget(self.vista_grafica_2d)
        self.stack.addWidget(self.vista_grafica_3d)

        # ========== VISTAS DE CÁLCULO ==========
        self.vista_derivada = VistaDerivacionPolinomios(self.volver_a_calculo)
        self.vista_integral_indefinida = VistaIntegralIndefinida(self.volver_a_calculo)
        self.vista_integral_definida = VistaIntegralDefinida(self.volver_a_calculo)

        self.stack.addWidget(self.vista_derivada)
        self.stack.addWidget(self.vista_integral_indefinida)
        self.stack.addWidget(self.vista_integral_definida)

        # ========== ACERCA DE ==========
        self.vista_acercade = AcercaDe(self.stack, self.menu_widget)
        self.stack.addWidget(self.vista_acercade)

        self.vista_vectores_propios = VistaVectoresPropios(self.volver_a_algebra)

        self.stack.addWidget(self.vista_vectores_propios)

        # Crear la vista
        self.vista_metodos = VistaMetodosNumericos(volver_callback=lambda: self.stack.setCurrentWidget(self.menu_widget))
        self.stack.setCurrentWidget(self.menu_widget)

        self.stack.addWidget(self.vista_metodos)

        # ========== SUBMENÚS ==========
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

        self.submenu_algebra = SubmenuAlgebra(
            self.stack,
            self.ir_a_vectores_propios,
            lambda: self.stack.setCurrentWidget(self.menu_widget)  # ✅ función válida
        )

        self.stack.addWidget(self.submenu_algebra)


        # Inicializa el menú principal
        self.init_menu()

    def init_menu(self):
        """Crea el diseño del menú principal con botones por módulo."""
        layout = QVBoxLayout(self.menu_widget)
        title = QLabel("Calculadora Científica")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        # Lista de módulos con sus iconos
        modules = [
            ("Matrices", obtener_ruta_recurso(os.path.join("imagenes", "matrices.png"))),
            ("Polinomios", obtener_ruta_recurso(os.path.join("imagenes", "polinomios.png"))),
            ("Vectores", obtener_ruta_recurso(os.path.join("imagenes", "vectores.png"))),
            ("Gráficas", obtener_ruta_recurso(os.path.join("imagenes", "graficas.png"))),
            ("Cálculo", obtener_ruta_recurso(os.path.join("imagenes", "calculo.png"))),
            ("AcercaDe", obtener_ruta_recurso(os.path.join("imagenes", "acercade.png"))),
            ("Métodos \nNuméricos", obtener_ruta_recurso(os.path.join("imagenes", "cruzado.png"))),
            ("Álgebra \nLineal", obtener_ruta_recurso(os.path.join("imagenes", "punto.png"))),

        ]

        # Crear los botones del menú
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
            # Conectar cada botón a su submenú correspondiente
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
            elif name == "Métodos \nNuméricos":
                btn.clicked.connect(lambda _, x=self.vista_metodos: self.stack.setCurrentWidget(x))
            elif name == "AcercaDe":
                btn.clicked.connect(lambda _, x=self.vista_acercade: self.stack.setCurrentWidget(x))
            elif name == "Álgebra \nLineal":
                btn.clicked.connect(lambda _, x=self.submenu_algebra: self.stack.setCurrentWidget(x))
            grid.addWidget(btn, i // 3, i % 3)

        layout.addLayout(grid)
        self.stack.setCurrentWidget(self.menu_widget)  # Mostrar el menú al iniciar

    # Métodos de navegación para cambiar entre vistas

    # MATRICES
    def ir_a_suma_matrices(self): self.stack.setCurrentWidget(self.vista_suma_matrices)
    def ir_a_resta_matrices(self): self.stack.setCurrentWidget(self.vista_resta_matrices)
    def ir_a_multiplicacion_matrices(self): self.stack.setCurrentWidget(self.vista_multiplicacion)
    def ir_a_determinante_matrices(self): self.stack.setCurrentWidget(self.vista_determinante)
    def ir_a_inversa_matrices(self): self.stack.setCurrentWidget(self.vista_inversa)
    def ir_a_sistema_matrices(self): self.stack.setCurrentWidget(self.vista_sistema)
    def volver_a_matrices(self): self.stack.setCurrentWidget(self.submenu_matrices)

    # POLINOMIOS
    def ir_a_suma_polinomios(self): self.stack.setCurrentWidget(self.vista_suma_polinomios)
    def ir_a_multiplicacion_polinomios(self): self.stack.setCurrentWidget(self.vista_multiplicacion_polinomios)
    def ir_a_derivacion_polinomios(self): self.stack.setCurrentWidget(self.vista_derivacion_polinomios)
    def ir_a_integracion_polinomios(self): self.stack.setCurrentWidget(self.vista_integracion_polinomios)
    def ir_a_evaluacion_polinomios(self): self.stack.setCurrentWidget(self.vista_evaluacion_polinomios)
    def volver_a_polinomios(self): self.stack.setCurrentWidget(self.submenu_polinomios)

    # VECTORES
    def ir_a_suma_vectores(self): self.stack.setCurrentWidget(self.vista_suma_vectores)
    def ir_a_resta_vectores(self): self.stack.setCurrentWidget(self.vista_resta_vectores)
    def ir_a_magnitud_vectores(self): self.stack.setCurrentWidget(self.vista_magnitud_vectores)
    def ir_a_producto_punto_vectores(self): self.stack.setCurrentWidget(self.VistaProductoPuntoVectores)
    def ir_a_producto_cruzado_vectores(self): self.stack.setCurrentWidget(self.vista_producto_cruz_vectores)
    def volver_a_vectores(self): self.stack.setCurrentWidget(self.submenu_vectores)

    # GRÁFICAS
    def ir_a_grafica_2d(self): self.stack.setCurrentWidget(self.vista_grafica_2d)
    def ir_a_grafica_3d(self): self.stack.setCurrentWidget(self.vista_grafica_3d)
    def volver_a_graficas(self): self.stack.setCurrentWidget(self.submenu_graficas)

    # CÁLCULO
    def ir_a_derivada(self): self.stack.setCurrentWidget(self.vista_derivada)
    def ir_a_integral_indefinida(self): self.stack.setCurrentWidget(self.vista_integral_indefinida)
    def ir_a_integral_definida(self): self.stack.setCurrentWidget(self.vista_integral_definida)
    def volver_a_calculo(self): self.stack.setCurrentWidget(self.submenu_calculo)

    def ir_a_vectores_propios(self): self.stack.setCurrentWidget(self.vista_vectores_propios)
    def volver_a_algebra(self): self.stack.setCurrentWidget(self.submenu_algebra)

# ------------------------- EJECUCIÓN -------------------------
if __name__ == "__main__":  # Verifica si el script es ejecutado directamente (no importado como módulo)
    app = QApplication(sys.argv)  # Crea una instancia de la aplicación Qt, pasando los argumentos de la línea de comandos
    window = MenuPrincipal()  # Crea una instancia de la clase principal de la ventana (el menú principal)
    window.show()  # Muestra la ventana en pantalla
    sys.exit(app.exec_())  # Ejecuta el bucle de eventos de la aplicación y asegura que al salir se termine correctamente
