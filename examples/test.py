## python
import numpy as np
import matplotlib.pyplot as plt
from sympy.physics.units import J, s

##code <<units definitions
lathon.use_units = [
    [J, "J"],
    [J * s, "J * s"]]
##latex
# TODO: convert this to a dictionary

##lathon <basics
gamma_ = 1.2 #c defining some variables
alpha = 10 #n m
beta_ = gamma_ * alpha
delta = 100

##latex <plot
# here is demostrated how to draw matplotlib 
# figures in the pdf

##python
a = np.linspace(0, 10, 100)
plt.figure(figsize=(8, 4))
plt.plot(a, np.cos(a) * np.sin(a)**2, label="test")
plt.legend()
plt.grid()
lathon.Parser.draw(name="plot", scale=0.6, text="this is a plot")

##latex <latex

# \[ x^n + y^n = z^n \]

##code <function
def a():
    return None