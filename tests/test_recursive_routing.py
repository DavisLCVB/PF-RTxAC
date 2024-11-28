"""
Device {
  "child_names": string
  "hosts": num | null
  "bits": num | null
  "connections"?: Device[]
}
"""
import ipaddress
import math


def populate_hosts_device(device):
    if("hosts" in device):
        # Si el router central tiene las conexiones finales (pcs), el return de bits cambia a solo retornar math.ceil(math.log2(device["hosts"]))
        device["bits"] = math.ceil(math.log2(device["hosts"] + 2 + 1))
        return {"hosts": device["hosts"]}

    if("connections" in device):
        total_hosts = 0
        for connection in device["connections"]:
            total_hosts += populate_hosts_device(connection)["hosts"]

        device["hosts"] = total_hosts
        # Si el router central tiene las conexiones finales (pcs), el lamba cambia a retornar el length de connections
        device["bits"] = math.ceil(max(list(map(lambda x: x["bits"], device["connections"])))) + math.ceil(math.log2(len(device["connections"])))
        return {"hosts": device["hosts"]}

red_central = {
    "child_names": "Edificios",
    "connections": [
        {
            "child_names": "Pisos",
            "connections": [
                {
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
                {
                    "hosts": 30
                },
                ]
        },
{
            "child_names": "Pisos",
            "connections": [
                {
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
                {
                    "hosts": 30
                },
{
                    "hosts": 30
                },
                ]
        },
{
            "child_names": "Pisos",
            "connections": [
                {
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
                {
                    "hosts": 30
                },
{
                    "hosts": 30
                },
                ]
        },
{
            "child_names": "Pisos",
            "connections": [
                {
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
{
                    "hosts": 20
                },
                {
                    "hosts": 30
                },
{
                    "hosts": 30
                },

{
                    "hosts": 30
                },
                ]
        },
    ]
}

populate_hosts_device(red_central)
print(red_central)

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


def divide_network(device, router: Router):
    if "connections" in device:
        num_subnets = len(device["connections"])
        subnets = router.subdivide_network(num_subnets)
        for i, subnet in enumerate(subnets):
            if i < len(device["connections"]):
                subnet_router = Router(f"{device['child_names']}-{i+1}", subnet.network_address, subnet.prefixlen)
                divide_network(device["connections"][i], subnet_router)
                router.add_child_router(subnet_router)


central_router = Router("Central", "192.162.0.0", 32 - red_central["bits"])
divide_network(red_central, central_router)
central_router.display_structure()
