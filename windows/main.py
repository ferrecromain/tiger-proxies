from PyQt5 import QtGui, QtCore, QtWidgets
import csv
import webbrowser
from models.entities import Proxy
from threads import ProxyFetcher
from windows import dialogs


class Window(QtWidgets.QMainWindow):
    """ Fenêtre principale """

    def __init__(self):
        super(Window, self).__init__()
        self._central_widget = CentralWidget()
        self.setCentralWidget(self._central_widget)
        self.setWindowTitle("Tiger Proxies v1.0")
        self.setWindowIcon(QtGui.QIcon("media/app.ico"))
        self.setGeometry(100, 100, 700, 400)


class CentralWidget(QtWidgets.QWidget):
    """ Composants centraux de la fenêtre """

    def __init__(self):
        super(CentralWidget, self).__init__()
        hbox1 = QtWidgets.QHBoxLayout()
        vbox1 = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        self.setLayout(hbox1)

        # Actions sur le tableau de proxies
        self.download_button = QtWidgets.QPushButton("Download proxies")
        self.download_button.clicked.connect(self._update_ctrl)
        copy_button = QtWidgets.QPushButton("Copy to clipboard")
        copy_button.clicked.connect(self._copy_to_clipboard_ctrl)
        save_button = QtWidgets.QPushButton("Save to file")
        save_button.clicked.connect(self._save_to_file_ctrl)
        vbox1.addWidget(self.download_button)
        vbox1.addWidget(copy_button)
        vbox1.addWidget(save_button)

        # A propos
        about_img = QtGui.QPixmap()
        about_img.load("media/tiger_face.png")
        about_img = about_img.scaledToWidth(80)
        about_label1 = QtWidgets.QLabel()
        about_label1.setAlignment(QtCore.Qt.AlignCenter)
        about_label1.setPixmap(about_img)
        about_label2 = QtWidgets.QLabel("Developped by mazert - 2017")
        about_button = QtWidgets.QPushButton("Donate")
        about_button.clicked.connect(self._donate_ctrl)
        vbox1.addStretch()
        vbox1.addWidget(about_label1)
        vbox1.addWidget(about_label2)
        vbox1.addWidget(about_button)

        # Tableau des proxies
        self.proxies_table = QtWidgets.QTableWidget()
        self.proxies_table.setColumnCount(4)
        self.proxies_table.setHorizontalHeaderLabels(
            ["Address", "Port", "Protocol", "Anonymity"]
        )
        self.proxies_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.proxies_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.proxies_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.proxies_table.verticalHeader().setVisible(False)
        self.proxies_table.horizontalHeader().setStretchLastSection(True)
        vbox2.addWidget(self.proxies_table)

    def _update_ctrl(self):
        """ Contrôleur de mise de à jour de la liste des proxies dans le
        tableau
        """

        pu = dialogs.ProxiesUpdater(self)
        self.proxyfetcher_thread = ProxyFetcher()
        self.proxyfetcher_thread.started.connect(pu.show)
        self.proxyfetcher_thread.started.connect(self._set_download_button_disabled)
        self.proxyfetcher_thread.finished.connect(pu.hide)
        self.proxyfetcher_thread.finished.connect(self._set_download_button_enabled)
        self.proxyfetcher_thread.new_proxies.connect(self._set_table)
        self.proxyfetcher_thread.start()

    def _copy_to_clipboard_ctrl(self):
        """ Copie le contenu actuel du tableau dans le presse papier au
        format ip:port
        """
        res = ""
        clipboard = QtWidgets.QApplication.clipboard()
        proxies = self._get_table()
        for proxy in proxies:
            res += str(proxy) + "\n"
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(res, mode=clipboard.Clipboard)

    def _save_to_file_ctrl(self):
        """ Sauvegarde le contenu actuel du tableau dans un fichier au
        format CSV
        """
        fname, _ = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            caption="Save proxies to file",
            filter="csv file (*.csv)"
        )
        if fname:
            with open(fname, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["Address", "Port", "Protocol", "Anonymity"])
                for proxy in self._get_table():
                    writer.writerow([
                        proxy.address,
                        proxy.port,
                        proxy.protocol,
                        proxy.anonymity
                    ])

    def _donate_ctrl(self):
        """ Ouvre le navigateur par défaut vers la page paypal de donation """

        webbrowser.open("https://www.paypal.me/mazert")

    def _get_table(self):
        """ Renvoi une liste d'objets Proxy tel qu'affichés dans le tableau """

        res = []
        for row in range(self.proxies_table.rowCount()):
            res.append(
                Proxy(
                    address=self.proxies_table.item(row, 0).text(),
                    port=int(self.proxies_table.item(row, 1).text()),
                    protocol=self.proxies_table.item(row, 2).text(),
                    anonymity=self.proxies_table.item(row, 3).text()
                )
            )
        return res

    def _set_table(self, proxies):
        """ Remplace le tableau par les proxies spécifiés dans la liste """

        self.proxies_table.clearContents()
        self.proxies_table.setRowCount(len(proxies))
        for row, proxy in enumerate(proxies):
            self.proxies_table.setItem(row, 0, QtWidgets.QTableWidgetItem(proxy.address))
            self.proxies_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(proxy.port)))
            self.proxies_table.setItem(row, 2, QtWidgets.QTableWidgetItem(proxy.protocol))
            self.proxies_table.setItem(row, 3, QtWidgets.QTableWidgetItem(proxy.anonymity))

    def _set_download_button_disabled(self):
        self.download_button.setEnabled(False)

    def _set_download_button_enabled(self):
        self.download_button.setEnabled(True)
