from routing import *


class RouterConf:
    def __init__(self):
        self.id = ""
        self.interfaces = []
        self._interface_counter = 0
        self.routes = []

    def add_interface(self, ip, mask):
        self.interfaces.append(
            {"name": f"FastEthernet0/{self._interface_counter}", "ip": ip, "mask": mask}
        )
        self._interface_counter += 1

    def add_route(self, network, mask, gateway):
        self.routes.append({"network": network, "mask": mask, "gateway": gateway})

    def __str__(self):
        return f"Router {self.id}\n{self.interfaces}"

    def script(self) -> str:
        script = f"enable\nconfigure terminal\nhostname {self.id}\n"
        for interface in self.interfaces:
            script += f"interface {interface['name']}\nip address {interface['ip']} {interface['mask']}\nno shutdown\n"
        for route in self.routes:
            script += (
                f"ip route {route['network']} {route['mask']} {route['gateway']}\n"
            )
        script += "end\nwrite memory\n"
        return script


def generate_scripts(router: Router, connections: list):
    list = []
    generate_network_structure(router, list)
    fill_connections(connections, list)
    script = ""
    for router in list:
        script += router.script() + "\n"
    return script


def generate_network_structure(router: Router, list: list[RouterConf]):
    if router.children:
        for child in router.children:
            generate_network_structure(child, list)
    else:
        router_conf = RouterConf()
        name = router.name
        if name.endswith("-hosts"):
            name = name[:-6]
        router_conf.id = name
        ip = router.segment.network.network_address + 1
        mask = router.segment.network.netmask
        router_conf.add_interface(ip, mask)
        list.append(router_conf)


def fill_connections(connections: list, list: list[RouterConf]):
    for connection in connections:
        id = connection["id"]
        conns = connection["connections"]
        router = find_router(id, list)
        if not router:
            router = RouterConf()
            router.id = id
            list.append(router)
        for conn in conns:
            router2 = find_router(conn["id"], list)
            if not router2:
                router2 = RouterConf()
                router2.id = conn["id"]
                list.append(router2)
            ipr2 = conn["ip"]
            mask = conn["subnet"].netmask
            ipr1 = conn["gateway"]
            router.add_interface(ipr1, mask)
            router2.add_interface(ipr2, mask)
            router.add_route(str(conn["subnet"]), mask, ipr2)
            router2.add_route(str(conn["subnet"]), mask, ipr1)


def find_router(id, list):
    for router in list:
        if router.id == id:
            return router
    return None


red_central = {
    "id": "Central-1",
    "connections": [
        {
            "id": "Central-1-Edificio-1",
            "hosts": 100,
            "connections": [
                {
                    "id": "Central-1-Edificio-1-Piso-1",
                    "hosts": 20,
                    "connections": [
                        {"id": "Central-1-Edificio-1-Piso-1-Cuarto-1", "hosts": 70},
                        {"id": "Central-1-Edificio-1-Piso-1-Cuarto-2", "hosts": 30},
                        {"id": "Central-1-Edificio-1-Piso-1-Cuarto-3", "hosts": 30},
                    ],
                },
                {"id": "Central-1-Edificio-1-Piso-2", "hosts": 20},
                {"id": "Central-1-Edificio-1-Piso-3", "hosts": 20},
                {"id": "Central-1-Edificio-1-Piso-4", "hosts": 20},
                {"id": "Central-1-Edificio-1-Piso-5", "hosts": 20},
                {"id": "Central-1-Edificio-1-Piso-6", "hosts": 30},
            ],
        },
        {
            "id": "Central-1-Edificio-2",
            "connections": [
                {"id": "Central-1-Edificio-2-Piso-1", "hosts": 20},
                {"id": "Central-1-Edificio-2-Piso-2", "hosts": 20},
                {"id": "Central-1-Edificio-2-Piso-3", "hosts": 20},
                {"id": "Central-1-Edificio-2-Piso-4", "hosts": 20},
                {"id": "Central-1-Edificio-2-Piso-5", "hosts": 20},
                {"id": "Central-1-Edificio-2-Piso-6", "hosts": 30},
                {"id": "Central-1-Edificio-2-Piso-7", "hosts": 30},
            ],
        },
    ],
}

if __name__ == "__main__":
    connections_table = extract_connections(red_central)
    ip_base = "192.162.0.0"
    prefix = 15
    red = subneteo(red_central, ip_base, prefix, connections_table)
    router = red["central_router"]
    connections = red["ip_connections"]
    script = generate_scripts(router, connections)
    print(script)
