class Proxy:
    """ Represente un proxy """

    def __init__(self, address, port, protocol, anonymity):
        self.address = address
        self.port = port
        self.protocol = protocol
        self.country = ""
        self.anonymity = anonymity

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        protocols = ["http", "https", "socks"]
        if protocol in protocols:
            self._protocol = protocol
        else:
            raise ValueError("Protocole non valide : {}".format(protocol))

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if 0 <= port <= 65535:
            self._port = port
        else:
            raise ValueError("Port non valide : {}".format(port))

    @property
    def anonymity(self):
        return self._anonymity

    @anonymity.setter
    def anonymity(self, anonymity):
        anonymities = ["transparent", "anonymous", "high anonymous"]
        if anonymity in anonymities:
            self._anonymity = anonymity
        else:
            raise ValueError(
                "Niveau d'anonymat '{}' non valide".format(anonymity)
            )

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        """ Essaye de trouver une entrée du pays dans la base de données
        pycountry, et définit l'attribu par cette valeur.
        """

        pass

    @property
    def checked(self):
        return self._checked.strftime("%Y-%m-%d %H:%M:%S")

    @checked.setter
    def checked(self, checked):
        pass

    def __repr__(self):
        return "{address}:{port}".format(
            address=self._address,
            port=self._port
        )
