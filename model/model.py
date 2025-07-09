import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}
        self._bestPath = []
        self._maxScore = 0


    def getStores(self):
        return DAO.getStores()

    def buildGraph(self, storeId, nGiorniMax):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMap = {}

        nodes = DAO.getAllNodes(storeId)
        for node in nodes:
            self._nodes.append(node)
            self._idMap[node.order_id] = node
        self._graph.add_nodes_from(nodes)
        print("N nodi: ", self._graph.number_of_nodes())
        edges = DAO.getEdges(storeId, nGiorniMax)
        for edge in edges:
            self._graph.add_edge(self._idMap[edge["o1"]], self._idMap[edge["o2"]], weight=edge["weight"])
        print("N archi: ", self._graph.number_of_edges())


    def searchPath(self, source):
        return list(nx.bfs_tree(self._graph, self._idMap[source]))

    def number_of_nodes(self):
        return self._graph.number_of_nodes()

    def number_of_edges(self):
        return self._graph.number_of_edges()

    def nodes(self):
        return self._nodes


    def getRicorsione(self, source):
        nodoSource = self._idMap[source]
        parziale = [nodoSource]
        nodiRimanenti = copy.deepcopy(self._nodes)
        nodiRimanenti.remove(nodoSource)
        self._ricorsione(parziale, nodiRimanenti, nodoSource)
        return self._bestPath, self._maxScore


    def _ricorsione(self, parziale, nodiRimanenti, source):
        if (actualScore := self._calculateScore(parziale)) > self._maxScore:
            self._maxScore = int(actualScore)
            self._bestPath = copy.deepcopy(parziale)
        else:
            for n in nx.neighbors(self._graph, source):
                if n not in parziale:
                    if self._verificaNodo(n, parziale):
                        parziale.append(n)
                        self._ricorsione(parziale, nodiRimanenti, n)
                        parziale.pop()

    def _hasNeighborsAvaible(self, source, nodiRimanenti):
        for n in nx.neighbors(self._graph, source):
            if n in nodiRimanenti:
                return True
        return False


    def _calculateScore(self, cammino):
        totale = 0
        for i in range(1, len(cammino)):
            arco = self._graph.get_edge_data(cammino[i-1], cammino[i])
            totale += arco["weight"]
        return totale


    def _verificaNodo(self, n, parziale):
        if n in parziale:
            return False
        if len(parziale) < 2:
            return True
        pesoPrecedente = self._graph.get_edge_data(parziale[-2], parziale[-1])["weight"]
        pesoAttuale = self._graph.get_edge_data(parziale[-1], n)["weight"]
        if pesoAttuale < pesoPrecedente:
            return True
        return False