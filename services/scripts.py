def generate_scripts(red: dict):
    script = ""
    with open("output.txt", "w") as f:
        f.write(generate_scripts_recursive(red, script))


def generate_scripts_recursive(red: dict, script: str):
    if "direct_hosts" in red:
        for i, host in enumerate(red["direct_hosts"]):
            script += generar_conf_host(host, i, red["name"])
    elif "router_ip" in red:
        script += generar_conf_router(red)
    if "connections" in red:
        for conn in red["connections"]:
            script = generate_scripts_recursive(conn, script)
    return script + "\n"


def generar_conf_router(info: dict):
    cfg = []
    cfg.append("-- ROUTER --")
    cfg.append("enable")
    cfg.append("configure terminal")
    if "name" in info:
        cfg.append(f"hostname {info['name'].replace(' ', '_')}")
    if "router_subnets" in info:
        for i, rs in enumerate(info["router_subnets"]):
            subnet = rs["subnet"]
            _, prefix = subnet.split("/")
            mask = prefix_to_mask(prefix)
            interface = f"FastEthernet0/{i}"
            if "local_ip" in rs:
                local_ip = rs["local_ip"]
            else:
                local_ip = rs["ip_router_1"]
            cfg.append(f"interface {interface}")
            cfg.append(f"ip address {local_ip} {mask}")
            cfg.append("no shutdown")
        for rs in info["router_subnets"]:
            red, prefix = rs["subnet"].split("/")
            mask = prefix_to_mask(prefix)
            ip2: str
            if "remote_ip" in rs:
                ip2 = rs["remote_ip"]
            else:
                ip2 = rs["ip_router_2"]
            cfg.append(f"ip route {red} {mask} {ip2}")
    cfg.append("end")
    cfg.append("write memory")
    return "\n".join(cfg) + "\n"


def generar_conf_host(info: dict, i: int, area: str):
    cfg = []
    cfg.append(f"-- HOST {i} {area} --")
    cfg.append(f"ip: {info['host_ip']}")
    cfg.append(f"gateway: {info['gateway']}")
    return "\n".join(cfg) + "\n"


def prefix_to_mask(prefix):
    bits = int(prefix)
    mask = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF
    return f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"


def main():
    red = {
        "name": "Router Central",
        "router_ip": "192.168.0.1",
        "router_subnets": [
            {
                "connection_to": "Area-1",
                "subnet": "192.168.0.0/19",
                "local_ip": "192.168.0.1",
                "remote_ip": "192.168.0.2",
            },
            {
                "connection_to": "Area-2",
                "subnet": "192.168.32.0/19",
                "local_ip": "192.168.32.1",
                "remote_ip": "192.168.32.2",
            },
        ],
        "connections": [
            {
                "name": "Area-1",
                "router_ip": "192.168.0.1",
                "router_subnets": [
                    {
                        "connection_to": "Edificio-1",
                        "subnet": "192.168.0.0/22",
                        "local_ip": "192.168.0.1",
                        "remote_ip": "192.168.0.2",
                    },
                    {
                        "connection_to": "Edificio-2",
                        "subnet": "192.168.4.0/22",
                        "local_ip": "192.168.4.1",
                        "remote_ip": "192.168.4.2",
                    },
                    {
                        "connection_to": "Edificio-3",
                        "subnet": "192.168.8.0/22",
                        "local_ip": "192.168.8.1",
                        "remote_ip": "192.168.8.2",
                    },
                    {
                        "connection_between": ["Edificio-1", "Edificio-2"],
                        "subnet": "192.168.28.0/22",
                        "ip_router_1": "192.168.28.1",
                        "ip_router_2": "192.168.28.2",
                    },
                    {
                        "connection_between": ["Edificio-1", "Edificio-3"],
                        "subnet": "192.168.24.0/22",
                        "ip_router_1": "192.168.24.1",
                        "ip_router_2": "192.168.24.2",
                    },
                    {
                        "connection_between": ["Edificio-2", "Edificio-3"],
                        "subnet": "192.168.20.0/22",
                        "ip_router_1": "192.168.20.1",
                        "ip_router_2": "192.168.20.2",
                    },
                ],
                "connections": [
                    {
                        "name": "Edificio-1",
                        "router_ip": "192.168.0.1",
                        "router_subnets": [
                            {
                                "connection_to": "Piso-1",
                                "subnet": "192.168.0.0/25",
                                "local_ip": "192.168.0.1",
                                "remote_ip": "192.168.0.2",
                            },
                            {
                                "connection_to": "Piso-2",
                                "subnet": "192.168.0.128/25",
                                "local_ip": "192.168.0.129",
                                "remote_ip": "192.168.0.130",
                            },
                            {
                                "connection_to": "Piso-3",
                                "subnet": "192.168.1.0/25",
                                "local_ip": "192.168.1.1",
                                "remote_ip": "192.168.1.2",
                            },
                        ],
                        "connections": [
                            {
                                "name": "Piso-1",
                                "direct_hosts_subnet": "192.168.0.0/25",
                                "gateway": "192.168.0.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.0.2",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.3",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.4",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.5",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.6",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.7",
                                        "gateway": "192.168.0.1",
                                    },
                                    {
                                        "host_ip": "192.168.0.8",
                                        "gateway": "192.168.0.1",
                                    },
                                ],
                            },
                            {
                                "name": "Piso-2",
                                "direct_hosts_subnet": "192.168.0.128/25",
                                "gateway": "192.168.0.129",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.0.130",
                                        "gateway": "192.168.0.129",
                                    },
                                    {
                                        "host_ip": "192.168.0.131",
                                        "gateway": "192.168.0.129",
                                    },
                                    {
                                        "host_ip": "192.168.0.132",
                                        "gateway": "192.168.0.129",
                                    },
                                    {
                                        "host_ip": "192.168.0.133",
                                        "gateway": "192.168.0.129",
                                    },
                                    {
                                        "host_ip": "192.168.0.134",
                                        "gateway": "192.168.0.129",
                                    },
                                ],
                            },
                            {
                                "name": "Piso-3",
                                "direct_hosts_subnet": "192.168.1.0/25",
                                "gateway": "192.168.1.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.1.2",
                                        "gateway": "192.168.1.1",
                                    },
                                    {
                                        "host_ip": "192.168.1.3",
                                        "gateway": "192.168.1.1",
                                    },
                                    {
                                        "host_ip": "192.168.1.4",
                                        "gateway": "192.168.1.1",
                                    },
                                    {
                                        "host_ip": "192.168.1.5",
                                        "gateway": "192.168.1.1",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "Edificio-2",
                        "router_ip": "192.168.4.1",
                        "router_subnets": [
                            {
                                "connection_to": "Piso-1",
                                "subnet": "192.168.4.0/25",
                                "local_ip": "192.168.4.1",
                                "remote_ip": "192.168.4.2",
                            },
                            {
                                "connection_to": "Piso-2",
                                "subnet": "192.168.4.128/25",
                                "local_ip": "192.168.4.129",
                                "remote_ip": "192.168.4.130",
                            },
                        ],
                        "connections": [
                            {
                                "name": "Piso-1",
                                "direct_hosts_subnet": "192.168.4.0/25",
                                "gateway": "192.168.4.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.4.2",
                                        "gateway": "192.168.4.1",
                                    },
                                    {
                                        "host_ip": "192.168.4.3",
                                        "gateway": "192.168.4.1",
                                    },
                                    {
                                        "host_ip": "192.168.4.4",
                                        "gateway": "192.168.4.1",
                                    },
                                    {
                                        "host_ip": "192.168.4.5",
                                        "gateway": "192.168.4.1",
                                    },
                                    {
                                        "host_ip": "192.168.4.6",
                                        "gateway": "192.168.4.1",
                                    },
                                    {
                                        "host_ip": "192.168.4.7",
                                        "gateway": "192.168.4.1",
                                    },
                                ],
                            },
                            {
                                "name": "Piso-2",
                                "direct_hosts_subnet": "192.168.4.128/25",
                                "gateway": "192.168.4.129",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.4.130",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.131",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.132",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.133",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.134",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.135",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.136",
                                        "gateway": "192.168.4.129",
                                    },
                                    {
                                        "host_ip": "192.168.4.137",
                                        "gateway": "192.168.4.129",
                                    },
                                ],
                            },
                        ],
                    },
                    {
                        "name": "Edificio-3",
                        "router_ip": "192.168.8.1",
                        "router_subnets": [
                            {
                                "connection_to": "Piso-1",
                                "subnet": "192.168.8.0/25",
                                "local_ip": "192.168.8.1",
                                "remote_ip": "192.168.8.2",
                            },
                            {
                                "connection_to": "Piso-2",
                                "subnet": "192.168.8.128/25",
                                "local_ip": "192.168.8.129",
                                "remote_ip": "192.168.8.130",
                            },
                        ],
                        "connections": [
                            {
                                "name": "Piso-1",
                                "direct_hosts_subnet": "192.168.8.0/25",
                                "gateway": "192.168.8.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.8.2",
                                        "gateway": "192.168.8.1",
                                    },
                                    {
                                        "host_ip": "192.168.8.3",
                                        "gateway": "192.168.8.1",
                                    },
                                    {
                                        "host_ip": "192.168.8.4",
                                        "gateway": "192.168.8.1",
                                    },
                                    {
                                        "host_ip": "192.168.8.5",
                                        "gateway": "192.168.8.1",
                                    },
                                ],
                            },
                            {
                                "name": "Piso-2",
                                "direct_hosts_subnet": "192.168.8.128/25",
                                "gateway": "192.168.8.129",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.8.130",
                                        "gateway": "192.168.8.129",
                                    },
                                    {
                                        "host_ip": "192.168.8.131",
                                        "gateway": "192.168.8.129",
                                    },
                                    {
                                        "host_ip": "192.168.8.132",
                                        "gateway": "192.168.8.129",
                                    },
                                    {
                                        "host_ip": "192.168.8.133",
                                        "gateway": "192.168.8.129",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Area-2",
                "router_ip": "192.168.32.1",
                "router_subnets": [
                    {
                        "connection_to": "Edificio-1",
                        "subnet": "192.168.32.0/21",
                        "local_ip": "192.168.32.1",
                        "remote_ip": "192.168.32.2",
                    }
                ],
                "connections": [
                    {
                        "name": "Edificio-1",
                        "router_ip": "192.168.32.1",
                        "router_subnets": [
                            {
                                "connection_to": "Piso-1",
                                "subnet": "192.168.32.0/24",
                                "local_ip": "192.168.32.1",
                                "remote_ip": "192.168.32.2",
                            },
                            {
                                "connection_to": "Piso-2",
                                "subnet": "192.168.33.0/24",
                                "local_ip": "192.168.33.1",
                                "remote_ip": "192.168.33.2",
                            },
                        ],
                        "connections": [
                            {
                                "name": "Piso-1",
                                "direct_hosts_subnet": "192.168.32.0/24",
                                "gateway": "192.168.32.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.32.2",
                                        "gateway": "192.168.32.1",
                                    },
                                    {
                                        "host_ip": "192.168.32.3",
                                        "gateway": "192.168.32.1",
                                    },
                                    {
                                        "host_ip": "192.168.32.4",
                                        "gateway": "192.168.32.1",
                                    },
                                    {
                                        "host_ip": "192.168.32.5",
                                        "gateway": "192.168.32.1",
                                    },
                                    {
                                        "host_ip": "192.168.32.6",
                                        "gateway": "192.168.32.1",
                                    },
                                    {
                                        "host_ip": "192.168.32.7",
                                        "gateway": "192.168.32.1",
                                    },
                                ],
                            },
                            {
                                "name": "Piso-2",
                                "direct_hosts_subnet": "192.168.33.0/24",
                                "gateway": "192.168.33.1",
                                "direct_hosts": [
                                    {
                                        "host_ip": "192.168.33.2",
                                        "gateway": "192.168.33.1",
                                    },
                                    {
                                        "host_ip": "192.168.33.3",
                                        "gateway": "192.168.33.1",
                                    },
                                    {
                                        "host_ip": "192.168.33.4",
                                        "gateway": "192.168.33.1",
                                    },
                                    {
                                        "host_ip": "192.168.33.5",
                                        "gateway": "192.168.33.1",
                                    },
                                    {
                                        "host_ip": "192.168.33.6",
                                        "gateway": "192.168.33.1",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
        ],
    }
    generate_scripts(red)


if __name__ == "__main__":
    main()
