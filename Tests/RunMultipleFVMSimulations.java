package Tests;

import Models.SimulationMain;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

public class RunMultipleFVMSimulations {

        @Test
        public void test() throws IOException, InterruptedException {
            double[] eta_values = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0};
            double[] v_values = {0.03};
            double[] L = {10.0};
            int[] N = {500};
            int n_runs =5, steps =100;
            long startTimeBF = System.nanoTime();
            SimulationMain.runMultipleSimulations(n_runs,eta_values,v_values,L,N,steps,true);
            long endTimeBF = System.nanoTime();
            long durationBF = TimeUnit.NANOSECONDS.toMillis(endTimeBF - startTimeBF);
            System.out.println("Execution Time: " + durationBF + " ms");

            PythonVisualize.animate_vectors_n_simulations();
        }

}
