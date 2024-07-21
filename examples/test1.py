##py
import lathon
import numpy as np
from sympy.physics.units import *
from matplotlib import pyplot as plt

lathon.use_units = [
    [J, "J"],
    [J * s, "J * s"]]


##la
# \tableofcontents
# \newpage


##pl <basics
gamma_ = 1.2 * J
alpha = 10 * s
beta_ = gamma_ * alpha
delta = 100

##la <plot
# here is demostrated how to draw matplotlib 
# figures in the pdf

##py
a = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 4))
plt.plot(a, np.cos(a) * np.sin(a)**2, label="test")
plt.legend()
plt.grid()
lathon.Parser.draw(name="plot", scale=0.6, text="this is a plot")

##la <latex

# \[ x^n + y^n = z^n \]