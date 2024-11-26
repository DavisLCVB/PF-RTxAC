# para testear la red de edificio y piso. (tablas de ruteo)

import ipaddress
import math

def calculate_network_base(edificios, pisos_maximo, pcs_por_piso, ip_base_str, ip_base_edificios):
    try:
        ip_base = ipaddress.IPv4Address(ip_base_str)
        ip_base_edificios = ipaddress.IPv4Address(ip_base_edificios)
    except ipaddress.AddressValueError:
        raise ValueError(f"La IP base '{ip_base_str}' no es válida.")
    
    bits_pcs = math.ceil(math.log2(pcs_por_piso + 2 + 1))  # +2 por dirección de red misma y broadcast, y +1 por el router de la subred
    bits_pisos = math.ceil(math.log2(pisos_maximo))
    bits_edificios = math.ceil(math.log2(edificios))
    
    total_bits = bits_edificios + bits_pisos + bits_pcs
    mask = 32 - total_bits 
    
    # Validar 
    try:
        network = ipaddress.IPv4Network(f"{ip_base}/{mask}", strict=False)

    except ipaddress.NetmaskValueError:
        raise ValueError(f"La IP base '{ip_base}' no es compatible con la máscara /{mask}.")
    
   
    total_addresses = 2 ** total_bits
    
    return {
        "ip_base": network,
        "mascara": mask,
        "direcciones_totales": total_addresses,
        "bits_edificios": bits_edificios,
        "bits_pisos": bits_pisos,
        "bits_computadoras": bits_pcs,
    }

def create_subnets_for_routers(ip_base, bits_edificios, bits_pisos, pisos_por_edificio):
    subred_edificios = list(ip_base.subnets(prefixlen_diff=bits_edificios))
    
    subredes_pisos = []
    for i, subred_edificio in enumerate(subred_edificios):
        subred_pisos = list(subred_edificio.subnets(prefixlen_diff=bits_pisos))[:pisos_por_edificio[i]]
        subredes_pisos.append(subred_pisos)
    
    conexiones_router = []
    for i in range(len(subred_edificios) - 1):
        subred_conexion = list(subred_edificios[i].subnets(prefixlen_diff=2))  
        conexiones_router.append(subred_conexion)
    
    return subred_edificios, subredes_pisos, conexiones_router

def assign_routers_and_pisos(subred_edificios, conexiones_router):
    router_ips = {}
    
    for i, subred_edificio in enumerate(subred_edificios):
        router_ips[f"Router {i+1}"] = list(subred_edificio.hosts())[0]  
    
    conexion_ips = {}
    for i, conexion in enumerate(conexiones_router):
        conexion_ips[f"Conexión {i+1}"] = [conexion[0].network_address + 1, conexion[0].network_address + 2]  # /30 tiene 2 direcciones utilizables
    
    return router_ips, conexion_ips


try:
    pisos_por_edificio = [8, 3, 4, 6]
    
    result = calculate_network_base(edificios=len(pisos_por_edificio), pisos_maximo=max(pisos_por_edificio), pcs_por_piso=30, ip_base_str="192.162.0.0", ip_base_edificios="172.16.10.0")
    
    #Outputs, se modifica para la response

    print("IP Base:", result["ip_base"])
    print("Máscara:", result["mascara"])
    print("Direcciones totales:", result["direcciones_totales"])
    print("Bits usados para edificios:", result["bits_edificios"])
    print("Bits usados para pisos:", result["bits_pisos"])
    print("Bits usados para computadoras:", result["bits_computadoras"])
    
    
    subred_edificios, subredes_pisos, conexiones_router = create_subnets_for_routers(result["ip_base"], result["bits_edificios"], result["bits_pisos"], pisos_por_edificio)
    
    print("\nSubredes para los edificios:")
    for subred in subred_edificios:
        print(subred)
    
    print("\nSubredes para los pisos de cada edificio:")
    for i, subred_piso in enumerate(subredes_pisos):
        print(f"Edificio {i+1}: {subred_piso}")
    
    print("\nSubredes para las conexiones entre routers ")
    for i, conexion in enumerate(conexiones_router):
        print(f"Conexión {i+1}: {conexion}")
    
    router_ips, conexion_ips = assign_routers_and_pisos(subred_edificios, subredes_pisos, conexiones_router)
  
    print("\nDirecciones IP para los routers:")
    for router, ip in router_ips.items():
        print(f"{router}: {ip}")
    
    print("\nDirecciones IP para las conexiones entre routers:")
    for conexion, ips in conexion_ips.items():
        print(f"{conexion}: {ips}")

except ValueError as e:
    print("Error:", e)
