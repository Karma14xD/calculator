from importaciones import *

# IMPORTANTE: importamos desde el módulo principal donde están definidos
from utilidades import obtener_ruta_recurso, SubmenuBase

class SubmenuMatrices(SubmenuBase):
    def __init__(self, stack, go_to_suma, go_to_resta, go_to_multiplicacion, go_to_determinante, go_to_inversa_matriz, go_to_sistema, menu_widget):
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
            ("Suma", obtener_ruta_recurso(os.path.join("imagenes", "suma.png"))),
            ("Resta", obtener_ruta_recurso(os.path.join("imagenes", "resta.png"))),
            ("Multiplicación", obtener_ruta_recurso(os.path.join("imagenes", "multiplicacion.png"))),
            ("Determinante", obtener_ruta_recurso(os.path.join("imagenes", "determinante.png"))),
            ("Inversa", obtener_ruta_recurso(os.path.join("imagenes", "inversa.png"))),
            ("Resolver Sistema", obtener_ruta_recurso(os.path.join("imagenes", "ecuaciones.png"))),
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
            btn.setFixedSize(140, 120)

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
