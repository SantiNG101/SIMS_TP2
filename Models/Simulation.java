package Models;

import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Simulation {
    private final Params p;
    private final List<Particle> particles;
    private final Random rng;
    private final Path simDir;
    private Map<Integer, List<Particle>> grid;
    private final boolean periodic;
    private final double cellSize;

    public Simulation(Params p) throws IOException {
        this.p = p;
        this.particles = new ArrayList<>(p.N);
        this.rng = p.seed==null? new Random():new Random(p.seed);
        this.periodic = true;
        cellSize = p.L / p.M;

        long ts = System.currentTimeMillis() / 1000L;
        this.simDir = Paths.get(p.outDir + "/sims", "sim_" + ts);
        Files.createDirectories(simDir);

        generateParticles();
        computeCellNeighbors();
    }

    private void generateParticles() {
        // Inicialización de partículas en posiciones y angulo aleatorios dentro del espacio
        for (int i = 0; i < p.N; i++) {
            double x = rng.nextDouble() * p.L;
            double y = rng.nextDouble() * p.L;
            double theta = rng.nextDouble() * 2.0 * Math.PI;
            particles.add(new Particle(x, y, theta,i));
        }
    }

    private void initializeGrid() {
        grid = new HashMap<>();
        for (Particle particle : particles) {
            int cellX = (int) (particle.getX() / cellSize);
            int cellY = (int) (particle.getY() / cellSize);
            int cellIndex = cellX + cellY * p.M;
            grid.computeIfAbsent(cellIndex, k -> new ArrayList<>()).add(particle);
        }
    }

    private int getCellIndex(Particle particle) {
        int cellX = (int) (particle.getX() / cellSize);
        int cellY = (int) (particle.getY() / cellSize);
        return cellX + cellY * p.M;
    }

    private Map<Integer, List<Integer>> cellNeighbors;

    private void computeCellNeighbors() {
        cellNeighbors = new HashMap<>();

        for (int cellY = 0; cellY < p.M; cellY++) {
            for (int cellX = 0; cellX < p.M; cellX++) {
                int cellIndex = cellX + cellY * p.M;
                List<Integer> neighbors = new ArrayList<>();

                for (int dx = 0; dx <= 1; dx++) {
                    for (int dy = -1; dy <= 1; dy++) {
                        if ( dx==0 && dy==-1 ) continue;
                        int neighborCellX = cellX + dx;
                        int neighborCellY = cellY + dy;

                        if (periodic) {
                            neighborCellX = (neighborCellX + p.M) % p.M;
                            neighborCellY = (neighborCellY + p.M) % p.M;
                        }

                        if (!periodic && (neighborCellX < 0 || neighborCellX >= p.M || neighborCellY < 0 || neighborCellY >= p.M)) {
                            continue;
                        }

                        int neighborCellIndex = neighborCellX + neighborCellY * p.M;
                        neighbors.add(neighborCellIndex);
                    }
                }
                cellNeighbors.put(cellIndex, neighbors);
            }
        }
    }

    public void updateParticles() {
        for (Particle pi : particles) {     //! paralelizable
            pi.registerCloseParticle(pi);       // it has to consider itself to calculate the mean
            double meanAngle = pi.getMeanAngle(p.N);
            double noise = rng.nextDouble() * p.eta - (p.eta / 2.0);
            pi.setTheta(wrapAngle(meanAngle + noise));
            pi.setX(wrapPos(pi.getX() + p.v * Math.cos(pi.getTheta()), p.L));
            pi.setY(wrapPos(pi.getY() + p.v * Math.sin(pi.getTheta()), p.L));
            pi.resetMeanAngle();
        }
    }

    public void findNeighborsCIM() {
        final double r2 = p.r * p.r;
        for (Particle p1 : particles) {
            int cellX = (int) (p1.getX() / cellSize);
            int cellY = (int) (p1.getY() / cellSize);
            int cellIndex = cellX + cellY * p.M;

            for (int neighborIndex : cellNeighbors.get(cellIndex)) {
                for (Particle p2 : grid.getOrDefault(neighborIndex, new ArrayList<>())) {
                    if (neighborIndex==cellIndex && p1.getId() >= p2.getId()) continue;

                    if (calculateDistance(p2, p1) <= r2 ) {
                        Particle.registerCloseParticles(p1, p2);
                    }
                }
            }

        }

    }

    public void runCIM() throws IOException {
        writeStep(0);

        for (int t = 1; t <= p.steps; t++) {
            initializeGrid();
            findNeighborsCIM();
            updateParticles();
            if (t % p.saveEvery == 0) writeStep(t);
        }
    }


    public void runBruteForce() throws IOException {
        writeStep(0);

        double[] newTheta = new double[p.N];
        double r2 = p.r * p.r;

        for (int t = 1; t <= p.steps; t++) {
            // Actualizar ángulos
            for (int i = 0; i < p.N; i++) {
                double c = 0.0, s = 0.0, count = 0;
                Particle pi = particles.get(i);

                // Buscamos los vecinos dentro del radio r
                for (int j = 0; j < p.N; j++) {
                    Particle pj = particles.get(j);
                    double dx = minImage(pj.getX() - pi.getX(), p.L);
                    double dy = minImage(pj.getY() - pi.getY(), p.L);

                    // Si está dentro del radio de interacción, contribuye al promedio
                    if (dx*dx + dy*dy <= r2) {
                        c += Math.cos(pj.getTheta());
                        s += Math.sin(pj.getTheta());
                        count++;
                    }
                }

                // Calculamos el ángulo promedio de vecinos
                // Si no hay vecinos, usamos el ángulo actual
                double meanAngle = (count > 0) ? Math.atan2(s/ count, c/ count) : pi.getTheta();

                // Añadimos ruido al ángulo promedio en el rango [-eta/2, eta/2]
                double noise = rng.nextDouble() * p.eta - (p.eta / 2.0);

                newTheta[i] = wrapAngle(meanAngle + noise);
            }

            // Actualizar posiciones de las partículas
            for (int i = 0; i < p.N; i++) {
                Particle pi = particles.get(i);
                pi.setTheta(newTheta[i]);
                pi.setX(wrapPos(pi.getX() + p.v * Math.cos(pi.getTheta()), p.L));;
                pi.setY(wrapPos(pi.getY() + p.v * Math.sin(pi.getTheta()), p.L));;
            }

            if (t % p.saveEvery == 0) writeStep(t);
        }
    }

    private void writeStep(int t) throws IOException {
        Path stepsDir = simDir.resolve("steps");
        Files.createDirectories(stepsDir);

        Path file = stepsDir.resolve(String.format("step_%03d.csv", t));

        try (BufferedWriter bw = Files.newBufferedWriter(file)) {
            bw.write("id,x,y,vx,vy\n");
            for (int i = 0; i < particles.size(); i++) {
                Particle ptl = particles.get(i);
                bw.write(String.format(Locale.US, "%d,%.6f,%.6f,%.6f,%.6f%n",
                        i, ptl.getX(), ptl.getY(), ptl.vx(p.v), ptl.vy(p.v)));
            }
        }
    }

    public Path getSimDir() { return simDir; }

    private static double minImage(double d, double L) {
        d = d - Math.rint(d / L) * L;
        return d;
    }

    // Asegura que la posición esté en [0, L)
    private static double wrapPos(double a, double L) {
        a = a % L;
        if (a < 0) a += L;
        return a;
    }

    // Asegura que el ángulo esté en [0, 2π)
    private static double wrapAngle(double ang) {
        double twoPi = 2.0 * Math.PI;
        ang = ang % twoPi;
        if (ang < 0) ang += twoPi;
        return ang;
    }

    private double calculateDistance(Particle pj, Particle pi) {
        double dx = minImage(pj.getX() - pi.getX(), p.L);
        double dy = minImage(pj.getY() - pi.getY(), p.L);
        return dx*dx + dy*dy;
    }

}