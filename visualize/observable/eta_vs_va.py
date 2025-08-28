import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def plot_bar_char(csv_path, out_path=None, eta_filter=None):
    """
    Grafica <v_a> vs eta con barras de error.
    Solo toma las filas cuyo eta esté en eta_filter (si no es None).
    """

    # Cargar datos
    data = np.genfromtxt(csv_path, delimiter=",", names=True)

    eta = data["eta"]
    va_mean = data["va_mean"]
    va_std = data["va_std"]

    # Filtrar si corresponde
    if eta_filter is not None:
        mask = np.isin(eta, eta_filter)
        eta = eta[mask]
        va_mean = va_mean[mask]
        va_std = va_std[mask]

    # Ordenar por eta
    order = np.argsort(eta)
    eta = eta[order]
    va_mean = va_mean[order]
    va_std = va_std[order]

    # Posiciones equiespaciadas en el eje X
    x_pos = np.arange(len(eta))
    
    # Graficar
    plt.figure(figsize=(8,5))
    bar_width = 0.5
    plt.bar(x_pos, va_mean, yerr=va_std, width=bar_width, capsize=5,
            color="#28769B", edgecolor="black", ecolor="#4ABEE8")

    plt.xlabel("η")
    plt.ylabel(r"Polarización promedio $<v_a>$")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Etiquetas arriba de cada barra
    for x, y in zip(x_pos, va_mean):
        plt.text(x, y + 0.02, f"{y:.3f}", ha="center", va="bottom", fontsize=9)

    # Etiquetas del eje X usando los valores de eta
    plt.xticks(x_pos, [f"{val:.2f}" for val in eta])

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {out_path}")


def plot_line_chart(csv_path, out_path=None, eta_filter=None, fixed_params=None):
    """
    Grafica <v_a> vs eta con líneas y barras de error.
    Solo toma las filas cuyo eta esté en eta_filter (si no es None).
    """

    data = np.genfromtxt(csv_path, delimiter=",", names=True)

    eta = data["eta"]
    va_mean = data["va_mean"]
    va_std = data["va_std"]

    # Máscara inicial: todos True
    mask = np.ones(len(eta), dtype=bool)

    # Filtrar por eta_filter
    if eta_filter is not None:
        mask &= np.isin(eta, eta_filter)

    # Filtrar por fixed_params
    if fixed_params is not None:
        for key, val in fixed_params.items():
            if key in data.dtype.names:   # solo si existe la columna
                mask &= (data[key] == val)

    # Aplicar filtro
    eta = eta[mask]
    va_mean = va_mean[mask]
    va_std = va_std[mask]

    # Ordenar por eta
    order = np.argsort(eta)
    eta = eta[order]
    va_mean = va_mean[order]
    va_std = va_std[order]

    # Graficar línea con barras de error
    plt.figure(figsize=(8,5))
    plt.errorbar(
        eta, va_mean, yerr=va_std, fmt='-o', capsize=5,
        color="#28769B", ecolor="#4ABEE8", elinewidth=1.2, markerfacecolor="white"
    )

    plt.xlabel("η")
    plt.ylabel(r"Polarización promedio $<v_a>$")
    plt.grid(True, linestyle="--", alpha=0.7)

    # Etiquetas encima de cada punto
    for x, y in zip(eta, va_mean):
        plt.text(x, y + 0.02, f"{y:.2f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {out_path}")

    

# ---------------------------

if __name__ == "__main__":
    outputs_dir = "input_vs_output"
    csv_path = os.path.join(outputs_dir, "input_vs_observable.csv")
    out_fig = os.path.join(outputs_dir, "eta_vs_va.png")

    # Parámetros fijos para filtrar
    fixed = {
    "L": 10.0,
    "v": 0.03,
    "N": 500.0,
    "r": 1.0,
    "steps": 1000,
    "save_every": 1.0
    }   

    # Filtrar solo ciertos valores de eta para mostrar el gráfico
    eta_filter = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]

    plot_line_chart(csv_path, out_path=out_fig, eta_filter=eta_filter, fixed_params=fixed)