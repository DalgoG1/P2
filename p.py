import sys
from collections import defaultdict
from heapq import heappush, heappop

def find_shortest_path(n, e, enemies, jump_platforms):
    """
    Encuentra el camino más corto en términos de acciones para que Samus llegue a la última plataforma.
    
    Args:
        n: Número de plataformas (sin contar la inicial)
        e: Unidades de energía iniciales
        enemies: Conjunto de plataformas con robots asesinos
        jump_platforms: Diccionario que mapea plataformas con poderes y la distancia de salto
    
    Returns:
        Una tupla (número de acciones, lista de acciones) o ("NO SE PUEDE", [])
    """
    # Estados visitados: (posición, energía) -> mínimo número de acciones
    dp = defaultdict(lambda: defaultdict(lambda: float('inf')))
    # Para reconstruir el camino tomado
    predecessor = defaultdict(dict)  # predecessor[pos][energy] = (prev_pos, prev_energy, action)
    
    # Cola de prioridad: (movimientos, posición, energía)
    pq = [(0, 0, e)]
    dp[0][e] = 0
    
    # Verificar si hay robot en posición 0 o n
    if 0 in enemies or n in enemies:
        return -1, []
    
    while pq:
        moves, pos, energy = heappop(pq)
        
        # Si llegamos a la meta
        if pos == n:
            # Reconstruir el camino tomado
            actions = []
            current_pos, current_energy = pos, energy
            
            while current_pos != 0 or current_energy != e:
                prev_pos, prev_energy, action = predecessor[current_pos][current_energy]
                actions.append(action)
                current_pos, current_energy = prev_pos, prev_energy
            
            actions.reverse()
            return moves, actions
        
        # Si ya encontramos un camino mejor para este estado, continuamos
        if moves > dp[pos][energy]:
            continue
        

                    
        # 1. Teletransportación
        for next_pos in range(n + 1):
            if next_pos != pos and next_pos not in enemies:
                distance = abs(next_pos - pos)
                if distance <= energy:  # Verificar si tenemos suficiente energía
                    new_energy = energy - distance
                    if moves + 1 < dp[next_pos][new_energy]:
                        dp[next_pos][new_energy] = moves + 1
                        direction = next_pos - pos
                        action = f"T{direction}" if direction > 0 else f"T{direction}"  # Asegurar formato T-x
                        predecessor[next_pos][new_energy] = (pos, energy, action)
                        heappush(pq, (moves + 1, next_pos, new_energy))
        
        # 2. Usar poder de salto si estamos en una plataforma con poder
        if pos in jump_platforms:
            jump_distance = jump_platforms[pos]
            for delta, action_prefix in [(jump_distance, "S+"), (-jump_distance, "S-")]:
                next_pos = pos + delta
                if 0 <= next_pos <= n and next_pos not in enemies:
                    if moves + 1 < dp[next_pos][energy]:
                        dp[next_pos][energy] = moves + 1
                        predecessor[next_pos][energy] = (pos, energy, action_prefix)
                        heappush(pq, (moves + 1, next_pos, energy))
                        
        # 3. Movimientos básicos (caminar)
        for delta, action in [(1, "C+"), (-1, "C-")]:
            next_pos = pos + delta
            if 0 <= next_pos <= n and next_pos not in enemies:
                if moves + 1 < dp[next_pos][energy]:
                    dp[next_pos][energy] = moves + 1
                    predecessor[next_pos][energy] = (pos, energy, action)
                    heappush(pq, (moves + 1, next_pos, energy))

    
    # Si llegamos aquí, no hay solución
    return -1, []

def main():
    lines = sys.stdin.read().strip().split('\n')
    num_cases = int(lines[0])
    
    line_index = 1
    for _ in range(num_cases):
        # Leer datos del caso
        n, e = map(int, lines[line_index].split())
        line_index += 1
        
        # Leer plataformas con robots
        enemies = set()
        if lines[line_index].strip():  # Si hay robots
            enemies = set(map(int, lines[line_index].split()))
        line_index += 1
        
        # Leer plataformas con poderes
        jump_platforms = {}
        if lines[line_index].strip():  # Si hay poderes
            powers = list(map(int, lines[line_index].split()))
            for i in range(0, len(powers), 2):
                if i+1 < len(powers):
                    platform, jump = powers[i], powers[i+1]
                    jump_platforms[platform] = jump
        line_index += 1
        
        # Resolver el caso
        result, actions = find_shortest_path(n, e, enemies, jump_platforms)
        
        # Imprimir resultado
        if result == -1:
            sys.stdout.write("NO SE PUEDE\n")
        else:
            sys.stdout.write(f"{result} {' '.join(actions)}\n")

if __name__ == "__main__":
    main()