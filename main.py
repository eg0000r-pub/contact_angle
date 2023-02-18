#!/bin/python3
# Contact angle calculation program by Egor Demidov

# DEPENDENCIES:
# - matplotlib
# - numpy
# - pillow

# KNOWN ISSUE: only works for contact angles less than 90

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title='Select an image')
img = np.asarray(Image.open(file_path))

fig, ax = plt.subplots()
ax.imshow(img)
plt.title('Select one corner (right-click)')

xs = []
ys = []


# Circle: x^2 + y^2 + 2gx + 2fy + c = 0
# where center (h, k) is (-g, -f) and radius is r^2 = h^2 + k^2 - c
# Rewrite as: 2x*g + 2y*f + 1*c = -x^2 - y^2
# Returns center and radius
def solve_circle(xs, ys):
    A = np.array([
        [2*xs[0], 2*ys[0], 1],
        [2*xs[1], 2*ys[1], 1],
        [2*xs[2], 2*ys[2], 1]
    ])
    B = np.array([
        [-xs[0]**2-ys[0]**2],
        [-xs[1]**2-ys[1]**2],
        [-xs[2]**2-ys[2]**2],
    ])
    sol = np.matmul(np.linalg.inv(A), B)
    h = -sol[0]
    k = -sol[1]
    c = sol[2]
    r = np.sqrt(h**2 + k**2 - c)
    return np.array([h, k]), r


def onclick(event):
    if event.button == 3:
        ax.scatter(event.xdata, event.ydata, color='r')
        xs.append(event.xdata)
        ys.append(event.ydata)

        if len(xs) == 1:
            plt.title('Select second corner (right-click)')
        elif len(xs) == 2:
            ax.plot([xs[0], xs[1]], [ys[0], ys[1]], 'r')
            plt.title('Select a point on the circle (right-click)')
        elif len(xs) == 3:
            center, r = solve_circle(xs, ys)
            t = np.arange(0, 2*np.pi, 0.01)
            xc = r*np.cos(t)+center[0]
            yc = r*np.sin(t)+center[1]
            ax.plot(xc, yc, 'r')
            slope = ((center[0]-xs[0])/(ys[0]-center[1]))[0]  # dy/dx = (h-x)/(y-k)
            ax.plot([xs[0], xs[1]], [ys[0], ys[0]+slope*(xs[1]-xs[0])], 'r')
            vec1 = np.array([xs[1]-xs[0], ys[1]-ys[0]])
            vec2 = np.array([xs[1]-xs[0], slope*(xs[1]-xs[0])])
            cos_theta = np.dot(vec1, vec2)/np.linalg.norm(vec1)/np.linalg.norm(vec2)
            theta = np.arccos(cos_theta)*180/np.pi
            print(f'Contact angle: {theta:.2f} deg')
            plt.title(f'$\\theta={theta:.2f}^\\circ$')

        plt.draw()


fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
