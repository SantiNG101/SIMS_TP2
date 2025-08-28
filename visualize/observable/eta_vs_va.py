import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from adjustText import adjust_text

def plot_line_chart(csv_path, out_path=None, eta_filter=None, fixed_params=None):
    """
    Grafica <v_a> vs eta con líneas y barras de error.
    Promedia múltiples simulaciones para cada valor de eta.
    """

    # Cargar datos con pandas para mejor manipulación
    data = pd.read_csv(csv_path)
    
    # Aplicar filtros de parámetros fijos
    if fixed_params is not None:
        for key, val in fixed_params.items():
            if key in data.columns:
                data = data[np.isclose(data[key], val)]
    
    # Filtrar por eta si se especifica
    if eta_filter is not None:
        data = data[data['eta'].isin(eta_filter)]
    
    # Agrupar por eta y calcular promedio y desviación estándar
    grouped = data.groupby('eta').agg({
        'va_mean': ['mean', 'std'],
        'va_std': 'mean'
    }).reset_index()
    
    # Aplanar columnas multi-index
    grouped.columns = ['eta', 'va_mean', 'va_std_mean', 'va_std_avg']
    
    # Ordenar por eta
    grouped = grouped.sort_values('eta')
    
    eta = grouped['eta'].values
    va_mean = grouped['va_mean'].values
    va_std = grouped['va_std_mean'].values
    
    print("Datos procesados:")
    for i, (e, mean, std) in enumerate(zip(eta, va_mean, va_std)):
        print(f"η={e:.3f}: {mean:.3f} ± {std:.3f}")

    # Graficar línea con barras de error
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.errorbar(
        eta, va_mean, yerr=va_std, fmt='-o', capsize=5, linewidth=2, markersize=8,
        color="#28769B", ecolor="#4ABEE8", elinewidth=1.5, 
        markerfacecolor="white", markeredgewidth=2
    )

    ax.set_xlabel("η", fontsize=12)
    ax.set_ylabel(r"Polarización promedio $<v_a>$", fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.7)
    
    # Ajustar límites del eje Y para mejor visualización
    ax.set_ylim(0, 1.1)
    
    # Crear etiquetas sin fondo
    texts = []
    for x, y in zip(eta, va_mean):
        texts.append(ax.text(x, y + 0.02, f"{y:.3f}", 
                             ha='center', va='bottom', fontsize=9))
    
    # Ajustar posiciones automáticamente
    adjust_text(texts, ax=ax, only_move={'points':'y', 'text':'y'})

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Gráfico guardado en: {out_path}")

# ---------------------------

if __name__ == "__main__":
    # Crear directorio si no existe
    outputs_dir = "input_vs_output"
    os.makedirs(outputs_dir, exist_ok=True)
    
    csv_path = os.path.join(outputs_dir, "input_vs_observable.csv")
    out_fig = os.path.join(outputs_dir, "eta_vs_va.png")

    # Parámetros fijos para filtrar
    fixed = {
        "L": 10.0,
        "v": 0.03,
        "N": 500.0,
        "r": 1.0,
        "steps": 2000.0,
        "save_every": 1.0,
        "rho": 5.0
    }   

    # Valores de eta que queremos incluir
    eta_filter = [0.0, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0]

    plot_line_chart(csv_path, out_path=out_fig, eta_filter=eta_filter, fixed_params=fixed)
