import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def fillDDStore(self):
        stores = self._model.getStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(store))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        store = self._view._ddStore.value
        if not store:
            self._view.txt_result.controls.append(ft.Text("Inserire lo store", color="red"))
            self._view.update_page()
            return
        k = self._view._txtIntK.value
        if not k:
            self._view.txt_result.controls.append(ft.Text("Inserire il numero massimo di giorni", color="red"))
            self._view.update_page()
            return
        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Il numero massimo di giorni deve essere un intero", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(store, kInt)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {self._model.number_of_nodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.number_of_edges()}"))
        self._fillDDNode()
        self._view.update_page()


    def _fillDDNode(self):
        self._view._ddNode.options.clear()
        nodes = self._model.nodes()
        for node in nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(node))

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        source = self._view._ddNode.value
        if not source:
            self._view.txt_result.controls.append(ft.Text("Inserire il nodo di partenza", color="red"))
            self._view.update_page()
            return
        path = self._model.searchPath(int(source))
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {path[0]}"))
        for p in path[1:]:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()


    def handleRicorsione(self, e):
        self._view.txt_result.controls.clear()
        source = self._view._ddNode.value
        if not source:
            self._view.txt_result.controls.append(ft.Text("Inserire il nodo di partenza", color="red"))
            self._view.update_page()
            return
        path, score = self._model.getRicorsione(int(source))
        self._view.txt_result.controls.append(ft.Text(f"Percorso di peso massimo trovato. Peso percorso: {score}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.update_page()
