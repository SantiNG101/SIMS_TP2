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
                         scale_units='xy', scale=0.6, pivot='middle', width=0.01)
        cbar = fig.colorbar(quiv, ax=ax, shrink=0.7)
        cbar.set_label("Ángulo de la velocidad (rad)")
    else:
        quiv = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy', scale=0.6, pivot='middle', width=0.01)

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

    anim = animation.FuncAnimation(fig, update, frames=len(step_indices), interval=50, blit=False)
    anim.save(out_path, writer=PillowWriter(fps=20))
    plt.close(fig)


# ---------------------------

if __name__ == "__main__":

    sims_dir = get_simulation_directory(eta=1.0, v=0.03, d=2.5)
    sim_dir_name = "sim_1756327052"
    sim_subdir_list = list(sims_dir.glob("sims/" + sim_dir_name))
    if len(sim_subdir_list) == 0:
        raise FileNotFoundError(f"No se encontró la simulación {sim_dir_name}")
    sim_subdir = sim_subdir_list[0]

    params = load_params(sims_dir)
    L = params["L"]

    # Animaciones
    out_plain = os.path.join(sim_subdir, "anim_plain.gif")
    out_angle = os.path.join(sim_subdir, "anim_color_angle.gif")
    animate_vectors(sim_subdir, L, out_plain, color_by_angle=False)
    animate_vectors(sim_subdir, L, out_angle, color_by_angle=True)

    print(f"Animaciones guardadas en:\n{out_plain}\n{out_angle}")
