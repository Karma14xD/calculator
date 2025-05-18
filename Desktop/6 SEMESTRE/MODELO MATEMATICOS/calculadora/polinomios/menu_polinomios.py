from importaciones import *
from utilidades import obtener_ruta_recurso, SubmenuBase

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
            btn.setFixedSize(140, 120)  # Mismo tamaño fijo para todos los botones del submenú

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
