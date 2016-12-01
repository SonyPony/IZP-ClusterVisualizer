from PyQt5.QtCore import QSizeF, pyqtSlot, pyqtSignal, pyqtProperty, QPointF
from PyQt5.QtGui import QColor, QFontMetricsF, QPainter
from PyQt5.QtWidgets import QWidget

from types.clusters.clustercontainer import ClusterContainer


class ClustersView(QWidget):
    PARTICLE_SIZE = QSizeF(10, 10)

    colors_changed = pyqtSignal(list)
    clusters_changed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__colors = list()
        self.__cluster_container = ClusterContainer()
        self.__active_point = QPointF()

        self.setMouseTracking(True)

        self.clusters_changed.connect(self.update)

    def mouseMoveEvent(self, e):
        self.__active_point = e.pos()
        self.update()

    def paintEvent(self, e):
        if not len(self.__cluster_container.clusters) or self.width() == 0 or self.height() == 0:
            return

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QColor("transparent"))
        painter.setBrush(QColor("red"))

        fm = QFontMetricsF(painter.font())
        neighbor_id = self.__cluster_container.neighbor_id(self.__active_point)

        # draw objects
        for cluster in self.__cluster_container.clusters:
            try:
                painter.setBrush(QColor(self.__colors[self.__cluster_container.clusters.index(cluster)]))
            except IndexError:
                print("Run out of colors")
                exit(1)

            for obj in cluster.objects:
                painter.setPen(QColor("transparent"))
                painter.drawEllipse(
                    obj.x(),
                    obj.y(),
                    ClustersView.PARTICLE_SIZE.width(),
                    ClustersView.PARTICLE_SIZE.height())
                painter.setPen(QColor("gray"))
                painter.drawText(obj.pos - QPointF(0, 2), str(obj.id))


            used_cluster_obj, distance = cluster.distance_from_point(self.__active_point)
            center_of_obj = QPointF(
                used_cluster_obj.x() + ClustersView.PARTICLE_SIZE.width() / 2,
                used_cluster_obj.y() + ClustersView.PARTICLE_SIZE.height() / 2
            )

            # draw circle
            painter.setPen(QColor("gray"))
            painter.setBrush(QColor("transparent"))
            painter.setOpacity(0.5)
            painter.drawEllipse(center_of_obj, ClustersView.PARTICLE_SIZE.width() * 2, ClustersView.PARTICLE_SIZE.height() * 2)
            painter.setOpacity(1)

            #draw line
            painter.setPen(QColor("#007ACC" if neighbor_id == cluster.id else "lightGray"))
            painter.drawLine(self.__active_point, center_of_obj)

            #draw text
            formatted_distance = "{:.1f}".format(distance)
            painter.setPen(QColor("gray"))
            painter.drawText(center_of_obj - QPointF(fm.width(str(formatted_distance)) / 2, 25), str(formatted_distance))

        # draw text at active point
        coords = "[{:.1f} {:.1f}]".format(self.__active_point.x(), self.__active_point.y())
        painter.drawText(self.__active_point - QPointF(fm.width(coords) / 2, 15), coords)


    @pyqtProperty("QStringList")
    def colors(self):
        return self.__colors

    @colors.setter
    def colors(self, cols):
        if self.__colors == cols:
            return

        self.__colors = cols
        self.colors_changed.emit(cols)

    @pyqtSlot(list)
    def set_clusters(self, clusters):
        if self.__cluster_container.clusters == clusters:
            return

        self.__cluster_container.clusters = clusters
        self.clusters_changed.emit(clusters)

