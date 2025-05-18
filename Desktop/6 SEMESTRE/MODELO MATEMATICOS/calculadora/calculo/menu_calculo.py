from importaciones import *
from utilidades import obtener_ruta_recurso, SubmenuBase

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