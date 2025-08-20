import os
import numpy as np
from pathlib import Path

def get_simulation_directory(eta, v, d):
    """
    Devuelve la carpeta de simulación para los parámetros dados (eta, v, d).
    """
    root_dir = Path(__file__).resolve().parent.parent
    outputs_dir = root_dir / "outputs"

    folder_name = f"eta{eta}_v{v}_d{d}"
    sim_dir = outputs_dir / folder_name

    if not sim_dir.exists():
        raise FileNotFoundError(f"No se encontró la carpeta: {sim_dir}")

    print(f"Usando simulación: {sim_dir}")
    return sim_dir


def load_params(sim_dir):
    """Lee el archivo params.csv y devuelve un diccionario."""
    params_path = os.path.join(sim_dir, "params.csv")
    data = np.genfromtxt(params_path, delimiter=",", names=True)
    params = {name: float(data[name]) for name in data.dtype.names}
    return params


def load_steps(sim_dir):
    """Carga todos los archivos step_XXXXX.csv en una lista de arrays."""
    steps_dir = os.path.join(sim_dir, "steps")
    files = sorted(f for f in os.listdir(steps_dir) if f.startswith("step_") and f.endswith(".csv"))
    steps = []
    for fname in files:
        arr = np.genfromtxt(os.path.join(steps_dir, fname), delimiter=",", names=True)
        steps.append(arr)
    return steps