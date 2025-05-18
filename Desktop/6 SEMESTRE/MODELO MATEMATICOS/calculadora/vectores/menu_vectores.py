from importaciones import *
from utilidades import obtener_ruta_recurso, SubmenuBase

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
            btn.setFixedSize(140, 120)  # Mismo tamaño fijo para todos los botones del submenú

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
