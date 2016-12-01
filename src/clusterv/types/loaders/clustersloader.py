from PyQt5.QtCore import QObject, pyqtSignal, QPointF
from types.clusters.clusterobject import ClusterObject
from types.clusters.cluster import Cluster
import re


class ClustersLoader(QObject):
    clusters_loaded = pyqtSignal([list])

    def load_clusters(self, str_cluster):
        re_cluster_id = re.compile(r'^cluster (?P<id>\d+)')
        re_object = re.compile(r'(?P<id>\d+)\[(?P<x>\d+),(?P<y>\d+)\]')

        lines = str_cluster.split("\n")[1::]
        lines = list(filter(None, lines))

        clusters = list()
        for single_line in lines:
            try:
                id = int(re_cluster_id.search(single_line).group("id"))
                clusters.append(Cluster(id))
            except (ValueError, IndexError):
                print("Cluster id not valid")

            for object_match in re_object.finditer(single_line):
                try:
                    pos = QPointF(float(object_match.group("x")), float(object_match.group("y")))
                    id = int(object_match.group("id"))

                except (ValueError, IndexError):
                    print("Object properties are not valid")

                clusters[-1].add_object(ClusterObject(id, pos))
        self.clusters_loaded.emit(clusters)