from importaciones import *
from utilidades import obtener_ruta_recurso,SubmenuBase

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
