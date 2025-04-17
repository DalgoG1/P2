from collections import defaultdict
from heapq import heappush, heappop

def find_shortest_path(n: int, e: int, enemies: set[int], jump_platforms: dict) -> int:
    dp = defaultdict(lambda: defaultdict(lambda: float('inf')))
    predecessor = defaultdict(dict)  # predecessor[pos][energy] = (prev_pos, prev_energy, action)
    
    pq = [(0, 0, e)]
    dp[0][e] = 0
    
    while pq:
        moves, pos, energy = heappop(pq)
        
        if pos == n:
            # Reconstruir el camino
            path = []
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
def main():
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