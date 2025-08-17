import numpy as np
import os
import matplotlib.pyplot as plt
from utils import load_params, load_steps, get_simulation_directory

# Calcula la polarización v_a(t) y la guarda su evolución temporal en polarization.csv
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

# ---------------------------

if __name__ == "__main__":
    sim_dir = get_simulation_directory()
    params = load_params(sim_dir)

    # Calculamos la polarización
    t_list, va_list = compute_polarization(sim_dir, params)

    # Guardamos el CSV
    out_csv = os.path.join(sim_dir, "polarization.csv")
    np.savetxt(out_csv, np.column_stack((t_list, va_list)), delimiter=",", header="t,v_a", comments="", fmt="%.6f")
    print(f"CSV guardado en: {out_csv}")

    # Graficamos la polarización en el tiempo
    out_fig = os.path.join(sim_dir, "va.png")
    plot_polarization(t_list, va_list, out_fig)

