##python
import lathon
import numpy as np
from sympy.physics.units import *
from matplotlib import pyplot as plt

lathon.use_units = [
    [J, "J"],
    [J * s, "J * s"]]


## lathon <Angaben
var_1 = 1.2 * J

## python
lathon.Parser.subsection("plot")
lathon.Parser.text("""
	here it is demostrated how to draw matplotlib 
	figures in the pdf
	""")

a = np.linspace(0, 10, 100)
plt.figure(figsize=(10, 4))
plt.plot(a, np.cos(a) * a, label="test")
plt.legend()
plt.grid()
lathon.Parser.draw(name="plot", scale=0.6, text="this is a plot")

## lathon <some thing
var_2 = 10 * s
var_3 = var_1 * var_2
var_4 = 100