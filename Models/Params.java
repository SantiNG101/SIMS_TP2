package Models;

import java.io.BufferedWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Locale;

public class Params {
    int N = 500;                // Número de partículas
    double L = 10.0;            // Tamaño del espacio cuadrado
    double v = 0.03;             // Velocidad constante
    double eta = 0.1;           // Intensidad del ruido angular (η)
    double r = 1;             // Radio de interacción
    int steps = 1000;            // Número total de pasos de la simulación
    int saveEvery = 1;          // Cada cuántos pasos se guarda el estado
    String outDir = "outputs";  // Directorio de salida
    int M = 5;                 // cantidad de celdas por fila/columna
    Integer seed = null;
    boolean FVM = false;

    public Params(Double eta, Double v, Double L, Integer N, String outDir) {
        if(N != null) this.N = N;
        if(L != null) this.L = L;
        if(v != null) this.v = v;
        if(eta != null) this.eta = eta;
        if(outDir != null) this.outDir = outDir;
    }

    public Params(Double eta, Double v, Double L, Integer N, String outDir, boolean FVM) {
        if(N != null) this.N = N;
        if(L != null) this.L = L;
        if(v != null) this.v = v;
        if(eta != null) this.eta = eta;
        if(outDir != null) this.outDir = outDir;
        this.FVM = FVM;
    }

    public void setSeed(int seed) { this.seed = seed; }

    public Integer getSeed() { return this.seed; }

    public void createCSVFile(){
        try (BufferedWriter bw = Files.newBufferedWriter(Paths.get(outDir).resolve("params.csv"))) {
            bw.write("N,L,rho,v,eta,r,steps,save_every\n");
            bw.write(String.format(Locale.US, "%d,%.3f,%.3f,%.3f,%.3f,%.3f,%d,%d\n", N, L, N / (L*L), v, eta, r, steps, saveEvery));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
