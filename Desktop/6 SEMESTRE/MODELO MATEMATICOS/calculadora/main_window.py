from importaciones import *
from utilidades import obtener_ruta_recurso

#-------------------------------------------------------------------------
# Importar las vistas de matrices
from matrices.menu_matrices import SubmenuMatrices
from matrices.vista_suma import VistaSumaMatrices
from matrices.vista_resta import VistaRestaMatrices
from matrices.vista_multiplicacion import VistaMultiplicacionMatrices
from matrices.vista_determinante import VistaDeterminanteMatrices
from matrices.vista_inversa import VistaInversaMatrices
from matrices.vista_sistema import VistaSistemaEcuaciones
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE POLINOMIOS ==========
from polinomios.menu_polinomios import SubmenuPolinomios
from polinomios.vista_suma import VistaSumaPolinomios
from polinomios.vista_multiplicacion import VistaMultiplicacionPolinomios
from polinomios.vista_derivacion import VistaDerivacionPolinomios
from polinomios.vista_integracion import VistaIntegracionPolinomios
from polinomios.vista_evaluacion import VistaEvaluacionPolinomios
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE VECTORES ==========
from vectores.menu_vectores import SubmenuVectores
from vectores.vista_suma import VistaSumaVectores
from vectores.vista_resta import VistaRestaVectores
from vectores.vista_magnitud import VistaMagnitudVectores
from vectores.vista_producto_punto import VistaProductoPuntoVectores
from vectores.vista_producto_cruzado import VistaProductoCruzadoVectores
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE GRAFICAS ==========
from graficas.menu_graficas import SubmenuGraficas
from graficas.vista_2d import VistaGrafica2D
from graficas.vista_3d import VistaGrafica3D
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE CALCULOS ==========
from calculo.menu_calculo import SubmenuCalculo
from calculo.vista_derivada import VistaDerivacionPolinomios
from calculo.vista_integral_indefinida import VistaIntegralIndefinida
from calculo.vista_integral_definida import VistaIntegralDefinida
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE METODOS NUMERICOS ==========
from metodos_numericos.vista_metodos import VistaMetodosNumericos
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE ACERCA DE ==========
from acerca.acerca_de import AcercaDe
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE VALORES Y VECTORES ==========
from algebra_lineal.vista_valores_vectores import VistaValoresVectores
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE GENERACION ALEATORIA ==========
from aleatorios.vista_generacion import VistaGeneracionAleatoria
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE MONTECARLO ==========
from montecarlo.menu_montecarlo import SubmenuMontecarlo
from montecarlo.vista_distribucion import VistaDistribucionesMontecarlo
from montecarlo.vista_integracion import VistaIntegracionMontecarlo
#-------------------------------------------------------------------------

#-------------------------------------------------------------------------
# ========== VISTAS DE MONTECARLO ==========
from prediccion.vista_prediccion_torricelli import VistaTorricelli
#-------------------------------------------------------------------------

#--------------------------------------------------------------------------
# ========== VISTA PRINCIPAL ==========
class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SIMULADOR X")
        self.setGeometry(300, 50, 800, 600)

        # Layout principal: horizontal con menú lateral
        layout_principal = QHBoxLayout(self)

        # Menú lateral (izquierdo)
        self.menu_lateral = QVBoxLayout()
        self.menu_lateral.setAlignment(Qt.AlignTop)

        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.menu_lateral)

        # Contenido derecho: stack de vistas
        self.stack = QStackedWidget()

        # Agregar al layout principal
        layout_principal.addWidget(self.menu_widget, 4)  # menú lateral más estrecho
        layout_principal.addWidget(self.stack, 6)        # contenido más ancho y centrado
            # Vista principal ocupa más
        self.menu_widget.setMaximumWidth(220)



    
#---------------------------------------------------------------------------
        # ========== SOLO VISTA DE MATRICES ==========
        self.vista_suma_matrices = VistaSumaMatrices(self.volver_a_matrices)
        self.stack.addWidget(self.vista_suma_matrices)
        self.vista_resta_matrices = VistaRestaMatrices(self.volver_a_matrices)
        self.stack.addWidget(self.vista_resta_matrices)
        self.vista_multiplicacion = VistaMultiplicacionMatrices(self.volver_a_matrices)
        self.stack.addWidget(self.vista_multiplicacion)
        self.vista_determinante = VistaDeterminanteMatrices(self.volver_a_matrices)
        self.stack.addWidget(self.vista_determinante)
        self.vista_inversa = VistaInversaMatrices(self.volver_a_matrices)
        self.stack.addWidget(self.vista_inversa)
        self.vista_sistema = VistaSistemaEcuaciones(self.volver_a_matrices)
        self.stack.addWidget(self.vista_sistema)

        # Submenú de matrices (solo este funciona por ahora)
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
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== SOLO VISTA DE POLINOMIOS ==========
        self.vista_suma_polinomios = VistaSumaPolinomios(self.volver_a_polinomios)
        self.stack.addWidget(self.vista_suma_polinomios)
        self.vista_multiplicacion_polinomios = VistaMultiplicacionPolinomios(self.volver_a_polinomios)
        self.stack.addWidget(self.vista_multiplicacion_polinomios)
        self.vista_derivacion_polinomios = VistaDerivacionPolinomios(self.volver_a_polinomios)
        self.stack.addWidget(self.vista_derivacion_polinomios)
        self.vista_integracion_polinomios = VistaIntegracionPolinomios(self.volver_a_polinomios)
        self.stack.addWidget(self.vista_integracion_polinomios)
        self.vista_evaluacion_polinomios = VistaEvaluacionPolinomios(self.volver_a_polinomios)
        self.stack.addWidget(self.vista_evaluacion_polinomios)

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
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTAS DE VECTORES ==========
        self.vista_suma_vectores = VistaSumaVectores(self.volver_a_vectores)
        self.stack.addWidget(self.vista_suma_vectores)
        self.vista_resta_vectores = VistaRestaVectores(self.volver_a_vectores)
        self.stack.addWidget(self.vista_resta_vectores)
        self.vista_magnitud_vectores = VistaMagnitudVectores(self.volver_a_vectores)
        self.stack.addWidget(self.vista_magnitud_vectores)
        self.vista_producto_punto_vectores = VistaProductoPuntoVectores(self.volver_a_vectores)
        self.stack.addWidget(self.vista_producto_punto_vectores)
        self.vista_producto_cruz_vectores = VistaProductoCruzadoVectores(self.volver_a_vectores)
        self.stack.addWidget(self.vista_producto_cruz_vectores)

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
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTAS DE GRAFICAS ==========
        self.vista_2d = VistaGrafica2D(self.volver_a_graficas)
        self.stack.addWidget(self.vista_2d)

        self.vista_3d = VistaGrafica3D(self.volver_a_graficas)
        self.stack.addWidget(self.vista_3d)

        self.submenu_graficas = SubmenuGraficas(
            self.stack,
            self.ir_a_grafica_2d,
            self.ir_a_grafica_3d,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_graficas)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTAS DE CALCULO ==========
        self.vista_derivada = VistaDerivacionPolinomios(self.volver_a_calculo)
        self.stack.addWidget(self.vista_derivada)

        self.vista_integral_indefinida = VistaIntegralIndefinida(self.volver_a_calculo)
        self.stack.addWidget(self.vista_integral_indefinida)

        self.vista_integral_definida = VistaIntegralDefinida(self.volver_a_calculo)
        self.stack.addWidget(self.vista_integral_definida)

        self.submenu_calculo = SubmenuCalculo(
            self.stack,
            self.ir_a_derivada,
            self.ir_a_integral_indefinida,
            self.ir_a_integral_definida,
            self.menu_widget
        )
        self.stack.addWidget(self.submenu_calculo)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTA ACERCA DE ==========
        self.vista_acerca = AcercaDe(self.stack, self.menu_widget)
        self.stack.addWidget(self.vista_acerca)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTA MÉTODOS NUMÉRICOS ==========
        self.vista_metodos_numericos = VistaMetodosNumericos(self.volver_a_menu)
        self.stack.addWidget(self.vista_metodos_numericos)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
        # ========== VISTA VALORES Y VECTORES ==========
        self.vista_valores_vectores = VistaValoresVectores(self.volver_a_menu)
        self.stack.addWidget(self.vista_valores_vectores)

#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# ========== VISTA GENERACION ALEATORIA ==========
        self.vista_generacion_aleatoria = VistaGeneracionAleatoria(self.volver_a_menu)
        self.stack.addWidget(self.vista_generacion_aleatoria)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# ========== VISTA MONTECARLO ==========
        self.vista_montecarlo_distribucion = VistaDistribucionesMontecarlo(self.volver_a_montecarlo)
        self.stack.addWidget(self.vista_montecarlo_distribucion)

        self.vista_montecarlo_integracion = VistaIntegracionMontecarlo(self.volver_a_montecarlo)
        self.stack.addWidget(self.vista_montecarlo_integracion)

 
        self.submenu_montecarlo = SubmenuMontecarlo(
            self.stack,
            self.menu_widget,
            {
                "Distribuciones": self.ir_a_montecarlo_distribuciones,
                "Integración": self.ir_a_montecarlo_integracion
            }
        )
        self.stack.addWidget(self.submenu_montecarlo)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# ========== VISTA TORRICELLI ==========
        self.vista_torricelli = VistaTorricelli(self.volver_a_menu)
        self.stack.addWidget(self.vista_torricelli)
#--------------------------------------------------------------------------

        # ========== Menú principal ==========
        self.init_menu()
        self.stack.setCurrentWidget(self.vista_acerca)

    def init_menu(self):
        title = QLabel("SIMULADOR X")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.menu_lateral.addWidget(title)

        botones = [
            ("Acerca de", "acercade.png", self.vista_acerca),
            ("Matrices", "matrices.png", self.submenu_matrices),
            ("Polinomios", "polinomios.png", self.submenu_polinomios),
            ("Vectores", "vectores.png", self.submenu_vectores),
            ("Gráficas", "graficas.png", self.submenu_graficas),
            ("Cálculo", "calculo.png", self.submenu_calculo),
            ("Métodos Numéricos", "cruzado.png", self.vista_metodos_numericos),
            ("Generación Aleatoria", "ecuaciones.png", self.vista_generacion_aleatoria),
            ("Vectores y Valores", "matrices.png", self.vista_valores_vectores),
            ("Montecarlo", "vectores.png", self.submenu_montecarlo),
            ("Torricelli", "integral.png", self.vista_torricelli),

        ]

        for texto, icono, destino in botones:
            btn = QToolButton()
            btn.setText(texto)
            btn.setIcon(QIcon(obtener_ruta_recurso(f"imagenes/{icono}")))
            btn.setIconSize(QSize(32, 32))
            btn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            btn.setStyleSheet("""
                QToolButton {
                    background-color: #2c3e50;
                    color: white;
                    font-weight: bold;
                    font-size: 13px;
                    border-radius: 8px;
                    padding: 10px;
                    text-align: left;
                }
                QToolButton:hover {
                    background-color: #34495e;
                }
            """)
            btn.setFixedSize(200, 50)  # MISMO TAMAÑO PARA TODOS
            btn.clicked.connect(lambda _, d=destino: self.stack.setCurrentWidget(d))
            self.menu_lateral.addWidget(btn)


#--------------------------------------------------------------------------
    # ================= FUNCIONES SOLO PARA MATRICES =================
    def ir_a_suma_matrices(self): self.stack.setCurrentWidget(self.vista_suma_matrices)
    def volver_a_matrices(self): self.stack.setCurrentWidget(self.submenu_matrices)
    def ir_a_resta_matrices(self): self.stack.setCurrentWidget(self.vista_resta_matrices)
    def ir_a_multiplicacion_matrices(self): self.stack.setCurrentWidget(self.vista_multiplicacion)
    def ir_a_determinante_matrices(self): self.stack.setCurrentWidget(self.vista_determinante)
    def ir_a_inversa_matrices(self): self.stack.setCurrentWidget(self.vista_inversa)
    def ir_a_sistema_matrices(self): self.stack.setCurrentWidget(self.vista_sistema)
    # ==============================================================
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
    # POLINOMIOS
    def ir_a_suma_polinomios(self): self.stack.setCurrentWidget(self.vista_suma_polinomios)
    def volver_a_polinomios(self): self.stack.setCurrentWidget(self.submenu_polinomios)
    def ir_a_multiplicacion_polinomios(self): self.stack.setCurrentWidget(self.vista_multiplicacion_polinomios)
    def ir_a_derivacion_polinomios(self): self.stack.setCurrentWidget(self.vista_derivacion_polinomios)
    def ir_a_integracion_polinomios(self): self.stack.setCurrentWidget(self.vista_integracion_polinomios)
    def ir_a_evaluacion_polinomios(self): self.stack.setCurrentWidget(self.vista_evaluacion_polinomios)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
    # ================= FUNCIONES SOLO PARA VECTORES =================
    def ir_a_suma_vectores(self): self.stack.setCurrentWidget(self.vista_suma_vectores)
    def ir_a_resta_vectores(self): self.stack.setCurrentWidget(self.vista_resta_vectores)
    def ir_a_magnitud_vectores(self): self.stack.setCurrentWidget(self.vista_magnitud_vectores)
    def ir_a_producto_punto_vectores(self): self.stack.setCurrentWidget(self.vista_producto_punto_vectores)
    def ir_a_producto_cruzado_vectores(self): self.stack.setCurrentWidget(self.vista_producto_cruz_vectores)
    def volver_a_vectores(self): self.stack.setCurrentWidget(self.submenu_vectores)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
    # ================= FUNCIONES SOLO PARA GRAFICAS =================
    def ir_a_grafica_2d(self): self.stack.setCurrentWidget(self.vista_2d)
    def ir_a_grafica_3d(self): self.stack.setCurrentWidget(self.vista_3d)
    def volver_a_graficas(self): self.stack.setCurrentWidget(self.submenu_graficas)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
    # ================= FUNCIONES SOLO PARA CÁLCULO =================
    def ir_a_derivada(self): self.stack.setCurrentWidget(self.vista_derivada)
    def ir_a_integral_indefinida(self): self.stack.setCurrentWidget(self.vista_integral_indefinida)
    def ir_a_integral_definida(self): self.stack.setCurrentWidget(self.vista_integral_definida)
    def volver_a_calculo(self): self.stack.setCurrentWidget(self.submenu_calculo)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
    # ================= FUNCIONES PARA METODOS NUMERICOS =================
    def volver_a_menu(self): self.stack.setCurrentWidget(self.menu_widget)
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
# ================= FUNCIONES PARA MONTECARLO =================
    def ir_a_montecarlo_distribuciones(self):
        self.stack.setCurrentWidget(self.vista_montecarlo_distribucion)
    def ir_a_montecarlo_integracion(self):
        self.stack.setCurrentWidget(self.vista_montecarlo_integracion)
    def volver_a_montecarlo(self):
        self.stack.setCurrentWidget(self.submenu_montecarlo)
#--------------------------------------------------------------------------
