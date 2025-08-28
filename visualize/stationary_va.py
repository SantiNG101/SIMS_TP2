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
    outputs_dir = "input_vs_output"
    out_csv = os.path.join(outputs_dir, "input_vs_observable.csv")

    # Armar fila con parámetros + observables
    row = {**params, "va_mean": va_mean, "va_std": va_std}

    # Escribir/append al CSV
    write_header = not os.path.exists(out_csv)
    with open(out_csv, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"Resultado guardado en: {out_csv}")

    return va_mean, va_std


def plot_va_with_stationary(t, va, stationary_index, va_mean, sim_dir):
    """Grafica v_a en el tiempo y marca el estado estacionario."""
    plt.figure(figsize=(8,5))
    
    # v_a completa
    plt.plot(t, va, color='blue', label=r'$v_a(t)$')
    
    # v_a en estado estacionario resaltada
    plt.plot(t[stationary_index:], va[stationary_index:], color='violet', linewidth=2, label='Estado estacionario')

    plt.xlabel("t")
    plt.ylabel(r"$v_a(t)$")
    plt.ylim(0, 1.05)
    plt.grid(True)
    plt.legend()
    plt.ylim(0, 1.05)
        
    out_path = os.path.join(sim_dir, "va_stationary.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {out_path}")


# ---------------------------

if __name__ == "__main__":

    # Definir los parámetros de las simulaciones a procesar
    # (eta, v, d, stationary_index)
    runs = [
        (0.0, 0.03, 5.0, 1250),
        (0.025, 0.03, 5.0, 800),
        (0.05, 0.03, 5.0,1250),
        (0.1, 0.03, 5.0,900),
        (0.25, 0.03, 5.0,500),
        (0.5, 0.03, 5.0,250),
        (1.0, 0.03, 5.0,100),
        (2.0, 0.03, 5.0,100)
    ]

    for eta, v, d, stationary_index in runs:

        sims_dir = get_simulation_directory(eta, v, d)

        sim_subdirs = list((sims_dir / "sims").glob("sim_*"))
        for sim_subdir in sim_subdirs:
            csv_path = sim_subdir / "polarization.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"No se encontró polarization.csv en {sim_subdir}")

            # Leer CSV con columnas t, v_a
            data = np.genfromtxt(csv_path, delimiter=",", names=True)
            t = data["t"]
            va = data["v_a"]

            va_mean, va_std = compute_stationary_va(t, va, stationary_index, sims_dir)

            plot_va_with_stationary(t, va, stationary_index, va_mean, sim_subdir)   