from importaciones import *
from matrices.vista_suma import VistaSumaMatrices

class VistaRestaMatrices(VistaSumaMatrices):
    def __init__(self, volver_callback):
        super().__init__(volver_callback)

        # Cambiar título
        self.findChild(QLabel).setText("➖ Resta de Matrices")

        # Cambiar texto y color del botón principal
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

        # Reasignar funcionalidad
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
