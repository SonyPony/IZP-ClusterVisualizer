from PyQt5.QtCore import QObject, QSizeF


class ClusterContainer(QObject):
    def __init__(self):
        super().__init__()

        self.__clusters = list()

    @property
    def clusters(self):
        return self.__clusters

    @clusters.setter
    def clusters(self, clusters):
        self.__clusters = clusters

    def max_size(self):
        size = QSizeF(0, 0)

        for cluster in self.__clusters:
            for obj in cluster.objects:
                if obj.x() > size.width():
                    size.setWidth(obj.x())

                if obj.y() > size.height():
                    size.setHeight(obj.y())
        return size

    def neighbor_id(self, obj):
        lowest_distance = None
        neighbor_id = -1

        for cluster in self.__clusters:
            _, new_distance = cluster.distance_from_point(obj)

            if lowest_distance is None or new_distance < lowest_distance:
                lowest_distance = new_distance
                neighbor_id = cluster.id
        return neighbor_id
