import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Simple HSV → RGB converter (no new libraries needed)
def hsv_to_rgb(h, s=1, v=1):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6
    if i == 0: r, g, b = v, t, p
    if i == 1: r, g, b = q, v, p
    if i == 2: r, g, b = p, v, t
    if i == 3: r, g, b = p, q, v
    if i == 4: r, g, b = t, p, v
    if i == 5: r, g, b = v, p, q
    return (r, g, b)

# Create figure
fig = plt.figure(figsize=(12, 6))

# --- GRID SPEC LAYOUT ---
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Bloch sphere 1
b1 = qt.Bloch()
b1.fig = fig
b1.axes = fig.add_subplot(gs[0, 0], projection='3d')
b1.frame = False
b1.scale = False

# *** CUSTOM TOP LABEL HERE ***
b1.zlabel = ['', '']   # top label, bottom label removed



# Bloch sphere 2
b2 = qt.Bloch()
b2.fig = fig
b2.axes = fig.add_subplot(gs[0, 1], projection='3d')
b2.frame = False
b2.scale = False

# *** CUSTOM TOP LABEL HERE ***
b2.zlabel = ['', '']   # top label, bottom label removed


# Draw spheres once
b1.make_sphere()
b2.make_sphere()

def remove_wireframe(b):
    for artist in list(b.axes.collections):
        if artist.__class__.__name__ == "Line3DCollection":
            artist.remove()

remove_wireframe(b1)
remove_wireframe(b2)

# Freeze axes
for ax in (b1.axes, b2.axes):
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.grid(False)

b1.render()
b2.render()

# --- TEXT ABOVE & BELOW SPHERES ---

# LEFT SPHERE
b1.axes.text2D(0.5, 1.05, "|00⟩", transform=b1.axes.transAxes,
               ha="center", va="bottom", fontsize=16, clip_on=False)

b1.axes.text2D(0.5, -0.12, "|01⟩", transform=b1.axes.transAxes,
               ha="center", va="top", fontsize=16, clip_on=False)

# RIGHT SPHERE
b2.axes.text2D(0.5, 1.05, "|00⟩", transform=b2.axes.transAxes,
               ha="center", va="bottom", fontsize=16, clip_on=False)

b2.axes.text2D(0.5, -0.12, "|01⟩", transform=b2.axes.transAxes,
               ha="center", va="top", fontsize=16, clip_on=False)


# Animation parameters
N = 200
STOP_K1 = int(0.7 * N)   # left sphere stops at 70%
STOP_K2 = int(0.4 * N)   # right sphere stops at 40%

# Dynamic artists for sphere 1
trail1_line, = b1.axes.plot([], [], [], color='red', linewidth=3)
dot1 = b1.axes.scatter([], [], [], color='red', s=60)
cover1_lines = []
trail1 = []

# Dynamic artists for sphere 2
trail2_line, = b2.axes.plot([], [], [], color='blue', linewidth=3)
dot2 = b2.axes.scatter([], [], [], color='blue', s=60)
cover2_lines = []
trail2 = []

# Gradient endpoints
orange = np.array([1.0, 0.5, 0.0])
purple = np.array([0.6, 0.0, 0.8])

for k in range(N):

    # --- LEFT SPHERE DOT MOTION (stops at 70%) ---
    if k <= STOP_K1:
        theta1 = 2 * np.pi * k / N
    else:
        theta1 = 2 * np.pi * 0.7

    x1 = np.cos(theta1)
    y1 = np.sin(theta1)
    z1 = 0

    if k <= STOP_K1:
        trail1.append([x1, y1, z1])

    t1 = np.array(trail1)

    # --- RIGHT SPHERE DOT MOTION (stops at 40%) ---
    if k <= STOP_K2:
        theta2 = 2 * np.pi * k / N
    else:
        theta2 = 2 * np.pi * 0.4

    # Right sphere moves in the SAME equatorial plane as the left sphere
    x2 = np.cos(theta2)
    y2 = np.sin(theta2)
    z2 = 0

    if k <= STOP_K2:
        trail2.append([x2, y2, z2])

    t2 = np.array(trail2)

    # --- LEFT SPHERE MAIN LINE ---
    trail1_line.set_data(t1[:,0], t1[:,1])
    trail1_line.set_3d_properties(t1[:,2])

    # --- RIGHT SPHERE MAIN LINE ---
    trail2_line.set_data(t2[:,0], t2[:,1])
    trail2_line.set_3d_properties(t2[:,2])

    # Remove old fading segments
    for line in cover1_lines: line.remove()
    for line in cover2_lines: line.remove()
    cover1_lines = []
    cover2_lines = []

    fade_steps = 20
    fade_length = 1

    # --- LEFT SPHERE FADING ---
    for i in range(fade_steps):
        cut = fade_length * (i + 1)
        t = i / fade_steps
        rgb = orange * (1 - t) + purple * t

        if len(t1) > cut:
            seg1 = t1[:-cut]
            line, = b1.axes.plot(seg1[:,0], seg1[:,1], seg1[:,2],
                                 color=rgb, linewidth=3)
            cover1_lines.append(line)

    # --- RIGHT SPHERE FADING ---
    for i in range(fade_steps):
        cut = fade_length * (i + 1)
        t = i / fade_steps
        rgb = orange * (1 - t) + purple * t

        if len(t2) > cut:
            seg2 = t2[:-cut]
            line, = b2.axes.plot(seg2[:,0], seg2[:,1], seg2[:,2],
                                 color=rgb, linewidth=3)
            cover2_lines.append(line)

    # Update dots
    dot1._offsets3d = ([x1], [y1], [z1])
    dot2._offsets3d = ([x2], [y2], [z2])

    plt.pause(0.05)

plt.show()
