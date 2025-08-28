import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def plot_line_chart(csv_path, out_path=None, N_filter=None, fixed_params=None):
    """
    Grafica <v_a> vs rho con líneas y barras de error.
    El eje x muestra la densidad y también L debajo.
    """

    data = np.genfromtxt(csv_path, delimiter=",", names=True)

    N = data["N"]
    rho = data["rho"]
    va_mean = data["va_mean"]
    va_std = data["va_std"]

    mask = np.ones(len(N), dtype=bool)

    # Filtrar por L_filter
    if N_filter is not None:
        mask &= np.isin(N, N_filter)

    # Filtrar por fixed_params
    if fixed_params is not None:
        for key, val in fixed_params.items():
            if key in data.dtype.names:   # solo si existe la columna
                mask &= (data[key] == val)

    # Aplicar filtro
    N = N[mask]
    rho = rho[mask]
    va_mean = va_mean[mask]
    va_std = va_std[mask]

    # Ordenar por rho
    order = np.argsort(rho)
    N = N[order]
    rho = rho[order]
    va_mean = va_mean[order]
    va_std = va_std[order]

    x_pos = np.log10(rho)

    plt.figure(figsize=(8,5))
    plt.errorbar(
        x_pos, va_mean, yerr=va_std, fmt='-o', capsize=5,
        color="#28769B", ecolor="#4ABEE8", elinewidth=1.2, markerfacecolor="white"
    )

    plt.xlabel(r"Densidad $\rho$")
    plt.ylabel(r"Polarización promedio $<v_a>$")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.ylim(0, 1.05)

    tick_labels = [f"{r:.2f}\nN={int(l)}" for r, l in zip(rho, N)]
    plt.xticks(x_pos, tick_labels)

    for x, y in zip(x_pos, va_mean):
        plt.text(x, y + 0.02, f"{y:.2f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {out_path}")
    

# ---------------------------

if __name__ == "__main__":
    outputs_dir = "input_vs_output"
    csv_path = os.path.join(outputs_dir, "input_vs_observable.csv")
    out_fig = os.path.join(outputs_dir, "N_vs_va.png")

    # Parámetros fijos para filtrar
    fixed = {
    "eta": 0.5,
    "v": 0.03,
    "L": 10.0,
    "r": 1.0,
    "save_every": 1.0
    }   

    # Filtrar solo ciertos valores de eta para mostrar el gráfico
    N_filter = [5, 20, 55, 125, 222, 500, 2000]

    plot_line_chart(csv_path, out_path=out_fig, N_filter=N_filter, fixed_params=fixed)