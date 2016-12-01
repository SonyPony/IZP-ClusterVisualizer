from PyQt5.QtCore import QObject


class ClusterObject(QObject):
    def __init__(self, id: int, pos):
        super().__init__()

        self.__id = id
        self.__pos = pos

    @property
    def id(self):
        return self.__id

    @property
    def pos(self):
        return self.__pos

    def x(self):
        return self.__pos.x()

    def y(self):
        return self.__pos.y()

    def __eq__(self, other):
        if self.x() == other.x() and self.y() == other.y():
            return True
        return False
