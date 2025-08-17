import numpy as np
import os
import matplotlib.pyplot as plt
from utils import get_simulation_directory

def compute_stationary_va(t, va, threshold, stable_steps):
    """
    Devuelve el primer paso estacionario y el promedio de v_a desde ahí hasta el final.

    Args:
        csv_path (str): Ruta al archivo polarization.csv
        threshold (float): Cambio máximo tolerable entre pasos para considerar estabilidad
        stable_steps (int): Cantidad de pasos consecutivos que tengan que cumplir el criterio
    """

    # Buscar el paso desde donde es estacionario
    count = 0
    stationary_index = 0
    for i in range(1, len(va)):
        if abs(va[i] - va[i-1]) < threshold:
            count += 1
            if count >= stable_steps:
                stationary_index = i - stable_steps + 1
                break
        else:
            count = 0

    va_mean = np.mean(va[stationary_index:])
    print(f"Estado estacionario desde paso: {stationary_index}")
    print(f"Promedio de v_a desde estado estacionario: {va_mean:.6f}")

    return stationary_index, va_mean


def plot_va_with_stationary(t, va, stationary_index, va_mean, threshold, stable_steps, sim_dir):
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
    
    text_str = (f"Threshold = {threshold}\n"
                f"Pasos estables = {stable_steps}\n"
                f"<v_a> = {va_mean:.4f}")
    
    plt.text(0.72, 0.1, text_str, transform=plt.gca().transAxes, bbox=dict(facecolor='white', edgecolor='violet'))
    
    out_path = os.path.join(sim_dir, "va_stationary.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {out_path}")


def plot_avg_va_with_stationary(t, va_mean, va_std, stationary_index, va_stationary_mean, threshold, stable_steps, out_dir):
    """Grafica v_a promedio con banda de error y marca el estado estacionario."""
    plt.figure(figsize=(8,5))

    plt.plot(t, va_mean, color='blue', label='Promedio v_a(t)')
    plt.fill_between(t, va_mean - va_std, va_mean + va_std, color='blue', alpha=0.3, label='Desvío estándar')

    plt.plot(t[stationary_index:], va_mean[stationary_index:], color='violet', linewidth=2, label='Estado estacionario')

    plt.xlabel("t")
    plt.ylabel("v_a(t)")
    plt.title("Evolución temporal promedio de v_a con estado estacionario")
    plt.grid(True)
    plt.legend()

    text_str = (f"Threshold = {threshold}\n"
                f"Pasos estables = {stable_steps}\n"
                f"<v_a> = {va_stationary_mean:.4f}")
    
    plt.text(0.72, 0.1, text_str, transform=plt.gca().transAxes,
             bbox=dict(facecolor='white', edgecolor='violet'))

    out_path = os.path.join(out_dir, "va_stationary_avg.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {out_path}")



# ---------------------------

if __name__ == "__main__":

    # Modificar estos parámetros según sea necesario
    sims_dir = get_simulation_directory(eta=0.1, v=0.3, d=1.25)

    threshold = 0.005
    stable_steps = 100

# ---------------- Parte 1: procesar cada simulación individual ------------------------
    for sim_subdir in sorted(sims_dir.glob("sims/sim_*")):
        csv_path = os.path.join(sim_subdir, "polarization.csv")

        data = np.genfromtxt(csv_path, delimiter=",", names=True)
        t = data["t"]
        va = data["v_a"]

        stationary_index, va_mean = compute_stationary_va(t, va, threshold, stable_steps)
        plot_va_with_stationary(t, va, stationary_index, va_mean, threshold, stable_steps, sim_subdir)

# ---------------- Parte 2: promedio de todas las simulaciones ------------------------
    avg_csv = os.path.join(sims_dir, "polarization_avg.csv")
    if not os.path.exists(avg_csv):
        raise FileNotFoundError(f"No existe polarization_avg.csv, generá primero el promedio.")

    data_avg = np.genfromtxt(avg_csv, delimiter=",", names=True)
    t = data_avg["t"]
    va_mean = data_avg["va_mean"]
    va_std = data_avg["va_std"]

    stationary_index, va_stationary_mean = compute_stationary_va(t, va_mean, threshold, stable_steps)
    plot_avg_va_with_stationary(t, va_mean, va_std, stationary_index, va_stationary_mean, threshold, stable_steps, sims_dir)