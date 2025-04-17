from collections import defaultdict
from typing import List, Set
from heapq import heappush, heappop

def find_shortest_path(n: int, e: int, enemies: Set[int], jump_platforms: dict) -> int:
    """
    n: número total de plataformas
    e: unidades de energía
    enemies: conjunto de plataformas con enemigos
    jump_platforms: diccionario donde key=plataforma, value=cantidad de saltos permitidos
    """
    
    # Inicializamos dp como un diccionario de diccionarios
    # dp[pos][energy] = mínimo número de movimientos para llegar a la plataforma n
    dp = defaultdict(lambda: defaultdict(lambda: float('inf')))
    
    # Cola de prioridad: (movimientos, posición, energía)
    pq = [(0, 0, e)]  # Comenzamos en la posición 0 con e unidades de energía
    dp[0][e] = 0
    
    path = []
    
    while pq:
        moves, pos, energy = heappop(pq)
        
        # Si llegamos a la última plataforma
        if pos == n:
            return moves
            
        # Si esta no es la mejor forma de llegar a esta posición con esta energía
        if moves > dp[pos][energy]:
            continue
            
        # Movimientos básicos (adelante y atrás)
        for next_pos in [pos + 1, pos - 1]:
            if 0 <= next_pos <= n and next_pos not in enemies:
                if moves + 1 < dp[next_pos][energy]:
                    dp[next_pos][energy] = moves + 1
                    # print(f"Moviendo a {next_pos} desde {pos}")
                    heappush(pq, (moves + 1, next_pos, energy))
        
        # Saltar si la plataforma actual lo permite
        if pos in jump_platforms:
            jumps = jump_platforms[pos]
            for next_pos in [pos + jumps, pos - jumps]:
                if 0 <= next_pos <= n and next_pos not in enemies:
                    if moves + 1 < dp[next_pos][energy]:
                        dp[next_pos][energy] = moves + 1
                        # print(f"Saltando a {next_pos} desde {pos}")
                        heappush(pq, (moves + 1, next_pos, energy))
        
        # Usar energía para teletransporte
        if energy > 0:
            for e_used in range(1, energy + 1):
                for next_pos in [pos + e_used, pos - e_used]:
                    if 0 <= next_pos <= n and next_pos not in enemies:
                        if moves + 1 < dp[next_pos][energy - e_used]:
                            dp[next_pos][energy - e_used] = moves + 1
                            # print(f"Usando {e_used} energía para mover a {next_pos} desde {pos}")
                            heappush(pq, (moves + 1, next_pos, energy - e_used))
    
    return -1  # No hay camino posible

# Ejemplo de uso
def main():
    # Ejemplo de entrada
    # n = 14  # 10 plataformas
    # e = 2   # 5 unidades de energía
    # enemies = {4, 5, 7, 9, 10, 12}  # Plataformas con enemigos
    # teleport_platforms = {1: 7, 3: 2, 6: 5, 11: 3}  # Plataforma 2 permite saltar 3 espacios, plataforma 5 permite saltar 4
    
    # n = 14
    # e = 3
    # enemies = {4, 5, 7, 9, 10, 12}
    # teleport_platforms = {1: 7, 3: 2, 6: 5, 11: 3}
    
    # n = 9
    # e = 2
    # enemies = {4, 5, 7}
    # teleport_platforms = {1: 3, 3: 2, 6: 5}
    
    n = 32
    e = 4
    enemies = {3, 7, 10, 13, 14, 17, 20, 24, 27, 29, 31}
    teleport_platforms = {1: 6, 4: 2, 6:20, 8: 4, 11: 3, 15: 5, 18: 2, 22: 4, 25: 3, 28: 2}
    
    result = find_shortest_path(n, e, enemies, teleport_platforms)
    
    if result != -1:
        print(f"El número mínimo de movimientos necesarios es: {result}")
    else:
        print("NO SE PUEDE")

if __name__ == "__main__":
    main()
