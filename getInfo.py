import requests
import json
import ConfigParser

def getMachines():
    config = ConfigParser.ConfigParser()
    config.read('/etc/daaas-vmm-admin-page/config.ini')
    session = requests.Session()
    try:
        response = session.get(config.get('VMMConfig','url')+ "machines", headers={'VMM-User':config.get('VMMConfig', 'user'), 'VMM-Password': config.get('VMMConfig','password')})
    except:
        return []
    machines = json.loads(response.text)
    return machines

def getMachineTypes():
    config = ConfigParser.ConfigParser()
    config.read('/etc/daaas-vmm-admin-page/config.ini')
    session = requests.Session()
    try:
        response = session.get(config.get('VMMConfig','url')+ "machinetypes", headers={'VMM-User':config.get('VMMConfig', 'user'), 'VMM-Password': config.get('VMMConfig','password')})
    except:
        return []
    machinetypes = json.loads(response.text)
    return machinetypes

if __name__ == '__main__':
    print(getMachineInfo())


