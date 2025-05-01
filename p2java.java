import java.util.*;

public class p2java {
    /**
     * Encuentra el camino mas corto en terminos de acciones para que Samus llegue a la ultima plataforma.
     * 
     * @param n Numero de plataformas (sin contar la inicial)
     * @param e Unidades de energia iniciales
     * @param enemies Conjunto de plataformas con robots asesinos
     * @param jumpPlatforms Diccionario que mapea plataformas con poderes y la distancia de salto
     * @return Una tupla (numero de acciones, lista de acciones) o (-1, lista vacia) si no hay solucion
     */
    public static Pair<Integer, List<String>> findShortestPath(int n, int e, Set<Integer> enemies, Map<Integer, Integer> jumpPlatforms) {
        // Estados visitados: [posicion][energia] -> minimo numero de acciones
        Map<Integer, Map<Integer, Integer>> dp = new HashMap<>();
        // Para reconstruir el camino tomado
        Map<Integer, Map<Integer, Triple<Integer, Integer, String>>> predecessor = new HashMap<>();
        
        // Cola de prioridad: (movimientos, posicion, energia)
        PriorityQueue<int[]> pq = new PriorityQueue<>(
            Comparator.comparingInt(a -> a[0])
        );
        
        // Inicializar estructuras de datos
        for (int i = 0; i <= n; i++) {
            dp.put(i, new HashMap<>());
            predecessor.put(i, new HashMap<>());
        }
        
        // Verificar si hay robot en posicion 0 o n
        if (enemies.contains(0) || enemies.contains(n)) {
            return new Pair<>(-1, new ArrayList<>());
        }
        
        // Inicializar punto de partida
        pq.add(new int[]{0, 0, e});
        dp.get(0).put(e, 0);
        
        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int moves = current[0];
            int pos = current[1];
            int energy = current[2];
            
            // Si llegamos a la meta
            if (pos == n) {
                // Reconstruir el camino tomado
                List<String> actions = new ArrayList<>();
                int currentPos = pos;
                int currentEnergy = energy;
                
                while (currentPos != 0 || currentEnergy != e) {
                    Triple<Integer, Integer, String> prev = predecessor.get(currentPos).get(currentEnergy);
                    actions.add(prev.third);
                    currentPos = prev.first;
                    currentEnergy = prev.second;
                }
                
                // Invertir la lista de acciones
                Collections.reverse(actions);
                return new Pair<>(moves, actions);
            }
            
            // Si ya encontramos un camino mejor para este estado, continuamos
            if (dp.get(pos).containsKey(energy) && moves > dp.get(pos).get(energy)) {
                continue;
            }
            
            // 1. Teletransportacion
            for (int nextPos = 0; nextPos <= n; nextPos++) {
                if (nextPos != pos && !enemies.contains(nextPos)) {
                    int distance = Math.abs(nextPos - pos);
                    if (distance <= energy) { // Verificar si tenemos suficiente energia
                        int newEnergy = energy - distance;
                        Integer currentBest = dp.get(nextPos).getOrDefault(newEnergy, Integer.MAX_VALUE);
                        if (moves + 1 < currentBest) {
                            dp.get(nextPos).put(newEnergy, moves + 1);
                            int direction = nextPos - pos;
                            String action = "T" + direction; // Asegurar formato T-x
                            predecessor.get(nextPos).put(newEnergy, new Triple<>(pos, energy, action));
                            pq.add(new int[]{moves + 1, nextPos, newEnergy});
                        }
                    }
                }
            }
            
            // 2. Usar poder de salto si estamos en una plataforma con poder
            if (jumpPlatforms.containsKey(pos)) {
                int jumpDistance = jumpPlatforms.get(pos);
                int[][] jumps = {{jumpDistance, 1}, {-jumpDistance, -1}}; // (distancia, direccion)
                
                for (int[] jump : jumps) {
                    int nextPos = pos + jump[0];
                    String actionPrefix = "S" + (jump[1] > 0 ? "+" : "-");
                    
                    if (nextPos >= 0 && nextPos <= n && !enemies.contains(nextPos)) {
                        Integer currentBest = dp.get(nextPos).getOrDefault(energy, Integer.MAX_VALUE);
                        if (moves + 1 < currentBest) {
                            dp.get(nextPos).put(energy, moves + 1);
                            predecessor.get(nextPos).put(energy, new Triple<>(pos, energy, actionPrefix));
                            pq.add(new int[]{moves + 1, nextPos, energy});
                        }
                    }
                }
            }
            
            // 3. Movimientos basicos (caminar)
            int[][] walks = {{1, 1}, {-1, -1}}; // (distancia, direccion)
            
            for (int[] walk : walks) {
                int nextPos = pos + walk[0];
                String action = "C" + (walk[1] > 0 ? "+" : "-");
                
                if (nextPos >= 0 && nextPos <= n && !enemies.contains(nextPos)) {
                    Integer currentBest = dp.get(nextPos).getOrDefault(energy, Integer.MAX_VALUE);
                    if (moves + 1 < currentBest) {
                        dp.get(nextPos).put(energy, moves + 1);
                        predecessor.get(nextPos).put(energy, new Triple<>(pos, energy, action));
                        pq.add(new int[]{moves + 1, nextPos, energy});
                    }
                }
            }
        }
        
        // Si llegamos aqui, no hay solucion
        return new Pair<>(-1, new ArrayList<>());
    }
    
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int numCases = Integer.parseInt(scanner.nextLine());
        
        for (int i = 0; i < numCases; i++) {
            // Leer datos del caso
            String[] line = scanner.nextLine().split(" ");
            int n = Integer.parseInt(line[0]);
            int e = Integer.parseInt(line[1]);
            
            // Leer plataformas con robots
            Set<Integer> enemies = new HashSet<>();
            String enemiesLine = scanner.nextLine();
            if (!enemiesLine.isEmpty()) {
                String[] enemiesArr = enemiesLine.split(" ");
                for (String enemy : enemiesArr) {
                    enemies.add(Integer.parseInt(enemy));
                }
            }
            
            // Leer plataformas con poderes
            Map<Integer, Integer> jumpPlatforms = new HashMap<>();
            String powersLine = scanner.nextLine();
            if (!powersLine.isEmpty()) {
                String[] powersArr = powersLine.split(" ");
                for (int j = 0; j < powersArr.length; j += 2) {
                    if (j + 1 < powersArr.length) {
                        int platform = Integer.parseInt(powersArr[j]);
                        int jump = Integer.parseInt(powersArr[j + 1]);
                        jumpPlatforms.put(platform, jump);
                    }
                }
            }
            
            // Resolver el caso
            Pair<Integer, List<String>> result = findShortestPath(n, e, enemies, jumpPlatforms);
            
            // Imprimir resultado
            if (result.first == -1) {
                System.out.println("NO SE PUEDE");
            } else {
                System.out.print(result.first + " ");
                System.out.println(String.join(" ", result.second));
            }
        }
        
        scanner.close();
    }
    
    // Clase auxiliar para devolver pares de valores
    static class Pair<A, B> {
        A first;
        B second;
        
        Pair(A first, B second) {
            this.first = first;
            this.second = second;
        }
    }
    
    // Clase auxiliar para representar tripletas
    static class Triple<A, B, C> {
        A first;
        B second;
        C third;
        
        Triple(A first, B second, C third) {
            this.first = first;
            this.second = second;
            this.third = third;
        }
    }
}