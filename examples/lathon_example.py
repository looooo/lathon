##latex <Example
# In this example we are computing the first eigenfrequency of a cantilever beam. First
# we are going to use the analytic solution and then we are going to compare this result
# with a computation by FreeCAD.
##code <<imports
import lathon
from numpy import pi
from sympy import sqrt
from sympy.physics.units import m, mm, Pa, kg, s
from matplotlib import pyplot as plt

##latex << defining the catilever beam

##lathon
l = 1000. * mm                          #c the length of the cantilever beam
w = 200 * mm                             #c the width of the cantilever beam
h_ = 100 * mm                            #c the height of the cantilever beam
E_ = 70. * 10**6 * kg / mm / s ** 2     #c the Young's modulus for aluminium
rho = 2700. * 10**(-9) * kg / mm ** 3               #c the density of aluminium
A = w * h_                              #c the cross section area of the cantilever beam

##lathon <<Analytic solution
I_yy = w * h_ ** 3 / 12                                          #c the second moment of area of the cantilever beam
k_1 = 4.73                                                       #c constant for the first bending eigenfrequency of a cantilever beam
nu_b1 = k_1 ** 2 / 2 / pi / l ** 2 * sqrt(E_ * I_yy / A / rho)   #c the first bending eigenfrequency of a cantilever beam

##latex <<FreeCAD solution
# trying to find the first bending eigenfrequency of a cantilever beam with FreeCAD failed with osx arm:
##python
lathon.Parser.add_image("osx_arm_freecad_result.png", scale=0.5, text="cantilever beam with freecad on osx-arm")

##latex
# with linux 64 the result looks better
##python
lathon.Parser.add_image("linux_64_freecad_result.png", scale=0.2, text="cantilever beam with freecad on linux-64")
lathon.Parser.add_image("linux_64_ccx_result.png", scale=0.4, text="cantilever beam result")