from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QPushButton, QTextEdit, QVBoxLayout, QWidget, QHBoxLayout
from types.loaders.clustersloader import ClustersLoader
from types.visualization.clustersview import ClustersView


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__cluster_loader = ClustersLoader(self)
        self.__cluster_view = ClustersView(self)
        self.__cluster_view.colors = ["red", "blue", "lime", "orange", "black",
                                      "yellow", "pink", "magenta", "brown", "gray",
                                      "cyan", "beige", "green", "steelblue", "#007ACC",
                                      "#b06f86", "#2ab07d", "#e823da", "#072340", "#9a7be2"]
        self.__cluster_view.setMinimumWidth(1000)
        self.__cluster_view.setMinimumHeight(1000)
        self.__text_edit = QTextEdit(self)
        self.__confirm_button = QPushButton("&Confirm")
        self.__confirm_button.setFixedHeight(40)

        # signals & slots
        self.__cluster_loader.clusters_loaded.connect(self.__cluster_view.set_clusters)
        self.__confirm_button.clicked.connect(self._set_clusters_from_text_area)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.__text_edit)
        input_layout.addWidget(self.__confirm_button)
        input_layout.setSpacing(0)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.__cluster_view)
        main_layout.addLayout(input_layout)
        main_layout.setStretch(0, 5)
        main_layout.setStretch(1, 1)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Cluster visualizer")

        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)

        # set defult example
        self.__text_edit.setText("""Clusters:
cluster 0: 40[86,663] 56[44,854] 62[85,874] 68[80,770] 75[28,603] 86[238,650]
cluster 1: 43[747,938]
cluster 2: 47[285,973]
cluster 3: 49[548,422]
""")

    @pyqtSlot()
    def _set_clusters_from_text_area(self):
        self.__cluster_loader.load_clusters(self.__text_edit.toPlainText())

    @pyqtSlot()
    def set_clusters(self, str_clusters):
        self.__text_edit.setText(str_clusters)
        self.__cluster_loader.load_clusters(str_clusters)