from models import providers
import inspect
from PyQt5 import QtCore


class ProxyFetcher(QtCore.QThread):
    """ Tâche recuperant les proxies disponibles sur l'ensemble des
    fournisseurs
    """

    new_proxies = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self._init_providers()

    def _init_providers(self):
        self._providers = []
        for name, cls in inspect.getmembers(providers):
            if inspect.isclass(cls) and cls.__module__ == "models.providers":
                self._providers.append(cls())

    def run(self):
        for provider in self._providers:
            self.new_proxies.emit(provider.get_proxies())
