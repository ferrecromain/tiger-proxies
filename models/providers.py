import requests
import time
from bs4 import BeautifulSoup
from models.entities import Proxy


class ProxyList:
    """ Fournisseur proxylist.me """

    def __init__(self):
        self.base_url = "https://proxylist.me/"
        self.first_p = 1

    def get_proxies(self):
        """ Renvoi l'ensemble des proxies disponibles """

        p = self.first_p
        res = []
        while True:
            page = self._get_page(p)
            if self._is_proxy_page(page):
                proxies = self._extract_proxies(page)
                res += proxies
                time.sleep(5)
                p += 1
            else:
                return res

    def _get_page(self, p):
        """ Recupère et renvoi la page d'indice p """

        r = requests.get(self.base_url, params={"page": p})
        return BeautifulSoup(r.text, "html.parser")

    def _extract_proxies(self, content):
        """ Renvoi une liste de proxies disponibles dans la page """

        res = []
        rows = content.select("#datatable-row-highlight tbody tr")
        for row in rows:
            if self._is_proxy_line(row):
                proxy = Proxy(
                    address=self._row_extract_adress(row),
                    port=self._row_extract_port(row),
                    protocol=self._row_extract_protocol(row),
                    anonymity=self._row_extract_anonymity(row),
                )
                res.append(proxy)
        return res

    def _is_proxy_page(self, content):
        """ Determine si la page contient des proxies ou non """

        return content.find("h3", text="Proxy List") is not None

    def _is_proxy_line(self, content):
        """ Determine si la ligne de tableau contient des informations sur
        un proxy ou non
        """

        return content.find("td", {"class": "ip"}) is not None

    def _row_extract_adress(self, row):
        """ extrait l'adresse ip de la ligne du tableau """

        return row.find("td", {"class": "ip"}).a.get_text()

    def _row_extract_port(self, row):
        """ extrait le numero de port de la ligne du tableau """

        return int(row.find("td", {"class": "port"}).get_text())

    def _row_extract_protocol(self, row):
        """ extrait le protocole de la ligne du tableau
        si plusieurs sont disponibles alors choisis le premier
        """

        protocols = row.find("td", {"class": "protocol"}).get_text()
        return protocols.split(", ")[0]

    def _row_extract_anonymity(self, row):
        """ extrait le niveau d'anonymat de la ligne du tableau """

        return row.find("td", {"class": "type"}).get_text().lower()
