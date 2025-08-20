package Models;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Locale;

public class SimulationMain {
    public static String runSimpleSimulation(Params p, Boolean useBruteForce) throws IOException {
        Simulation sim = new Simulation(p);
        if (useBruteForce) sim.runBruteForce(); else sim.runCIM();
        System.out.println("Simulación " + (useBruteForce? "BruteForce":"CIM") + " terminada en: " + sim.getSimDir().toAbsolutePath());
        return sim.getSimDir().toString();
    }

    public static void main(String[] args) throws IOException {
        int n_runs = args.length==0? 1:Integer.parseInt(args[0]);

        double eta_values[] = {0.1};
        double v_values[] = {0.3};
        double L[] = {20.0};
        int N[] = {500};


        for (double eta : eta_values) {
            for (double v : v_values) {
                for (double l : L) {
                    for (int n : N) {

                        String outDir = "outputs/eta" + eta + "_v" + v + "_d" + n/(l*l);
                        Params p = new Params(eta, v, l, n, outDir);

                        for (int runs = 0; runs < n_runs; runs++) {
                            Simulation sim = new Simulation(p);
                            sim.runCIM();
                            System.out.println("Simulación " + runs + " terminada en: " + sim.getSimDir().toAbsolutePath());
                        }

                        // Guardar params
                        try (BufferedWriter bw = Files.newBufferedWriter(Paths.get(outDir).resolve("params.csv"))) {
                            bw.write("N,L,rho,v,eta,r,steps,save_every\n");
                            bw.write(String.format(Locale.US, "%d,%.3f,%.3f,%.3f,%.3f,%.3f,%d,%d\n", n, l, n / (l*l), v, eta, p.r, p.steps, p.saveEvery));
                        }
                    }
                }
            }
        }


    }
}

