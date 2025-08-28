package Tests;

import java.io.IOException;
import java.nio.file.Path;

import org.junit.jupiter.api.Test;
import Models.Params;
import Models.SimulationMain;

import java.util.concurrent.TimeUnit;

public class RunFVMSimulations {
        Double v = 0.03;

        @Test
        public void testSingleSimulation() throws IOException, InterruptedException {
                // mismo conjunto de parámetros para ambos
                Double eta = 0.05, l=10.0;
                int n = 500;
                String outDir = "outputs/eta" + eta + "_v" + v + "_d" + n/(l*l);
                Params p = new Params(eta, v, l, n, outDir,2000);
                //  p.setSeed(20);

                Path simDir = SimulationMain.runSimpleSimulationUsingOneRandomNeighbor(p);
                PythonVisualize.animate_vectors(outDir,simDir.getFileName().toString());
        }


        @Test
        public void testMultipleSimulations() throws IOException, InterruptedException {
                double[] eta_values = {0.0, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0};
                double[] v_values = {0.03};
                double[] L = {10.0};
                int[] N = {500};
                int n_runs =10, steps =2000;
                long startTimeBF = System.nanoTime();
                SimulationMain.runMultipleSimulations(n_runs,eta_values,v_values,L,N,steps,true);
                long endTimeBF = System.nanoTime();
                long durationBF = TimeUnit.NANOSECONDS.toMillis(endTimeBF - startTimeBF);
                System.out.println("Execution Time: " + durationBF + " ms");

                PythonVisualize.plot_n_simulations();
                PythonVisualize.animate_vectors_n_simulations();
        }

        @Test
        public void animateMultipleSimulations() throws IOException, InterruptedException {
                System.out.println("Starting animations");
                PythonVisualize.animate_vectors_n_simulations();
        }

        @Test
        public void animateSingleSimulation() throws IOException, InterruptedException {
                // mismo conjunto de parámetros para ambos
                Double eta = 0.05, l=10.0;
                int n = 500;
                String outDir = "outputs/eta" + eta + "_v" + v + "_d" + n/(l*l);
                String simDirName = "sim_1756403667_146" + ".csv";

                PythonVisualize.animate_vectors(outDir,simDirName);
        }


}


