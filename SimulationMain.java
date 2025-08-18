import java.io.*;

public class SimulationMain {
    public static void main(String[] args) throws IOException {
        Params p = Params.fromArgs(args);

        Simulation sim = new Simulation(p);
        sim.runCIM();
        System.out.println("Simulación terminada en: " + sim.getSimDir().toAbsolutePath());
    }
}

class Params {
    int N = 500;
    double L = 40.0;
    int M = 10;
    double v = 0.3;
    double eta = 0.3;
    double r = 1;
    int steps = 1000;
    long seed = 7L;
    int saveEvery = 1;
    String outDir = "outputs";

    static Params fromArgs(String[] args) {
        Params p = new Params();
        for (String a : args) {
            if (!a.startsWith("--")) continue;
            String[] kv = a.substring(2).split("=", 2);
            if (kv.length != 2) continue;
            String k = kv[0].toLowerCase();
            String v = kv[1];
            switch (k) {
                case "n": p.N = Integer.parseInt(v); break;
                case "l": p.L = Double.parseDouble(v); break;
                case "v": p.v = Double.parseDouble(v); break;
                case "eta": p.eta = Double.parseDouble(v); break;
                case "r": p.r = Double.parseDouble(v); break;
                case "steps": p.steps = Integer.parseInt(v); break;
                case "seed": p.seed = Long.parseLong(v); break;
                case "save_every": p.saveEvery = Integer.parseInt(v); break;
                case "out_dir": p.outDir = v; break;
            }
        }
        return p;
    }
}