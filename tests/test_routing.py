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


try:

    pisos_por_edificio = [8, 3, 4, 6]

    result = calculate_network_base(edificios=len(pisos_por_edificio), pisos_maximo= max(pisos_por_edificio), pcs_por_piso=30, ip_base_str="192.162.0.0", ip_base_edificios="172.16.10.0")


    #Outputs, se modifica para la response

    print("IP Base:", result["ip_base"])
    print("Máscara:", result["mascara"])
    print("Direcciones totales:", result["direcciones_totales"])
    print("Bits usados para edificios:", result["bits_edificios"])
    print("Bits usados para pisos:", result["bits_pisos"])
    print("Bits usados para computadoras:", result["bits_computadoras"])

    print(" ")
    print("subredes para los edificios")
    subred_edificios = list(result["ip_base"].subnets(prefixlen_diff=result["bits_edificios"]))
    print(subred_edificios)
    print(" ")

    print("subredes para los pisos de cada edificio")

    for i, subred_edificio in enumerate(subred_edificios):
            subred_pisos = list(subred_edificio.subnets(prefixlen_diff=result["bits_pisos"]))[:pisos_por_edificio[i]]
            print(subred_pisos)
            print(" ")

    print("Ips para los hosts de cada piso de cada edificio")
    for i, subred_edificio in enumerate(subred_edificios):
        print("")
        print("Edificio ", subred_edificio)
        print(" ")

        # Aqui aumenta una subred por edificio (como si fuera un piso más) para los la conexion entre routers.

        subred_pisos = list(subred_edificio.subnets(prefixlen_diff=result["bits_pisos"]))[:pisos_por_edificio[i]]
        for subred_piso in subred_pisos:
            print("Piso ", subred_piso)
            host_piso = list(subred_piso.hosts())
            print("Cantidad de hosts ", len(host_piso))
            print("Hosts ", host_piso)
            print(" ")


except ValueError as e:
    print("Error:", e)

