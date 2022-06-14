# Fractal tree (fractal canopy, binary tree,)
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk


def set_axis():
    ax1.grid()
    ax1.set_title('Fractal tree')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax1.set_aspect("equal")


def left(value):
    global theta_degree
    theta_degree = theta_degree + value


def right(value):
    global theta_degree
    theta_degree = theta_degree - value


def backward(value):
    global x, y
    x_next = x - value * np.cos(theta_degree * np.pi / 180.)
    y_next = y - value * np.sin(theta_degree * np.pi / 180.)
    x_line_points.append(x_next)
    y_line_points.append(y_next)
    x = x_next
    y = y_next


def forward(value):
    global x, y
    x_next = x + value * np.cos(theta_degree * np.pi / 180.)
    y_next = y + value * np.sin(theta_degree * np.pi / 180.)
    x_line_points.append(x_next)
    y_line_points.append(y_next)
    x = x_next
    y = y_next


def home():
    global x, y
    x = x_home
    y = y_home


def change_skew(value):
    global skew
    skew = value
    clear_curve()
    draw_graph()


def change_ratio(value):
    global ratio_length
    ratio_length = value
    clear_curve()
    draw_graph()


def change_angle(value):
    global angle
    angle = value
    clear_curve()
    draw_graph()


def change_len_branch(value):
    global length_branch
    length_branch = value
    clear_curve()
    draw_graph()


def clear_curve():
    global x_line_points, y_line_points
    x_line_points.clear()
    y_line_points.clear()
    ax1.cla()
    set_axis()
    canvas.draw()
    home()


def binary_tree(len_branch):
    if len_branch > length_branch_min:
        forward(len_branch)
        right(angle + skew)
        binary_tree(len_branch * ratio_length)
        left(angle * 2.)
        binary_tree(len_branch * ratio_length)
        right(angle - skew)
        backward(len_branch)


def draw_graph():
    binary_tree(length_branch)
    ax1.plot(x_line_points, y_line_points, c=line_color, linewidth=1)
    canvas.draw()


# Global variables
# axes
x_min = -500.
x_max = 500.
y_min = -200.
y_max = 500.

# Parameters
x_home = 0.
y_home = 0.
x = x_home
y = y_home
theta_degree = 0.
line_color = 'green'

x_line_points = []
y_line_points = []

x_line_points.append(0.)
y_line_points.append(0.)

angle = 30.
length_branch = 100.
ratio_length = 0.75
length_branch_min = 5.
skew = 0.

# Generate figure and axes
fig = Figure()
ax1 = fig.add_subplot(111)

# Embed in Tkinter
root = tk.Tk()
root.title("Fractal tree")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

lbl_len_branch = tk.Label(root, text="Length")
lbl_len_branch.pack(side='left')
var_len_branch = tk.StringVar(root)  # variable for spinbox-value
var_len_branch.set(length_branch)  # Initial value
spn_len_branch = tk.Spinbox(
    root, textvariable=var_len_branch, format="%.1f", from_=10., to=200, increment=10.,
    command=lambda: change_len_branch(float(var_len_branch.get())), width=5
    )
spn_len_branch.pack(side='left')

lbl_ratio = tk.Label(root, text="Ratio")
lbl_ratio.pack(side='left')
var_ratio = tk.StringVar(root)  # variable for spinbox-value
var_ratio.set(ratio_length)  # Initial value
spn_ratio = tk.Spinbox(
    root, textvariable=var_ratio, format="%.2f", from_=0.1, to=0.8, increment=0.01,
    command=lambda: change_ratio(float(var_ratio.get())), width=5
    )
spn_ratio.pack(side='left')

lbl_angle = tk.Label(root, text="Angle(degree)")
lbl_angle.pack(side='left')
var_angle = tk.StringVar(root)  # variable for spinbox-value
var_angle.set(angle)  # Initial value
spn_angle = tk.Spinbox(
    root, textvariable=var_angle, format="%.1f", from_=0., to=180., increment=1.,
    command=lambda: change_angle(float(var_angle.get())), width=5
    )
spn_angle.pack(side='left')

lbl_skew = tk.Label(root, text="Skew(degree)")
lbl_skew.pack(side='left')
var_skew = tk.StringVar(root)  # variable for spinbox-value
var_skew.set(skew)  # Initial value
spn_skew = tk.Spinbox(
    root, textvariable=var_skew, format="%.1f", from_=-90., to=90., increment=1.,
    command=lambda: change_skew(float(var_skew.get())), width=5
    )
spn_skew.pack(side='left')

btn_draw = tk.Button(root, text="Draw", command=draw_graph)
btn_draw.pack(side='left')

btn_clear = tk.Button(root, text="Clear", command=clear_curve)
btn_clear.pack(side='left')

# main loop
left(90)
clear_curve()
root.mainloop()
