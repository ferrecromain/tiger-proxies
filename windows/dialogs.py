from PyQt5 import QtGui, QtCore, QtWidgets
from threading import get_ident


class ProxiesUpdater(QtWidgets.QDialog):
    """ Fenêtre de mise à jour des proxies """

    def __init__(self, parent):
        super(ProxiesUpdater, self).__init__(parent=parent)
        self._build_ui()

    def _build_ui(self):
        vbox1 = QtWidgets.QVBoxLayout()
        img_label = QtWidgets.QLabel()
        img = QtGui.QMovie("media/running_tiger.gif")
        img_label.setMovie(img)
        img_label.setAlignment(QtCore.Qt.AlignCenter)
        img.start()
        message = QtWidgets.QLabel(
            "Tiger Proxies is downloading proxies across different servers"
            ", it may take several minutes ..."
        )
        vbox1.addWidget(img_label)
        vbox1.addWidget(message)
        self.setLayout(vbox1)
        self.setWindowTitle("Updating the list of proxies")
        self.setWindowIcon(QtGui.QIcon("media/app.ico"))
