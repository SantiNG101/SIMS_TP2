package Tests;

import Models.Params;
import Models.SimulationMain;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;

public class RunOneCIMSimulation {
    @Test
    public void test() throws IOException, InterruptedException {
        // mismo conjunto de parámetros para ambos
        double eta = 1, v= 0.03, l=20.0;
        int n = 1000;
        String outDir = "outputs/eta" + eta + "_v" + v + "_d" + n/(l*l);
        Params p = new Params(eta, v, l, n, outDir);
        p.setSeed(20);

        long startTimeBF = System.nanoTime();
        Path simDir = SimulationMain.runSimpleSimulation(p,false);
        long endTimeBF = System.nanoTime();
        long durationBF = TimeUnit.NANOSECONDS.toMillis(endTimeBF - startTimeBF);
        System.out.println("Execution Time: " + durationBF + " ms");

        PythonVisualize.animate_vectors(outDir,simDir);
    }
}
