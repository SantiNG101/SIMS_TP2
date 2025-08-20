package Tests;

import java.io.IOException;
import java.nio.file.Path;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

        import java.io.*;
        import java.nio.file.*;
        import java.util.*;
        import java.util.stream.Collectors;

public class SimulationMethodsComparisonTest {

    private Path runSimulation(String mode, Params p) throws IOException {
        Simulation sim = new Simulation(p);
        if (mode.equals("brute")) {
            sim.runBruteForce();
        } else if (mode.equals("cim")) {
            sim.runCIM();
        } else {
            throw new IllegalArgumentException("Modo desconocido: " + mode);
        }
        return sim.getSimDir();
    }

    private Path getLastStepFile(Path simDir) throws IOException {
        try (var files = Files.list(simDir)) {
            return files
                    .filter(f -> f.getFileName().toString().startsWith("step_"))
                    .sorted(Comparator.comparingInt(f -> {
                        String name = f.getFileName().toString();
                        return Integer.parseInt(name.substring(5, name.length() - 4)); // step_XXXXX.csv
                    }))
                    .reduce((first, second) -> second) // último
                    .orElseThrow(() -> new FileNotFoundException("No step_*.csv en " + simDir));
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
        Params p1 = new Params(0.1, 0.3, 20.0, 500, "outputs/sim_brute");
        Params p2 = new Params(0.1, 0.3, 20.0, 500, "outputs/sim_cim");

        Path dirBrute = runSimulation("brute", p1);
        Path dirCIM = runSimulation("cim", p2);

        Path lastBrute = getLastStepFile(dirBrute);
        Path lastCIM = getLastStepFile(dirCIM);

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
{
}
