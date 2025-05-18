from importaciones import *
from utilidades import obtener_ruta_recurso

class VistaTorricelli(QWidget):
    def __init__(self, volver_callback):
        super().__init__()
        self.volver_callback = volver_callback
        self.setStyleSheet("background-color: #f0f3f4; font-family: Arial;")
        self.init_ui()

    def init_ui(self):
        self.estilo_input = """
            QLineEdit {
                background-color: white; padding: 6px;
                font-size: 14px; border: 1px solid #ccc; border-radius: 5px;
            }
        """

        main_layout = QVBoxLayout(self)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # Título
        titulo = QLabel("⛲ Modelo de Drenaje de Tanques - Torricelli")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;")
        container_layout.addWidget(titulo)

        # Formulario de parámetros
        self.form_layout = QFormLayout()

        self.input_H = QLineEdit()
        self.input_H.setPlaceholderText("Ej: 16")
        self.input_a = QLineEdit()
        self.input_a.setPlaceholderText("Ej: 0.1963")
        self.input_A = QLineEdit()
        self.input_A.setPlaceholderText("Ej: 201")
        self.input_g = QLineEdit()
        self.input_g.setPlaceholderText("Ej: 981")

        for campo in [self.input_H, self.input_a, self.input_A, self.input_g]:
            campo.setStyleSheet(self.estilo_input)

        self.modelo_combo = QComboBox()
        self.modelo_combo.addItems(["Ideal (Torricelli)", "Corregido (con fricción)"])
        self.modelo_combo.setStyleSheet("padding: 6px; font-size: 14px;")

        self.form_layout.addRow("Altura del tanque H (cm):", self.input_H)
        self.form_layout.addRow("Área del orificio a (cm²):", self.input_a)
        self.form_layout.addRow("Área de la base A (cm²):", self.input_A)
        self.form_layout.addRow("Gravedad g (cm/s²):", self.input_g)
        self.form_layout.addRow("Modelo de simulación:", self.modelo_combo)

        container_layout.addLayout(self.form_layout)

        # Botón Calcular
        self.btn_calcular = QPushButton("Calcular")
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #27ae60; color: white;
                font-size: 14px; padding: 10px 20px; border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.btn_calcular.clicked.connect(self.calcular)
        container_layout.addWidget(self.btn_calcular, alignment=Qt.AlignCenter)

        # Resultado
        self.resultado_label = QLabel("")
        self.resultado_label.setAlignment(Qt.AlignCenter)
        self.resultado_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        container_layout.addWidget(self.resultado_label)

        # Gráfica
        self.figura = Figure(figsize=(5, 3))
        self.canvas = FigureCanvas(self.figura)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.canvas.setMinimumHeight(350)
        container_layout.addWidget(self.canvas)

        # Tabla
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(2)
        self.tabla.setHorizontalHeaderLabels(["Tiempo (s)", "Altura (cm)"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabla.setMinimumHeight(250)
        self.tabla.setStyleSheet("""
            QTableWidget {
                background-color: white;
                font-size: 14px;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
                font-weight: bold;
            }
        """)
        container_layout.addWidget(self.tabla)

        # Botón info
        self.btn_info = QPushButton("Ver explicación del modelo")
        self.btn_info.setStyleSheet("""
            QPushButton {
                background-color: #8e44ad; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
        """)
        self.btn_info.clicked.connect(self.mostrar_info_modelo)
        container_layout.addWidget(self.btn_info, alignment=Qt.AlignCenter)

        # Botón abrir PDF
        self.btn_abrir_pdf = QPushButton("Ver artículo completo (PDF)")
        self.btn_abrir_pdf.setStyleSheet("""
            QPushButton {
                background-color: #2980b9; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        self.btn_abrir_pdf.clicked.connect(self.abrir_pdf)
        container_layout.addWidget(self.btn_abrir_pdf, alignment=Qt.AlignCenter)

        # Botón volver
        btn_volver = QPushButton("Volver al Menú")
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
        container_layout.addWidget(btn_volver, alignment=Qt.AlignCenter)

    def mostrar_info_modelo(self):
        dialogo = DialogoInfoModelo(self)
        dialogo.exec_()


    def obtener_ruta_recurso(ruta_relativa):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, ruta_relativa)
        return os.path.join(os.path.abspath("."), ruta_relativa)

    def abrir_pdf(self):
        ruta = obtener_ruta_recurso("DOCUMENTOS/EJP-2021Torricelli.pdf")
        if os.path.exists(ruta):
            webbrowser.open_new(ruta)
        else:
            QMessageBox.warning(self, "Archivo no encontrado", "No se encontró el archivo del artículo PDF.")


    def calcular(self):
        try:
            H = float(self.input_H.text())
            a = float(self.input_a.text())
            A = float(self.input_A.text())
            g = float(self.input_g.text())
            modelo = self.modelo_combo.currentText()

            if modelo.startswith("Ideal"):
                T = (A / a) * math.sqrt(2 * H / g)
                CD = 1
            else:
                k = 8
                CD = k / (k + 2)
                T = (A / a) * math.sqrt(2 * H / g) / CD

            self.resultado_label.setText(f"Tiempo estimado para vaciar el tanque: {T:.2f} segundos")

            t_vals = np.linspace(0, T, 300)
            if CD == 1:
                h_vals = (np.sqrt(H) - (a * np.sqrt(2 * g) / (2 * A)) * t_vals) ** 2
            else:
                h_vals = (np.sqrt(H) - (a * np.sqrt(2 * g) * CD / (2 * A)) * t_vals) ** 2
            h_vals = np.clip(h_vals, 0, H)

            # Gráfica
            self.figura.clear()
            ax = self.figura.add_subplot(111)
            ax.plot(t_vals, h_vals, label="Altura del agua h(t)", color="#2980b9")
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Altura (cm)")
            ax.set_title("Simulación del vaciado del tanque")
            ax.grid(True)
            ax.legend()
            self.canvas.draw()

            # Tabla
            self.tabla.setRowCount(0)
            for i in range(0, len(t_vals), 20):
                row = self.tabla.rowCount()
                self.tabla.insertRow(row)
                self.tabla.setItem(row, 0, QTableWidgetItem(f"{t_vals[i]:.2f}"))
                self.tabla.setItem(row, 1, QTableWidgetItem(f"{h_vals[i]:.2f}"))

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error: {str(e)}")

# ------------------------- DIALOGO DE INFORMACION DEL MODELO -------------------------
class DialogoInfoModelo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Explicación del Modelo de Torricelli")
        self.setStyleSheet("background-color: #fdfefe; font-family: Arial; font-size: 14px;")
        self.resize(600, 600)
        self._imagenes_temp = []  # para eliminar luego

        layout = QVBoxLayout(self)

        # Introducción
        intro = QLabel(
            '📘 <b>Modelo basado en el artículo:</b><br>'
            '“Torricelli’s law revisited” – European Journal of Physics (2021)<br><br>'
            '🔬 Este modelo usa la ley de Torricelli para describir cómo se vacía un tanque por un orificio en la base.'
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        # Subtítulo
        subtitulo = QLabel("<h3 style='color:#2c3e50;'>📐 Fórmulas utilizadas</h3>")
        layout.addWidget(subtitulo)

        # Fórmulas LaTeX
        formulas = [
            r"T = \frac{A}{a} \sqrt{\frac{2H}{g}}",
            r"h(t) = \left(\sqrt{H} - \frac{a\sqrt{2g}}{2A}t\right)^2",
            r"CD = \frac{k}{k + 2} \quad \text{con } k = 8"
        ]
        for formula in formulas:
            label_img = self.render_formula(formula)
            layout.addWidget(label_img)

        # Datos finales
        datos = QLabel(
            "<br><b>🧪 Datos del artículo:</b><br>"
            "⏱️ Tiempo experimental: <b>29.2 s</b><br>"
            "📉 Tiempo teórico ideal: <b>23.1 s</b><br>"
            "⚙️ CD observado ajustado: <b>0.8</b>"
        )
        datos.setWordWrap(True)
        layout.addWidget(datos)

        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d; color: white;
                font-size: 13px; padding: 8px 20px; border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar, alignment=Qt.AlignCenter)

    def render_formula(self, latex_str):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        path = temp_file.name
        temp_file.close()

        plt.figure(figsize=(4, 0.8))
        plt.text(0.5, 0.5, f"${latex_str}$", fontsize=14, ha='center', va='center')
        plt.axis("off")
        plt.savefig(path, bbox_inches="tight", pad_inches=0.02, dpi=150)
        plt.close()

        self._imagenes_temp.append(path)

        label = QLabel()
        label.setPixmap(QPixmap(path))
        label.setAlignment(Qt.AlignCenter)
        return label

    def closeEvent(self, event):
        # Eliminar imágenes temporales
        for f in self._imagenes_temp:
            if os.path.exists(f):
                os.remove(f)
        event.accept()
