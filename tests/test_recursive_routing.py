"""
Device {
  "child_names": string
  "hosts": num | null
  "neighbors": num | null
  "bits": num | null
  "connections"?: Device[]
}
"""
import ipaddress
import math

connections_table = [
    {
        "from": "Central-1",
        "to": "Central-1-Edificio-1",
    },
    {
        "from": "Central-1-Edificio-1",
        "to": "Central-1-Edificio-1-Piso-1",
    },
    {
        "from": "Piso 1",
        "to": "Cuarto 1",
    }
]


red_central = {
    "id": "Central-1",
    "connections": [
        {
            "id": "Central-1-Edificio-1",
            "connections": [
                {
                    "id": "Central-1-Edificio-1-Piso-1",
                    "hosts": 20,
                    "connections": [
                        {
                            "id": "Central-1-Edificio-1-Piso-1-Cuarto-1",
                            "hosts": 70
                        },
                        {
                            "id": "Central-1-Edificio-1-Piso-1-Cuarto-2",
                            "hosts": 30
                        },
                        {
                            "id": "Central-1-Edificio-1-Piso-1-Cuarto-3",
                            "hosts": 30
                        }
                    ]
                },
                {
                    "id": "Central-1-Edificio-1-Piso-2",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-1-Piso-3",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-1-Piso-4",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-1-Piso-5",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-1-Piso-6",
                    "hosts": 30
                },
            ]
        },
        {
            "id": "Central-1-Edificio-2",
            "connections": [
                {
                    "id": "Central-1-Edificio-2-Piso-1",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-2-Piso-2",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-2-Piso-3",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-2-Piso-4",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-2-Piso-5",
                    "hosts": 20
                },
                {
                    "id": "Central-1-Edificio-2-Piso-6",
                    "hosts": 30
                },
                {
                    "id": "Central-1-Edificio-2-Piso-7",
                    "hosts": 30
                },
            ]
        },
    ]
}

def extract_connections(node, parent=None):
    connections = []
    if parent:
        connections.append({"from": parent, "to": node["id"]})
    if "connections" in node:
        for child in node["connections"]:
            connections.extend(extract_connections(child, node["id"]))
    return connections


# Generate the connections array
connections_table = extract_connections(red_central)
print(connections_table)

def print_network_structure(node, level=0):
    indent = "  " * level
    print(f"{indent}- id: {node['id']}")
    if "hosts" in node:
        print(f"{indent}  hosts: {node['hosts']}")
    if "nei" in node:
        for connection in node["connections"]:
            print_network_structure(connection, level + 1)
    if "connections" in node:
        for connection in node["connections"]:
            print_network_structure(connection, level + 1)


def populate_neighbors(device):
    if("connections" in device):
        total_neighbors = 0
        for connection in connections_table:
            if(connection["from"] == device["id"]):
                total_neighbors += 1

        device["neighbors"] = total_neighbors
        device["hosts"] = total_neighbors
        for connection in device["connections"]:
            populate_neighbors(connection)


populate_neighbors(red_central)


def print_network_structure(node, level=0):
    indent = "  " * level
    print(f"{indent}- id: {node['id']}")
    if "hosts" in node:
        print(f"{indent}  hosts: {node['hosts']}")
    if "neighbors" in node:
        print(f"{indent}  neighbors: {node['neighbors']}")
    if "connections" in node:
        for connection in node["connections"]:
            print_network_structure(connection, level + 1)


print_network_structure(red_central)


def populate_hosts_device(device):
    if("hosts" in device and "connections" not in device):
        # Si el router central tiene las conexiones finales (pcs), el return de bits cambia a solo retornar math.ceil(math.log2(device["hosts"]))
        device["bits"] = math.ceil(math.log2(device["hosts"] + 2 + 1))
        return {"hosts": device["hosts"]}

    if("connections" in device):
        total_hosts = 0
        for connection in device["connections"]:
            total_hosts += populate_hosts_device(connection)["hosts"]

        if("hosts" in device):
            device["hosts"] += total_hosts
        else:
            device["hosts"] = total_hosts
        # Si el router central tiene las conexiones finales (pcs), el lamba cambia a retornar el length de connections
        device["bits"] = math.ceil(max(list(map(lambda x: x["bits"], device["connections"])))) + math.ceil(math.log2(device["neighbors"] + 2 ))
        return {"hosts": device["hosts"]}

populate_hosts_device(red_central)
print_network_structure(red_central)

class NetworkSegment:
    def __init__(self, ip_base, prefix):
        self.network = ipaddress.ip_network(f"{ip_base}/{prefix}", strict=False)
        self.subnets = []

    def subdivide(self, num_subnets):
        self.subnets = list(self.network.subnets(new_prefix=self.network.prefixlen + (num_subnets - 1).bit_length()))
        return self.subnets

class Router:
    def __init__(self, name, ip_base, prefix):
        self.name = name
        self.segment = NetworkSegment(ip_base, prefix)
        self.children = []

    def add_child_router(self, child_router):
        self.children.append(child_router)

    def subdivide_network(self, num_subnets):
        return self.segment.subdivide(num_subnets)

    def display_structure(self, level=0):
        indent = "  " * level
        print(f"{indent}- Router: {self.name}, Network: {self.segment.network}")
        """
        for i, subnet in enumerate(self.segment.subnets):
            print(f"{indent}  Subnet {i+1}: {subnet}")
        """
        for child in self.children:
            child.display_structure(level + 1)


ips_connections = []
"""
ip_connection {
   "id": string
    "connections": ip_connection[]
    "ip": string
    "subnet": string
    "gateway": string
}
"""


def divide_network(device, router: Router):

    ip_connection = {"id": device["id"], "connections": []}
    if "connections" in device:
        num_subnets = len(device["connections"]) + 1  # +1 for neighbors
        subnets = router.subdivide_network(num_subnets)

        subnet_connetions = list(subnets[-1].subnets(new_prefix=30))
        for connection in connections_table:
            if(connection["from"] == device["id"]):
                child_connection = {}
                child_connection["id"] = connection["to"]
                child_connection["subnet"] = subnet_connetions.pop(0)
                child_connection["gateway"] = child_connection["subnet"].network_address + 1
                child_connection["ip"] = child_connection["subnet"].network_address + 2
                ip_connection["connections"].append(child_connection)

        ips_connections.append(ip_connection)
        for i, subnet in enumerate(subnets):
            if i < len(device["connections"]):
                subnet_router = Router(f"{device['id']}", subnet.network_address, subnet.prefixlen)
                divide_network(device["connections"][i], subnet_router)
                router.add_child_router(subnet_router)




central_router = Router("Central", "192.162.0.0", 32 - red_central["bits"])
divide_network(red_central, central_router)
central_router.display_structure()

def print_ip_connections(node, level=0):
    """
    Recursively prints an ip_connection object with indentation.

    :param node: The current ip_connection object.
    :param level: The current indentation level.
    """
    for sing_node in node:
        indent = "  " * level
        print(f"{indent}- id: {sing_node["id"]}")
        if "ip" in sing_node:
            print(f"{indent}  ip: {sing_node["ip"]}")
        if "subnet" in sing_node:
            print(f"{indent}  subnet: {sing_node["subnet"]}")
        if "gateway" in sing_node:
            print(f"{indent}  gateway: {sing_node["gateway"]}")
        if "connections" in sing_node:
            print(f"{indent}  connections:")
        if "connections" in sing_node:
            print_ip_connections(sing_node["connections"], level + 1)

print_ip_connections(ips_connections)