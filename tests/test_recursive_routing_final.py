import ipaddress
import json


def allocate_subnets(device, base_ip, prefix):
    """
    Asigna subredes recursivamente con conexiones directas entre routers de edificios y al router del área.
    """
    if "connections" in device:
        # Contar las conexiones (hijos directos del nodo actual)
        num_connections = len(device["connections"])
        network = ipaddress.ip_network(f"{base_ip}/{prefix}", strict=False)
        subnets = list(
            network.subnets(new_prefix=prefix + num_connections.bit_length() + 1)
        )  # Subred para cada conexión

        if len(subnets) < num_connections:
            raise ValueError(
                f"No hay suficientes subredes para {device['child_names']}. "
                f"Necesarias: {num_connections}, Generadas: {len(subnets)}"
            )

        # Asignar IP del router actual
        device["router_ip"] = str(subnets[0].network_address + 1)
        device["router_subnets"] = []  # Subredes para conexiones directas

        # Asignar conexiones entre routers
        for i, connection in enumerate(device["connections"]):
            connection_subnet = subnets[i]
            # Conexión router-actual -> router-hijo
            device["router_subnets"].append(
                {
                    "connection_to": connection["child_names"],
                    "subnet": str(connection_subnet),
                    "local_ip": str(connection_subnet.network_address + 1),
                    "remote_ip": str(connection_subnet.network_address + 2),
                }
            )

            # Asignar IP remota al nodo hijo
            connection["router_ip"] = str(connection_subnet.network_address + 2)

            # Recursivamente asignar subredes a los hijos
            allocate_subnets(
                connection,
                connection_subnet.network_address,
                connection_subnet.prefixlen,
            )

        # Conexiones entre routers en el mismo nivel (solo para routers de edificios)
        if device["child_names"].startswith("Area"):
            for i, conn1 in enumerate(device["connections"]):
                for j, conn2 in enumerate(device["connections"]):
                    if i < j:  # Evitar duplicar conexiones
                        interconnection_subnet = subnets.pop()
                        device["router_subnets"].append(
                            {
                                "connection_between": (
                                    conn1["child_names"],
                                    conn2["child_names"],
                                ),
                                "subnet": str(interconnection_subnet),
                                "ip_router_1": str(
                                    interconnection_subnet.network_address + 1
                                ),
                                "ip_router_2": str(
                                    interconnection_subnet.network_address + 2
                                ),
                            }
                        )

    else:
        # Nodo final: asignar subred a hosts directos
        network = ipaddress.ip_network(f"{base_ip}/{prefix}", strict=False)
        device["direct_hosts_subnet"] = str(network)
        device["direct_hosts"] = []
        device["gateway"] = str(network.network_address + 1)
        for i in range(device["hosts"]):
            device["direct_hosts"].append(
                {
                    "host_ip": str(network.network_address + i + 2),
                    "gateway": device["gateway"],
                }
            )


def create_output_dict(device):
    """
    Crea un diccionario con la estructura de salida para representar la red.
    """
    output = {"name": device["child_names"]}

    if "connections" in device:
        output["router_ip"] = device.get("router_ip")
        output["router_subnets"] = device.get("router_subnets", [])

        output["connections"] = [
            create_output_dict(conn) for conn in device["connections"]
        ]
    else:
        output["direct_hosts_subnet"] = device.get("direct_hosts_subnet")
        output["gateway"] = device.get("gateway")
        output["direct_hosts"] = [
            {"host_ip": host["host_ip"], "gateway": host["gateway"]}
            for host in device.get("direct_hosts", [])
        ]

    return output


# Estructura de red basada en la imagen
red_central = {
    "child_names": "Router Central",
    "connections": [
        {
            "child_names": "Area-1",
            "connections": [
                {
                    "child_names": "Edificio-1",
                    "connections": [
                        {"child_names": "Piso-1", "hosts": 7},
                        {"child_names": "Piso-2", "hosts": 5},
                        {"child_names": "Piso-3", "hosts": 4},
                    ],
                },
                {
                    "child_names": "Edificio-2",
                    "connections": [
                        {"child_names": "Piso-1", "hosts": 6},
                        {"child_names": "Piso-2", "hosts": 8},
                    ],
                },
                {
                    "child_names": "Edificio-3",
                    "connections": [
                        {"child_names": "Piso-1", "hosts": 4},
                        {"child_names": "Piso-2", "hosts": 4},
                    ],
                },
            ],
        },
        {
            "child_names": "Area-2",
            "connections": [
                {
                    "child_names": "Edificio-1",
                    "connections": [
                        {"child_names": "Piso-1", "hosts": 6},
                        {"child_names": "Piso-2", "hosts": 5},
                    ],
                }
            ],
        },
    ],
}


def generate_output(red_central):
    try:
        allocate_subnets(red_central, ipaddress.IPv4Address("192.168.0.0"), 16)
        output_dict = create_output_dict(red_central)
        return output_dict
    except Exception as e:
        return {"error": str(e)}


# Ejecutar asignación de subredes
try:
    output_dict = generate_output(red_central)
    formatted_output = json.dumps(output_dict, indent=2)
    print(formatted_output)
except Exception as e:
    print(f"Error: {e}")
