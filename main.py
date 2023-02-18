#!/bin/python3
# Contact angle calculation program by Egor Demidov

# DEPENDENCIES:
# - matplotlib
# - numpy
# - pillow

# INSTRUCTIONS:
# (1) Select an image file when prompted in the file dialog
# (2) Use the toolbar to zoom in on the droplet as needed
# (3) Right-click on the origin (corner of the droplet)
# (4) Right-click on the opposite corner of the droplet
# (5) Right-click on a point on a line tangent to the surface (close to the origin)
# Calculated contact angle will be displayed in the plot title and printed to stdout

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
plt.title('Select origin (right-click)')

xs = []
ys = []

# # x^2 + y^2 + 2gx + 2fy + c = 0
# def find_circle(xs, ys):
#

# First point is the corner
def onclick(event):
    if event.button == 3:
        ax.scatter(event.xdata, event.ydata, color='r')
        xs.append(event.xdata)
        ys.append(event.ydata)

        if len(xs) == 1:
            plt.title('Select first vector (right-click)')
        elif len(xs) == 2:
            ax.plot([xs[0], xs[1]], [ys[0], ys[1]], 'r')
            plt.title('Select second vector (right-click)')
        elif len(xs) == 3:
            ax.plot([xs[0], xs[2]], [ys[0], ys[2]], 'r')
            vec1 = np.array([xs[1] - xs[0], ys[1] - ys[0]])
            vec2 = np.array([xs[2] - xs[0], ys[2] - ys[0]])
            cos_theta = np.dot(vec1, vec2) / np.linalg.norm(vec1) / np.linalg.norm(vec2)
            print(f'Contact angle: {np.arccos(cos_theta) * 180 / np.pi:.2f} deg')
            plt.title(f'$\\theta={np.arccos(cos_theta) * 180 / np.pi:.2f}^\\circ$')

        plt.draw()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
