import requests
import ConfigParser

class VMMEditor:
    def __init__(self):
        self.session = requests.Session()
        self.config = ConfigParser.ConfigParser()
        self.config.read('/etc/daaas-vmm-admin-page/config.ini')
        return

    def add_new_pool(self, poolDetails):
        response = self.session.post(self.config.get('VMMConfig','url')+ "machinetypes", headers={"VMM-User": self.config.get('VMMConfig', 'user') , "VMM-Password": self.config.get('VMMConfig','password'), "Content-Type": "application/json"}, data=poolDetails)
        return response.status_code, response.text
