## Algoritmo de subneteo
Se presenta un objeto con una red de las siguientes características:
- Se provee una dirección base `192.162.0.0`
- 4 Edificios
	- El primer edificio: 6 pisos.
		- El primero posee 20 hosts, con 3 subredes "*Cuartos*", con hosts entre 30 y 70.
		- Los demás pisos presentan entre 30 y 20 hosts.
	- Los 3 edificios restantes presentan 7, 7 y 8 pisos, cada uno con 30 o 20 hosts.

*Resultados*
```
- Router: Central, Network: 192.162.0.0/18
  - Router: Edificios-1, Network: 192.162.0.0/20
    - Router: Pisos-1, Network: 192.162.0.0/23
      - Router: Cuartos-1, Network: 192.162.0.0/25
      - Router: Cuartos-2, Network: 192.162.0.128/25
      - Router: Cuartos-3, Network: 192.162.1.0/25
    - Router: Pisos-2, Network: 192.162.2.0/23
    - Router: Pisos-3, Network: 192.162.4.0/23
    - Router: Pisos-4, Network: 192.162.6.0/23
    - Router: Pisos-5, Network: 192.162.8.0/23
    - Router: Pisos-6, Network: 192.162.10.0/23
  - Router: Edificios-2, Network: 192.162.16.0/20
    - Router: Pisos-1, Network: 192.162.16.0/23
    - Router: Pisos-2, Network: 192.162.18.0/23
    - Router: Pisos-3, Network: 192.162.20.0/23
    - Router: Pisos-4, Network: 192.162.22.0/23
    - Router: Pisos-5, Network: 192.162.24.0/23
    - Router: Pisos-6, Network: 192.162.26.0/23
    - Router: Pisos-7, Network: 192.162.28.0/23
  - Router: Edificios-3, Network: 192.162.32.0/20
    - Router: Pisos-1, Network: 192.162.32.0/23
    - Router: Pisos-2, Network: 192.162.34.0/23
    - Router: Pisos-3, Network: 192.162.36.0/23
    - Router: Pisos-4, Network: 192.162.38.0/23
    - Router: Pisos-5, Network: 192.162.40.0/23
    - Router: Pisos-6, Network: 192.162.42.0/23
    - Router: Pisos-7, Network: 192.162.44.0/23
  - Router: Edificios-4, Network: 192.162.48.0/20
    - Router: Pisos-1, Network: 192.162.48.0/23
    - Router: Pisos-2, Network: 192.162.50.0/23
    - Router: Pisos-3, Network: 192.162.52.0/23
    - Router: Pisos-4, Network: 192.162.54.0/23
    - Router: Pisos-5, Network: 192.162.56.0/23
    - Router: Pisos-6, Network: 192.162.58.0/23
    - Router: Pisos-7, Network: 192.162.60.0/23
    - Router: Pisos-8, Network: 192.162.62.0/23
```

## Algoritmo Genético para determinar la menor ruta posible
Se emplea una matriz de adyacencia:

```
[  
    [0, 5, 4, 5, 6, 3, 20, np.inf, np.inf, np.inf, 10, np.inf, np.inf, np.inf],  
    [5, 0, np.inf, 4, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [4, np.inf, 0, 2, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [5, 4, 2, 0, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [6, np.inf, np.inf, np.inf, 0, 4, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [3, np.inf, np.inf, np.inf, 4, 0, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [20, np.inf, np.inf, np.inf, np.inf, np.inf, 0, 2, 5, 4, 25, np.inf, np.inf, np.inf],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 2, 0, 4, np.inf, np.inf, np.inf, np.inf, np.inf],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 5, 4, 0, 5, np.inf, np.inf, np.inf, np.inf],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, np.inf, 5, 0, np.inf, np.inf, np.inf, np.inf],  
    [10, np.inf, np.inf, np.inf, np.inf, np.inf, 25, np.inf, np.inf, np.inf, 0, 2, 3, 4],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 2, 0, 4, 5],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 3, 4, 0, 5],  
    [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, 4, 5, 5, 0]  
]
```

Esta representa las distancias y conexiones de la siguiente red:
![[red-ejemplo.png]]

Encontrando las rutas optimas entre:
- R1 - R14:
	- `{'solucion': [0, 10, 13], 'costo': np.float64(14.0)}`
- R11 - R14:
	- `{'solucion': [10, 13], 'costo': np.float64(4.0)}`
- R2 - R9:
	- `{'solucion': [2, 0, 6, 8], 'costo': np.float64(29.0)}`