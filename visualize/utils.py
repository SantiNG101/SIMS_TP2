import os
import numpy as np
from pathlib import Path

def get_simulation_directory():
    """Busca la carpeta de simulación más reciente en outputs/."""
    root_dir = Path(__file__).resolve().parent.parent
    outputs_dir = root_dir / "outputs"

    sim_folders = list(outputs_dir.glob("sim_*"))
    if not sim_folders:
        raise FileNotFoundError("No se encontraron carpetas 'sim_*' en outputs/")

    sim_dir = max(sim_folders, key=lambda p: p.stat().st_mtime)
    print(f"Usando simulación: {sim_dir}")
    return sim_dir


def load_params(sim_dir):
    """Lee el archivo params.txt y devuelve un diccionario."""
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