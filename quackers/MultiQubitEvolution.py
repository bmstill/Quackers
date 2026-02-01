import numpy as np
import qutip as qt
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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

fig = plt.figure(figsize=(14, 5))
gs = gridspec.GridSpec(1, 3, width_ratios=[1, 1, 0.35])

# LEFT BLOCH SPHERE
b1 = qt.Bloch()
b1.fig = fig
b1.axes = fig.add_subplot(gs[0, 0], projection='3d')
b1.frame = False
b1.scale = False
# remove default |0>, |1> axis labels so only text2D is used
b1.zlabel = ['', '']

# RIGHT BLOCH SPHERE
b2 = qt.Bloch()
b2.fig = fig
b2.axes = fig.add_subplot(gs[0, 1], projection='3d')
b2.frame = False
b2.scale = False
b2.zlabel = ['', '']

# PHASE BAR
rect_ax = fig.add_subplot(gs[0, 2])
rect_ax.set_xticks([])
rect_ax.set_yticks([])
rect_ax.set_title("Phase of |11⟩", fontsize=16, pad=12, color='black')

width_px = 300
height_px = 300
gradient = np.zeros((height_px, width_px, 3))
red = np.array([1.0, 0.0, 0.0])
blue = np.array([0.0, 0.0, 1.0])

for j in range(height_px):
    tt = j / height_px
    rgb = red * (1 - tt) + blue * tt
    gradient[j, :, :] = rgb

rect_ax.imshow(gradient, aspect='auto')
rect_ax.set_xlim(0, width_px)
rect_ax.set_ylim(height_px, 0)

# overlay text axis for labels on the phase bar
text_ax = fig.add_subplot(gs[0, 2])
text_ax.set_xticks([])
text_ax.set_yticks([])
text_ax.set_facecolor("none")

text_ax.text(1.05, 0.98, "3π", fontsize=16, va='top', ha='left', color='black')
text_ax.text(1.05, 0.66, "2π", fontsize=16, va='center', ha='left', color='black')
text_ax.text(1.05, 0.34, "π", fontsize=16, va='center', ha='left', color='black')
text_ax.text(1.05, 0.02, "0", fontsize=16, va='bottom', ha='left', color='black')

text_ax.set_xlim(0, 1)
text_ax.set_ylim(0, 1)

# draw Bloch spheres
b1.make_sphere()
b2.make_sphere()

def remove_wireframe(b):
    for artist in list(b.axes.collections):
        if artist.__class__.__name__ == "Line3DCollection":
            artist.remove()

remove_wireframe(b1)
remove_wireframe(b2)

for ax in (b1.axes, b2.axes):
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.grid(False)

b1.render()
b2.render()

# make room above and below for labels
plt.subplots_adjust(top=0.9, bottom=0.2)

# TEXT ABOVE & BELOW LEFT SPHERE
b1.axes.text2D(0.5, 1.05, "|00⟩", transform=b1.axes.transAxes,
               ha="center", va="bottom", fontsize=16, clip_on=False, zorder=10)
b1.axes.text2D(0.5, -0.12, "|01⟩", transform=b1.axes.transAxes,
               ha="center", va="top", fontsize=16, clip_on=False, zorder=10)

# TEXT ABOVE & BELOW RIGHT SPHERE
b2.axes.text2D(0.5, 1.05, "|00⟩", transform=b2.axes.transAxes,
               ha="center", va="bottom", fontsize=16, clip_on=False, zorder=10)
b2.axes.text2D(0.5, -0.12, "|01⟩", transform=b2.axes.transAxes,
               ha="center", va="top", fontsize=16, clip_on=False, zorder=10)

# TRAILS & DOTS
trail1_line, = b1.axes.plot([], [], [], color='red', linewidth=3)
trail2_line, = b2.axes.plot([], [], [], color='blue', linewidth=3)

dot1 = b1.axes.scatter([], [], [], color='red', s=60)
dot2 = b2.axes.scatter([], [], [], color='blue', s=60)

cover1_lines = []
cover2_lines = []

N = 200
trail1 = []
trail2 = []

orange = np.array([1.0, 0.5, 0.0])
purple = np.array([0.6, 0.0, 0.8])

# RIGHT-SPHERE heart path
t = np.linspace(0, 2*np.pi, N, endpoint=False)
hx = 16 * np.sin(t)**3
hy = 13*np.cos(t) - 5*np.cos(2*t) - 2*np.cos(3*t) - np.cos(4*t)

hx = hx / np.max(np.abs(hx))
hy = (hy - np.min(hy)) / (np.max(hy) - np.min(hy))

start_idx = np.argmin(hy)
hx = np.roll(hx, -start_idx)
hy = np.roll(hy, -start_idx)

width = 1.25
height = 1.05
phi0 = (np.pi / 4) + (2*np.pi/3)

phi_heart = phi0 + width * hx
theta_heart = np.pi - height * hy

def sample_loop(arr, u):
    s = (u / (2*np.pi)) * N
    i0 = int(np.floor(s)) % N
    i1 = (i0 + 1) % N
    frac = s - np.floor(s)
    return (1 - frac) * arr[i0] + frac * arr[i1]

speed_right = 1.5

# PHASE BAR DOTS
x_bar_left = width_px * 0.35
x_bar_right = width_px * 0.65

bar_dot_left = rect_ax.scatter([x_bar_left], [height_px], s=90,
                               color='red', edgecolors='black', linewidths=1.0, zorder=10)
bar_dot_right = rect_ax.scatter([x_bar_right], [height_px], s=90,
                                color='blue', edgecolors='black', linewidths=1.0, zorder=10)

def phase_to_y(phase):
    phase = np.clip(phase, 0.0, 3*np.pi)
    return height_px * (1.0 - phase / (3*np.pi))

dot1._offsets3d = ([0], [0], [-1])
dot2._offsets3d = ([0], [0], [-1])
plt.pause(0.5)

for k in range(N):
    lam = 2 * np.pi * k / N

    # LEFT-SPHERE path
    theta_min = 0.55
    p1 = 3.2
    theta_sph1 = np.pi - (np.sin(lam / 2))**p1 * (np.pi - theta_min)
    phi0_1 = -np.pi / 2
    Aphi1 = 0.65
    phi_sph1 = phi0_1 + Aphi1 * np.sin(lam)
    x1 = np.sin(theta_sph1) * np.cos(phi_sph1)
    y1 = np.sin(theta_sph1) * np.sin(phi_sph1)
    z1 = np.cos(theta_sph1)

    # RIGHT-SPHERE heart
    u = speed_right * lam
    if u > 2*np.pi:
        u = 2*np.pi

    theta_sph2 = sample_loop(theta_heart, u)
    phi_sph2 = sample_loop(phi_heart, u)
    x2 = np.sin(theta_sph2) * np.cos(phi_sph2)
    y2 = np.sin(theta_sph2) * np.sin(phi_sph2)
    z2 = np.cos(theta_sph2)

    trail1.append([x1, y1, z1])
    trail2.append([x2, y2, z2])

    t1 = np.array(trail1)
    t2 = np.array(trail2)

    trail1_line.set_data(t1[:, 0], t1[:, 1])
    trail1_line.set_3d_properties(t1[:, 2])

    trail2_line.set_data(t2[:, 0], t2[:, 1])
    trail2_line.set_3d_properties(t2[:, 2])

    for line in cover1_lines:
        line.remove()
    for line in cover2_lines:
        line.remove()
    cover1_lines = []
    cover2_lines = []

    fade_steps = 20
    fade_length = 1

    for i in range(fade_steps):
        cut = fade_length * (i + 1)
        tt = i / fade_steps
        rgb = orange * (1 - tt) + purple * tt

        if len(t1) > cut:
            seg1 = t1[:-cut]
            line, = b1.axes.plot(seg1[:, 0], seg1[:, 1], seg1[:, 2],
                                 color=rgb, linewidth=3)
            cover1_lines.append(line)

        if len(t2) > cut:
            seg2 = t2[:-cut]
            line, = b2.axes.plot(seg2[:, 0], seg2[:, 1], seg2[:, 2],
                                 color=rgb, linewidth=3)
            cover2_lines.append(line)

    dot1._offsets3d = ([x1], [y1], [z1])
    dot2._offsets3d = ([x2], [y2], [z2])

    progress_left = k / (N - 1)
    phase_left = 2*np.pi * progress_left

    progress_right = u / (2*np.pi)
    phase_right = 3*np.pi * progress_right

    y_left = phase_to_y(phase_left)
    y_right = phase_to_y(phase_right)

    bar_dot_left.set_offsets([[x_bar_left, y_left]])
    bar_dot_right.set_offsets([[x_bar_right, y_right]])

    plt.pause(0.05)

plt.show()
