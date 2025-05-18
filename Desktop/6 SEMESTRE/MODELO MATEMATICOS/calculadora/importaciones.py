import sys,math,random,re,os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QStackedWidget,
    QToolButton, QGridLayout, QMessageBox, QSpacerItem, QSizePolicy,
    QHBoxLayout, QSpinBox, QPushButton, QLineEdit, QFrame,QFormLayout,QComboBox,QTableWidget,QTableWidgetItem,QScrollArea,QHeaderView,QGroupBox,QTextEdit,QDoubleSpinBox,QDialog,QTextBrowser
)
import tempfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon,QPixmap
import uuid

from PyQt5.QtCore import Qt, QSize
import numpy as np
import webbrowser
from matplotlib.figure import Figure
from sympy import Matrix,sympify,simplify,symbols,diff,integrate,lambdify
import sympy as sp

from utilidades import interpretar_valor, interpretar_valor_simbolico, limpiar_expresion
