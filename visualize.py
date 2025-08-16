import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
from pathlib import Path


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


def animate_vectors(sim_dir, L, out_path, color_by_angle=False):
    steps = load_steps(sim_dir)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_aspect('equal', 'box')
    ax.set_title("Off-Lattice simulation" + (" (color por ángulo)" if color_by_angle else ""))

    # Cargo primer frame
    data0 = steps[0]
    x, y, vx, vy = data0["x"], data0["y"], data0["vx"], data0["vy"]

    if color_by_angle:
        ang = (np.arctan2(vy, vx) + 2*np.pi) % (2*np.pi)
        quiv = ax.quiver(x, y, vx, vy, ang, cmap="hsv", angles='xy',
                         scale_units='xy', scale=1, pivot='middle')
        cbar = fig.colorbar(quiv, ax=ax)
        cbar.set_label("Ángulo de la velocidad (rad)")
    else:
        quiv = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy', scale=1, pivot='middle')

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    def update(frame_idx):
        data = steps[frame_idx]
        x, y, vx, vy = data["x"], data["y"], data["vx"], data["vy"]
        if color_by_angle:
            ang = (np.arctan2(vy, vx) + 2*np.pi) % (2*np.pi)
            quiv.set_UVC(vx, vy, ang)
        else:
            quiv.set_UVC(vx, vy)
        quiv.set_offsets(np.c_[x, y])
        ax.set_title(f"Off-Lattice simulation{' (color por ángulo)' if color_by_angle else ''} | t={frame_idx}")
        return quiv,

    anim = animation.FuncAnimation(fig, update, frames=len(steps), interval=50, blit=False)
    anim.save(out_path, writer=PillowWriter(fps=20))
    plt.close(fig)


# ---------------------------

if __name__ == "__main__":

    root_dir = Path(__file__).resolve().parent
    outputs_dir = root_dir / "outputs"

    print(f"Buscando en: {outputs_dir.resolve()}")
    print("Contenido:", list(outputs_dir.glob("*")))

    sim_folders = list(outputs_dir.glob("sim_*"))
    if not sim_folders:
        raise FileNotFoundError("No se encontraron carpetas 'sim_*' en outputs/")

    sim_dir = max(sim_folders, key=lambda p: p.stat().st_mtime)
    print(f"Usando simulación: {sim_dir}")
    params = load_params(sim_dir)
    L = params["L"]

    # Animaciones
    out_plain = os.path.join(sim_dir, "anim_plain.gif")
    out_angle = os.path.join(sim_dir, "anim_color_angle.gif")
    animate_vectors(sim_dir, L, out_plain, color_by_angle=False)
    animate_vectors(sim_dir, L, out_angle, color_by_angle=True)

    print(f"Animaciones guardadas en:\n{out_plain}\n{out_angle}")
