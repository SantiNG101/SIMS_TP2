import os
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import io
from PIL import Image
import argparse
from pathlib import Path


from utils import load_steps, load_params, get_simulation_directory


def animate_vectors(sim_dir, L, out_path, color_by_angle=False):
    steps = load_steps(sim_dir)
    max_frames = 1000
    step_indices = np.linspace(0, len(steps)-1, min(len(steps), max_frames), dtype=int)
    steps_to_animate = [steps[i] for i in step_indices]

    if color_by_angle:
        norm = mpl.colors.Normalize(vmin=0, vmax=2*np.pi)
        sm = mpl.cm.ScalarMappable(cmap="hsv", norm=norm)
        sm.set_array([])
        fig_cbar, ax_cbar = plt.subplots(figsize=(0.3, 3))
        cbar = fig_cbar.colorbar(sm, cax=ax_cbar)
        cbar.set_label("Ángulo de la velocidad (rad)")
        buf = io.BytesIO()
        fig_cbar.savefig(buf, format="png", bbox_inches="tight", dpi=150)
        plt.close(fig_cbar)
        buf.seek(0)
        bar_img = Image.open(buf).convert("RGBA")

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    ax.set_aspect('equal', 'box')

    data0 = steps_to_animate[0]
    x, y, vx, vy = data0["x"], data0["y"], data0["vx"], data0["vy"]

    if color_by_angle:
        ang = (np.arctan2(vy, vx) + 2 * np.pi) % (2 * np.pi)
        quiv = ax.quiver(x, y, vx, vy, ang, cmap="hsv", norm=norm,
                         angles='xy', scale_units='xy', scale=0.14,
                         pivot='middle', width=0.01)
    else:
        quiv = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy',
                         scale=0.14, pivot='middle', width=0.01)

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

    frames = []
    for i in range(len(step_indices)):
        update(i)
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
        buf.seek(0)
        frame_img = Image.open(buf).convert("RGBA")

        if color_by_angle:
            frame_H = frame_img.height
            bar_W, bar_H = bar_img.size

            width_factor = 1
            height_factor = 0.6

            new_bar_H = int(frame_H * height_factor)
            new_bar_W = int(bar_W * (new_bar_H / bar_H) * width_factor)
            bar_resized = bar_img.resize((new_bar_W, new_bar_H))

            new_img = Image.new("RGBA", (frame_img.width + new_bar_W + 10, frame_H), (255, 255, 255, 255))
            new_img.paste(frame_img, (0, 0))
            y_offset = (frame_H - new_bar_H) // 2
            new_img.paste(bar_resized, (frame_img.width + 10, y_offset))
            frames.append(new_img)
        else:
            frames.append(frame_img)

    frames[0].save(out_path, save_all=True, append_images=frames[1:], duration=20, loop=0)
    plt.close(fig)


# ---------------------------

def animate_single_simulation():
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


# ---------------------------

if __name__ == "__main__":

    if len(sys.argv) > 1:
        animate_single_simulation()
        sys.exit(0)

    runs = [
        (0.0, 0.03, 5.0),  # (eta, v, d)
        (0.5, 0.03, 5.0),
        (1.0, 0.03, 5.0),
        (1.5, 0.03, 5.0),
        (2.0, 0.03, 5.0),
        (2.5, 0.03, 5.0),
        (3.0, 0.03, 5.0),
        (4.0, 0.03, 5.0),
        (5.0, 0.03, 5.0),

        
            ]
    
    # ---------------- Parte 1: procesar cada simulación individual ------------------------

    for eta, v, d in runs:

        sims_dir = get_simulation_directory(eta, v, d)
        params = load_params(sims_dir)

        for sim_subdir in sorted(sims_dir.glob("sims/sim_*")):
            if "sim_plus_" in sim_subdir.name:
                continue

            params = load_params(sims_dir)
            L = params["L"]

            # Animaciones
            out_angle = os.path.join(sim_subdir, "anim_color_angle.gif")
            animate_vectors(sim_subdir, L, out_angle, color_by_angle=True)

            print(f"Animaciones guardadas en:\n{out_angle}")


