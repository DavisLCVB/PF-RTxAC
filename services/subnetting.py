import ipaddress

def generate_subnets(data):
    
    # Calcula subredes para cada edificio y piso, asigna IPs para dispositivos
    # y gateways en los routers. (o sea todo)
    
    base_ip = data.base_ip
    num_edificios = data.num_edificios
    pisos = data.pisos_por_edificio

    subnets = []
    for edificio in range(num_edificios):
        for piso in range(pisos[edificio]):
            subnet = calculate_subnet(base_ip, edificio, piso)
            subnets.append(subnet)
    
    return {"subnets": subnets}

def calculate_subnet(base_ip, building, floor):

    red_base = ipaddress.ip_network(base_ip, strict=False) 
    print (red_base)
    
    # Aquí va la lógica para calcular la subred...
    
    return {"espero":"que funcione"}

