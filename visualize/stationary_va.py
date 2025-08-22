import numpy as np
import os
import matplotlib.pyplot as plt
from utils import get_simulation_directory
import csv

from utils import load_params

def compute_stationary_va(t, va, stationary_first_step, sims_dir):
    """
    Devuelve el promedio y desvío estándar de v_a desde el primer paso estacionario hasta el final.
    Además guarda los resultados junto con los parámetros en outputs/input_vs_observable.csv
    """

    va_mean = np.mean(va[stationary_first_step:])
    va_std = np.std(va[stationary_first_step:], ddof=0)  # poblacional

    # Leer parámetros desde params.csv
    params = load_params(sims_dir)

    # Archivo de salida global
    root_dir = sims_dir.parent  # sube un nivel, ej: outputs/eta0.1_v0.3_d1.25
    out_csv = root_dir.parent / "outputs" / "input_vs_observable.csv"

    # Armar fila con parámetros + observables
    row = {**params, "va_mean": va_mean, "va_std": va_std}

    # Escribir/append al CSV
    write_header = not os.path.exists(out_csv)
    with open(out_csv, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"Promedio de v_a en estado estacionario: {va_mean:.6f}")
    print(f"Desvío estándar de v_a en estado estacionario: {va_std:.6f}")
    print(f"Resultado guardado en: {out_csv}")

    return va_mean, va_std


def plot_va_with_stationary(t, va, stationary_index, va_mean, sim_dir):
    """Grafica v_a en el tiempo y marca el estado estacionario."""
    plt.figure(figsize=(8,5))
    
    # v_a completa
    plt.plot(t, va, color='blue', label='v_a(t)')
    
    # v_a en estado estacionario resaltada
    plt.plot(t[stationary_index:], va[stationary_index:], color='violet', marker='o', linestyle='None', label='Estado estacionario')

    plt.xlabel("t")
    plt.ylabel("v_a(t)")
    plt.title(f"Evolución temporal de v_a con estado estacionario")
    plt.grid(True)
    plt.legend()
        
    out_path = os.path.join(sim_dir, "va_stationary.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {out_path}")


# ---------------------------

if __name__ == "__main__":

    # Modificar estos parámetros según sea necesario
    sims_dir = get_simulation_directory(eta=0.1, v=0.3, d=1.25)

# ---------------- Parte 1: procesar cada simulación individual ------------------------

    sim_dir_name = "sim_1755875186"
    sim_subdir = sims_dir / "sims" / sim_dir_name

    if not sim_subdir.exists():
        raise FileNotFoundError(f"No se encontró la simulación {sim_dir_name}")

    csv_path = sim_subdir / "polarization.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"No se encontró polarization.csv en {sim_subdir}")

    # Leer CSV con columnas t, v_a
    data = np.genfromtxt(csv_path, delimiter=",", names=True)
    t = data["t"]
    va = data["v_a"]

    stationary_index = 1000 
    va_mean, va_std = compute_stationary_va(t, va, stationary_index, sims_dir)

    plot_va_with_stationary(t, va, stationary_index, va_mean, sim_subdir)   