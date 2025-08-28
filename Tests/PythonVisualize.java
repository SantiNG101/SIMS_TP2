package Tests;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class PythonVisualize {

    // Obtiene la raíz del proyecto de forma absoluta y normalizada
    final static String projectRoot;
    final static String pythonEnvironment;

    static {
        try {
            projectRoot = new File(".").getCanonicalPath(); // limpia . y .. automáticamente
            pythonEnvironment = Paths.get(projectRoot, "venv", "bin", "python").toString();
        } catch (IOException e) {
            throw new RuntimeException("Error obteniendo path del proyecto", e);
        }
    }

    /**
     * Genera animación llamando al script de Python
     *
     * @param simsDir carpeta de simulación relativa a projectRoot (ej: "outputs/eta0.1_v0.3_d12.5")
     * @param simName nombre de la simulación (ej: "sim_1756343233")
     */
    public static void animate_vectors(String simsParamsDir, Path simDir) throws IOException, InterruptedException {

        String script = Paths.get(projectRoot, "visualize", "animate_vectors.py").toString();
        ProcessBuilder pb = new ProcessBuilder(
                pythonEnvironment,
                script,
                simsParamsDir,
                simDir.getFileName().toString()
        );
        pb.inheritIO();  // para ver la salida de Python en la consola
        Process process = pb.start();
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            System.err.println("Error generando animación");
        }
    }

    public static void animate_vectors_n_simulations() throws IOException, InterruptedException {

        String script = Paths.get(projectRoot, "visualize", "animate_vectors.py").toString();
        ProcessBuilder pb = new ProcessBuilder(
                pythonEnvironment,
                script
        );
        pb.inheritIO();  // para ver la salida de Python en la consola
        Process process = pb.start();
        int exitCode = process.waitFor();
        if (exitCode != 0) {
            System.err.println("Error generando animación");
        }
    }
}
