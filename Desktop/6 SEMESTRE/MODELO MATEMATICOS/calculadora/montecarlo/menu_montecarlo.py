from importaciones import *
from utilidades import obtener_ruta_recurso,SubmenuBase

class SubmenuMontecarlo(SubmenuBase):
    def __init__(self, stack, menu_widget, callbacks):
        super().__init__(stack, menu_widget)
        self.callbacks = callbacks  # Diccionario de {nombre: función}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Simulación por Montecarlo")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(20)
        grid.setAlignment(Qt.AlignCenter)

        # Opciones disponibles
        operaciones = [
            ("Distribuciones", "distribucion.png"),
            ("Integración", "integral.png"),
        ]

        for idx, (nombre, icono_archivo) in enumerate(operaciones):
            btn = QToolButton()
            btn.setText(nombre)
            btn.setIcon(QIcon(obtener_ruta_recurso(os.path.join("imagenes", icono_archivo))))
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

            if nombre in self.callbacks:
                btn.clicked.connect(self.callbacks[nombre])
            else:
                btn.clicked.connect(lambda _, x=nombre: QMessageBox.information(self, "Montecarlo", f"'{x}' aún no está disponible"))

            grid.addWidget(btn, idx // 3, idx % 3)

        layout.addLayout(grid)
        layout.addSpacing(1)
        self.add_back_button(layout)
