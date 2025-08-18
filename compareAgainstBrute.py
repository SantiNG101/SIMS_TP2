import os
import numpy as np
from pathlib import Path

def load_last_step(sim_dir):
    """Carga el último archivo step_XXXXX.csv de la simulación."""
    files = sorted(
        (f for f in os.listdir(sim_dir) if f.startswith("step_") and f.endswith(".csv")),
        key=lambda name: int(name[5:-4])  # extrae el número después de "step_"
    )
    if not files:
        raise FileNotFoundError(f"No hay archivos step_*.csv en {sim_dir}")
    last_file = files[-1]
    arr = np.genfromtxt(os.path.join(sim_dir, last_file), delimiter=",", names=True)
    return last_file, arr

def compare_arrays(arr1, arr2, tol=1e-8):
    """Compara dos arrays estructurados."""
    if arr1.shape != arr2.shape:
        return [f"Dimensiones distintas {arr1.shape} vs {arr2.shape}"]

    diffs = []
    for col in arr1.dtype.names:
        if not np.allclose(arr1[col], arr2[col], atol=tol):
            diffs.append(f"Columna '{col}': valores difieren")
    return diffs

if __name__ == "__main__":
    root_dir = Path(__file__).resolve().parent
    outputs_dir = root_dir / "outputs"

    sim_dirs = sorted(
        (d for d in outputs_dir.glob("sim_*") if d.is_dir()),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    if len(sim_dirs) < 2:
        raise FileNotFoundError("Se necesitan al menos dos carpetas 'sim_*' en outputs/")

    sim1, sim2 = sim_dirs[:2]

    print(f"Comparando últimas simulaciones:\n1) {sim1.name}\n2) {sim2.name}")

    file1, arr1 = load_last_step(sim1)
    file2, arr2 = load_last_step(sim2)

    print(f"Últimos archivos:\n - {file1} en {sim1.name}\n - {file2} en {sim2.name}")

    diffs = compare_arrays(arr1, arr2)

    if not diffs:
        print("\n✅ Últimos archivos son idénticos")
    else:
        print("\n⚠️ Diferencias encontradas:")
        for d in diffs:
            print(" -", d)
