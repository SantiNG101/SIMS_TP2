import argparse
from pathlib import Path
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
from utils import load_params, load_steps, get_simulation_directory

def animate_vectors(sim_dir, L, out_path, color_by_angle=False):
    steps = load_steps(sim_dir)
    max_frames = 1000
    step_indices = np.linspace(0, len(steps)-1, min(len(steps), max_frames), dtype=int)
    steps_to_animate = [steps[i] for i in step_indices]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_aspect('equal', 'box')

    # Cargo primer frame
    data0 = steps_to_animate[0]
    x, y, vx, vy = data0["x"], data0["y"], data0["vx"], data0["vy"]

    if color_by_angle:
        ang = (np.arctan2(vy, vx) + 2*np.pi) % (2*np.pi)
        quiv = ax.quiver(x, y, vx, vy, ang, cmap="hsv", angles='xy',
                         scale_units='xy', scale=0.1, pivot='middle', width=0.01)
        cbar = fig.colorbar(quiv, ax=ax, shrink=0.7)
        cbar.set_label("Ángulo de la velocidad (rad)")
    else:
        quiv = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy',
                         scale=0.1, pivot='middle', width=0.01)

    ax.set_xlabel("x")
    ax.set_ylabel("y")

    def update(frame_idx):
        data = steps_to_animate[frame_idx]
        x, y, vx, vy = data["x"], data["y"], data["vx"], data["vy"]
        if color_by_angle:
            ang = (np.arctan2(vy, vx) + 2*np.pi) % (2*np.pi)
            quiv.set_UVC(vx, vy, ang)
        else:
            quiv.set_UVC(vx, vy)
        quiv.set_offsets(np.c_[x, y])
        ax.set_title(f"t={frame_idx}")
        return quiv,

    anim = animation.FuncAnimation(fig, update, frames=len(step_indices), interval=20, blit=False)
    anim.save(out_path, writer=PillowWriter(fps=50))
    plt.close(fig)


# ---------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar animación de simulación")
    parser.add_argument("sims_dir", type=str, help="Directorio sims (ej: outputs/eta0.1_v0.3_d12.5)")
    parser.add_argument("sim_name", type=str, help="Nombre de la simulación (ej: sim_1756343233)")

    args = parser.parse_args()

    sims_dir = Path(args.sims_dir).resolve()
    sim_subdir = sims_dir / "sims" / args.sim_name

    if not sim_subdir.exists():
        raise FileNotFoundError(f"No existe {sim_subdir}")

    params = load_params(sims_dir)
    L = params["L"]

    out_angle = os.path.join(sim_subdir, "anim_color_angle.gif")
    animate_vectors(sim_subdir, L, out_angle, color_by_angle=True)

    print(f"Animación guardada en:\n{out_angle}")
