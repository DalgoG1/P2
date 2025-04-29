from collections import defaultdict
from heapq import heappush, heappop

def find_shortest_path(n: int, e: int, enemies: set[int], jump_platforms: dict) -> list[str]:
    dp = defaultdict(lambda: defaultdict(lambda: float('inf')))
    predecessor = defaultdict(dict)  # predecessor[pos][energy] = (prev_pos, prev_energy, action)
    
    pq = [(0, 0, e)]
    dp[0][e] = 0
    path = []
    
    
    if e >= n:
        return 1
    if 0 in enemies:
        return -1
    if n in enemies:
        return -1
    
    while pq:
        moves, pos, energy = heappop(pq)
        
        if pos == n:
            # Reconstruir el camino
            current_pos, current_energy = pos, energy
            while True:
                prev_info = predecessor.get(current_pos, {}).get(current_energy, None)
                if prev_info is None:
                    break
                prev_pos, prev_energy, action = prev_info
                path.append(f"{action} -> {current_pos}")
                current_pos, current_energy = prev_pos, prev_energy
            path.append(f"Inicio -> 0")
            path.reverse()
            print("Camino tomado:", " | ".join(path))
            return moves
            
        if moves > dp[pos][energy]:
            continue
            
        # Movimientos básicos
        for next_pos in [pos + 1, pos - 1]:
            if 0 <= next_pos <= n and next_pos not in enemies:
                if moves + 1 < dp[next_pos][energy]:
                    dp[next_pos][energy] = moves + 1
                    action = "C+" if next_pos > pos else "C-"
                    predecessor[next_pos][energy] = (pos, energy, action)
                    heappush(pq, (moves + 1, next_pos, energy))
                    
        # Saltos desde plataforma
        if pos in jump_platforms:
            jump = jump_platforms[pos]
            for next_pos in [pos + jump, pos - jump]:
                if 0 <= next_pos <= n and next_pos not in enemies:
                    if moves + 1 < dp[next_pos][energy]:
                        dp[next_pos][energy] = moves + 1
                        action = f"S+{jump}" if next_pos > pos else f"S-{jump}"
                        predecessor[next_pos][energy] = (pos, energy, action)
                        heappush(pq, (moves + 1, next_pos, energy))
        
        # Teletransporte con energía
        if energy > 0:
            for e_used in range(1, energy + 1):
                for next_pos in [pos + e_used, pos - e_used]:
                    if 0 <= next_pos <= n and next_pos not in enemies:
                        new_energy = energy - e_used
                        if moves + 1 < dp[next_pos][new_energy]:
                            dp[next_pos][new_energy] = moves + 1
                            action = f"T+{e_used}" if next_pos > pos else f"T-{e_used}"
                            predecessor[next_pos][new_energy] = (pos, energy, action)
                            heappush(pq, (moves + 1, next_pos, new_energy))
    
    return -1

# Ejemplo de uso (se mantiene igual)
import random
from random import randint

def main():
    random.seed(42)  # Para reproducibilidad
    n = 10**5       # 100,000 plataformas
    e = (500000)  # Energía aleatoria
    enemies = set()
    jump_platforms = {}
    
    # Generar enemigos (30% de las plataformas, excluyendo 0 y n)
    for pos in range(1, n):
        if random.random() < 0.3:  # 30% de probabilidad de ser enemigo
            enemies.add(pos)
    
    # Generar plataformas de salto (20% de las plataformas no enemigas)
    for pos in range(n):
        if pos not in enemies and random.random() < 0.2:
            jump = randint(1, 1000)  # Salto aleatorio entre 1 y 1000
            jump_platforms[pos] = jump
    
    # Asegurar que haya al menos un camino válido (0 → 50000 → n)
    if 50000 not in enemies:
        jump_platforms[50000] = n - 50000  # Salto directo a n
    
    result = find_shortest_path(n, e, enemies, jump_platforms)
    print(f"Movimientos mínimos: {result}")

if __name__ == "__main__":
    main()