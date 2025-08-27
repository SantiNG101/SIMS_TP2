package Tests;

import java.io.IOException;
import java.nio.file.Path;

import org.junit.jupiter.api.Test;
import Models.Params;
import Models.SimulationMain;

import static org.junit.jupiter.api.Assertions.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class OneRandomNeighborTest {


    private static Path getLastStepFile(String dir) throws IOException {
        try (Stream<Path> files = Files.list(Paths.get(dir))) {
            return files
                    .filter(f -> f.getFileName().toString().startsWith("step_")
                            && f.getFileName().toString().endsWith(".csv"))
                    .max(Comparator.comparingInt(f -> {
                        String name = f.getFileName().toString();
                        String num = name.substring(5, name.length() - 4); // entre "step_" y ".csv"
                        return Integer.parseInt(num);
                    }))
                    .orElseThrow(() -> new IOException("No step_*.csv files found in " + dir));
        }
    }

    private List<String[]> loadCsv(Path file) throws IOException {
        try (BufferedReader br = Files.newBufferedReader(file)) {
            return br.lines()
                    .map(line -> line.split(","))
                    .collect(Collectors.toList());
        }
    }

    @Test
    public void test() throws IOException {
        // mismo conjunto de parámetros para ambos
        Double eta = 0.1, v= 0.3, l=20.0;
        int n = 5000;
        String outDir = "outputs/eta" + eta + "_v" + v + "_d" + n/(l*l);
        Params p = new Params(eta, v, l, n, outDir);
        p.setSeed(20);

        SimulationMain.runSimpleSimulationUsingOneRandomNeighbor(p);

    }
}


