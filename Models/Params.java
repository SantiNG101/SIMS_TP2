package Models;

public class Params {
    int N = 500;                // Número de partículas
    double L = 40.0;            // Tamaño del espacio cuadrado
    double v = 0.3;             // Velocidad constante
    double eta = 0.1;           // Intensidad del ruido angular (η)
    double r = 1;             // Radio de interacción
    int steps = 1000;            // Número total de pasos de la simulación
    int saveEvery = 1;          // Cada cuántos pasos se guarda el estado
    String outDir = "outputs";  // Directorio de salida
    int M = 12;                 // cantidad de celdas por fila/columna
    Integer seed = null;

    public Params(Double eta, Double v, Double L, Integer N, String outDir) {
        if(N != null) this.N = N;
        if(L != null) this.L = L;
        if(v != null) this.v = v;
        if(eta != null) this.eta = eta;
        if(outDir != null) this.outDir = outDir;
    }
    
    public void setSeed(int seed) { this.seed = seed; }

    public Integer getSeed() { return this.seed; }
}
