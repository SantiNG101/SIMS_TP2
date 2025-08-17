import numpy as np
import os
import matplotlib.pyplot as plt
from utils import load_params, load_steps, get_simulation_directory

# Calcula la polarización v_a(t)
def compute_polarization(sim_dir, params):
    N = int(params['N'])
    v = params['v']
    save_every = params.get('save_every', 1)

    # Cargar pasos
    steps = load_steps(sim_dir)

    v_a_list = []
    for step in steps:
        sum_vx = np.sum(step['vx'])
        sum_vy = np.sum(step['vy'])
        sum_velocity_magnitude = np.sqrt(sum_vx**2 + sum_vy**2)
        v_a = sum_velocity_magnitude / (N * v)
        v_a_list.append(v_a)

    time_list = np.arange(len(v_a_list)) * save_every
    return time_list, np.array(v_a_list)


# Grafica la polarización v_a(t)
def plot_polarization(time_list, v_a_list, out_path):
    plt.figure(figsize=(8,5))
    plt.plot(time_list, v_a_list, color='blue', label='v_a(t)')
    plt.xlabel("t")
    plt.ylabel("v_a(t)")
    plt.title("Evolución temporal de v_a")
    plt.grid(True)
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"Gráfico guardado en: {out_path}")


# Calcula y grafica el promedio de v_a(t) a partir de múltiples simulaciones
def plot_average_polarization(out_dir):
    
    sims_path = os.path.join(out_dir, "sims")
    sim_dirs = sorted([os.path.join(sims_path, d) for d in os.listdir(sims_path) if d.startswith("sim_")])
    if not sim_dirs:
        raise FileNotFoundError(f"No se encontraron simulaciones en {sims_path}")

    all_va = []
    time_list = None

    for sim_dir in sim_dirs:
        csv_path = os.path.join(sim_dir, "polarization.csv")

        data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
        t, va = data[:,0], data[:,1]

        if time_list is None:
            time_list = t
        all_va.append(va)

    all_va = np.array(all_va)

    va_mean = np.mean(all_va, axis=0)
    va_std = np.std(all_va, axis=0)

    # Graficar
    plt.figure(figsize=(8,5))
    plt.plot(time_list, va_mean, color="blue", label="Promedio v_a(t)")
    plt.fill_between(time_list, va_mean - va_std, va_mean + va_std, color="blue", alpha=0.3, label="Desvío estándar")
    plt.xlabel("t")
    plt.ylabel("v_a(t)")
    plt.title("Promedio de v_a(t) con error")
    plt.legend()
    plt.grid(True)

    out_path = os.path.join(out_dir, "va_avg.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"✅ Gráfico promedio guardado en: {out_path}")

    # Guardar CSV con promedio y desvío estándar
    out_csv = os.path.join(out_dir, "polarization_avg.csv")
    np.savetxt(out_csv, np.column_stack((time_list, va_mean, va_std)),
               delimiter=",", header="t,va_mean,va_std", comments="", fmt="%.6f")
    print(f"✅ CSV promedio guardado en: {out_csv}")


# ---------------------------


if __name__ == "__main__":

    # Modificar estos parámetros según sea necesario
    sims_dir = get_simulation_directory(eta=0.1, v=0.3, d=1.25)
    params = load_params(sims_dir)


# ---------------- Parte 1: procesar cada simulación individual ------------------------
    for sim_subdir in sorted(sims_dir.glob("sims/sim_*")):

        # Calculamos la polarización
        t_list, va_list = compute_polarization(sim_subdir, params)

        # Guardamos el CSV
        out_csv = os.path.join(sim_subdir, "polarization.csv")
        np.savetxt(out_csv, np.column_stack((t_list, va_list)), delimiter=",", header="t,v_a", comments="", fmt="%.6f")
        print(f"CSV guardado en: {out_csv}")

        # Graficamos la polarización en el tiempo
        # out_fig = os.path.join(sim_subdir, "va.png")
        # plot_polarization(t_list, va_list, out_fig)

# ---------------- Parte 2: promedio de todas las simulaciones ------------------------
    plot_average_polarization(sims_dir)