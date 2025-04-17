import java.util.*;

/**
 * Traducción de P2.py a Java para el problema "Samus y el laberinto de Zebes".
 */
public class ProblemaP2 {
    // Clase para almacenar el estado previo y la acción tomada
    static class PreState {
        int prevPos, prevEnergy;
        String action;
        PreState(int p, int e, String a) { prevPos = p; prevEnergy = e; action = a; }
    }

    // Clase para el estado en la cola de prioridad (Dijkstra sobre (pos, energía))
    static class State implements Comparable<State> {
        int moves, pos, energy;
        State(int m, int p, int e) { moves = m; pos = p; energy = e; }
        public int compareTo(State other) {
            return Integer.compare(this.moves, other.moves);
        }
    }

    /**
     * Busca el número mínimo de acciones para llegar de la plataforma 0 a n.
     * @param n número de la plataforma final
     * @param e energía inicial
     * @param enemies conjunto de plataformas con robots (prohibidas)
     * @param jumpPlatforms mapa de plataformas con salto especial (plataforma->k)
     * @return número mínimo de acciones, o -1 si no es posible
     */
    public static int findShortestPath(int n, int e, Set<Integer> enemies, Map<Integer,Integer> jumpPlatforms) {
        final int INF = Integer.MAX_VALUE / 2;
        int[][] dp = new int[n+1][e+1];               // dp[pos][energy] = mín. acciones
        PreState[][] predecessor = new PreState[n+1][e+1];
        for (int i = 0; i <= n; i++) Arrays.fill(dp[i], INF);
        dp[0][e] = 0;

        PriorityQueue<State> pq = new PriorityQueue<>();
        pq.offer(new State(0, 0, e));

        while (!pq.isEmpty()) {
            State cur = pq.poll();
            int moves = cur.moves, pos = cur.pos, energy = cur.energy;

            if (pos == n) {
                // Reconstruir y mostrar el camino
                List<String> path = new ArrayList<>();
                int cp = pos, ce = energy;
                while (predecessor[cp][ce] != null) {
                    PreState ps = predecessor[cp][ce];
                    path.add(ps.action + " -> " + cp);
                    int tp = ps.prevPos, te = ps.prevEnergy;
                    cp = tp; ce = te;
                }
                path.add("Inicio -> 0");
                Collections.reverse(path);
                System.out.println("Camino tomado: " + String.join(" | ", path));
                return moves;
            }
            if (moves > dp[pos][energy]) continue;

            // 1) Caminar (+1/-1)
            for (int d : new int[]{1, -1}) {
                int np = pos + d;
                if (np >= 0 && np <= n && !enemies.contains(np)) {
                    if (moves + 1 < dp[np][energy]) {
                        dp[np][energy] = moves + 1;
                        String act = d > 0 ? "C+" : "C-";
                        predecessor[np][energy] = new PreState(pos, energy, act);
                        pq.offer(new State(moves + 1, np, energy));
                    }
                }
            }

            // 2) Salto con poder (S+k / S-k)
            if (jumpPlatforms.containsKey(pos)) {
                int jump = jumpPlatforms.get(pos);
                for (int d : new int[]{jump, -jump}) {
                    int np = pos + d;
                    if (np >= 0 && np <= n && !enemies.contains(np)) {
                        if (moves + 1 < dp[np][energy]) {
                            dp[np][energy] = moves + 1;
                            String act = d > 0 ? "S+" + jump : "S-" + jump;
                            predecessor[np][energy] = new PreState(pos, energy, act);
                            pq.offer(new State(moves + 1, np, energy));
                        }
                    }
                }
            }

            // 3) Teletransportación (consume energía)
            if (energy > 0) {
                for (int used = 1; used <= energy; used++) {
                    for (int d : new int[]{used, -used}) {
                        int np = pos + d;
                        int ne = energy - used;
                        if (np >= 0 && np <= n && !enemies.contains(np)) {
                            if (moves + 1 < dp[np][ne]) {
                                dp[np][ne] = moves + 1;
                                String act = d > 0 ? "T+" + used : "T-" + used;
                                predecessor[np][ne] = new PreState(pos, energy, act);
                                pq.offer(new State(moves + 1, np, ne));
                            }
                        }
                    }
                }
            }
        }

        return -1;  // No hay camino
    }

    public static void main(String[] args) {
        // Ejemplo hardcodeado (como en P2.py)
        int n = 32;
        int e = 4;
        Set<Integer> enemies = new HashSet<>(Arrays.asList(3, 7, 10, 13, 14, 17, 20, 24, 27, 29, 31));
        Map<Integer,Integer> jumpPlatforms = new HashMap<>();
        jumpPlatforms.put(1, 6);
        jumpPlatforms.put(4, 2);
        jumpPlatforms.put(6, 20);
        jumpPlatforms.put(8, 4);
        jumpPlatforms.put(11, 3);
        jumpPlatforms.put(15, 5);
        jumpPlatforms.put(18, 2);
        jumpPlatforms.put(22, 4);
        jumpPlatforms.put(25, 3);
        jumpPlatforms.put(28, 2);

        int result = findShortestPath(n, e, enemies, jumpPlatforms);
        if (result != -1) {
            System.out.println("El número mínimo de movimientos necesarios es: " + result);
        } else {
            System.out.println("NO SE PUEDE");
        }
    }
}
