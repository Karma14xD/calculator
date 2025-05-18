from importaciones import *
from utilidades import obtener_ruta_recurso,SubmenuBase

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
            btn.setFixedSize(140, 120)  # Mismo tamaño fijo para todos los botones del submenú

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