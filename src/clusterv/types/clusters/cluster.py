from PyQt5.QtCore import QObject, QPointF
from math import sqrt


class Cluster(QObject):
    def __init__(self, id):
        super().__init__()

        self.__objects = list()
        self.__id = id

    @property
    def objects(self):
        return self.__objects

    @property
    def id(self) -> int:
        return self.__id

    def distance_from_point(self, point):
        max_distance = 0
        used_point = None

        for obj in self.__objects:
            new_distance = sqrt((obj.x() - point.x()) ** 2 + (obj.y() - point.y()) ** 2);
            if new_distance > max_distance:
                max_distance = new_distance
                used_point = QPointF(obj.pos)

        return (used_point, max_distance)

    def add_object(self, obj):
        self.__objects.append(obj)