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

public class SimulationMethodsComparisonTest {


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
    public void testBruteForceVsCIM() throws IOException {
        // mismo conjunto de parámetros para ambos

        String outDir = "outputs/comparison";
        Params p = new Params(0.1, 0.3, 20.0, 500, outDir);
        p.setSeed(20);

        String dirBrute = SimulationMain.runSimpleSimulation(p,true);
        String dirCIM = SimulationMain.runSimpleSimulation(p,false);


        Path lastBrute = getLastStepFile(dirCIM + "/steps");
        Path lastCIM = getLastStepFile(dirBrute + "/steps");

        List<String[]> bruteData = loadCsv(lastBrute);
        List<String[]> cimData = loadCsv(lastCIM);

        assertEquals(bruteData.size(), cimData.size(), "Distinto número de filas");

        for (int i = 0; i < bruteData.size(); i++) {
            String[] row1 = bruteData.get(i);
            String[] row2 = cimData.get(i);
            assertEquals(row1.length, row2.length, "Fila " + i + " tiene distinta cantidad de columnas");

            for (int j = 0; j < row1.length; j++) {
                double v1, v2;
                try {
                    v1 = Double.parseDouble(row1[j]);
                    v2 = Double.parseDouble(row2[j]);
                } catch (NumberFormatException e) {
                    continue; // probablemente cabecera
                }
                assertEquals(v1, v2, 1e-8, "Diferencia en fila " + i + ", columna " + j);
            }
        }
    }
}
