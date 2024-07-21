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

##pl <Angaben
gamma = 1.2 * J

##la <<plot
# here is demostrated how to draw matplotlib 
# figures in the pdf

##py
a = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 4))
plt.plot(a, np.cos(a) * np.sin(a)**2, label="test")
plt.legend()
plt.grid()
lathon.Parser.draw(name="plot", scale=0.6, text="this is a plot")

##pl <something
alpha = 10 * s
beta = gamma * alpha
delta = 100

##la <some latex stuff

# \[ x^n + y^n = z^n \]