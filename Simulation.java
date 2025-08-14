import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Simulation {
    private final Params p;
    private final List<Particle> particles = new ArrayList<>();
    private final Random rng;
    private final Path simDir;

    Simulation(Params p) throws IOException {
        this.p = p;
        this.rng = new Random(p.seed);
        long ts = System.currentTimeMillis() / 1000L;
        this.simDir = Paths.get(p.outDir, "sim_" + ts);
        Files.createDirectories(simDir);

        // Guardar params
        try (BufferedWriter bw = Files.newBufferedWriter(simDir.resolve("params.txt"))) {
            bw.write("N=" + p.N + "\n");
            bw.write("L=" + p.L + "\n");
            bw.write("v=" + p.v + "\n");
            bw.write("eta=" + p.eta + "\n");
            bw.write("r=" + p.r + "\n");
            bw.write("steps=" + p.steps + "\n");
            bw.write("seed=" + p.seed + "\n");
            bw.write("save_every=" + p.saveEvery + "\n");
        }

        // Inicialización
        for (int i = 0; i < p.N; i++) {
            double x = rng.nextDouble() * p.L;
            double y = rng.nextDouble() * p.L;
            double theta = rng.nextDouble() * 2.0 * Math.PI;
            particles.add(new Particle(x, y, theta));
        }
    }

    void run() throws IOException {
        writeStep(0);

        double[] newTheta = new double[p.N];
        double r2 = p.r * p.r;

        for (int t = 1; t <= p.steps; t++) {
            // Actualizar ángulos
            for (int i = 0; i < p.N; i++) {
                double c = 0.0, s = 0.0;
                Particle pi = particles.get(i);
                for (int j = 0; j < p.N; j++) {
                    Particle pj = particles.get(j);
                    double dx = minImage(pj.getX() - pi.getX(), p.L);
                    double dy = minImage(pj.getY() - pi.getY(), p.L);
                    if (dx*dx + dy*dy <= r2) {
                        c += Math.cos(pj.getTheta());
                        s += Math.sin(pj.getTheta());
                    }
                }
                double meanAngle = Math.atan2(s/p.N, c/p.N);
                double noise = rng.nextDouble() * p.eta - (p.eta / 2.0);
                newTheta[i] = wrapAngle(meanAngle + noise);
            }

            // Aplicar y mover
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
        Path file = simDir.resolve(String.format("step_%03d.csv", t));
        try (BufferedWriter bw = Files.newBufferedWriter(file)) {
            bw.write("id,x,y,vx,vy\n");
            for (int i = 0; i < particles.size(); i++) {
                Particle ptl = particles.get(i);
                bw.write(String.format(Locale.US, "%d,%.6f,%.6f,%.6f,%.6f%n",
                        i, ptl.getX(), ptl.getY(), ptl.vx(p.v), ptl.vy(p.v)));
            }
        }
    }

    Path getSimDir() { return simDir; }

    private static double minImage(double d, double L) {
        d = d - Math.rint(d / L) * L;
        return d;
    }
    private static double wrapPos(double a, double L) {
        a = a % L;
        if (a < 0) a += L;
        return a;
    }
    private static double wrapAngle(double ang) {
        double twoPi = 2.0 * Math.PI;
        ang = ang % twoPi;
        if (ang < 0) ang += twoPi;
        return ang;
    }
}