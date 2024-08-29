##latex <Example
# In this example we are computing the first eigenfrequencies of a cantilever beam. First
# we are going to use the analytic solution and then we are going to compare this result
# with a computation by FreeCAD via the FEM-workbench.

##code <<imports
import lathon
from numpy import pi
from sympy import sqrt
from sympy.physics.units import m, cm, mm, Pa, kg, s
from matplotlib import pyplot as plt


##lathon << Defining the cantilever beam and it's properties
l_ = 1000. * mm                          	#r eqn:length #c the length of the cantilever beam
w  = 200 * mm                             	#c the width of the cantilever beam
h_ = 100 * mm                            	#c the height of the cantilever beam
A = w * h_                              	#u cm #c the cross section area of the cantilever beam
E_ = 70. * 10**6 * kg / mm / s ** 2     	#c the Young's modulus for aluminium
nu = 0.33 									#c Poisson atio
G = 1 / (2 * (1 + nu)) * E_
rho = 2700. * 10**(-9) * kg / mm ** 3       #c the density of aluminium

##lathon <<Analytic solution
I_yy = w * h_ ** 3 / 12                                           #u cm**4 #c the second moment of area of the cantilever beam
I_zz = h_ * w ** 3 / 12                                           #u cm**4 #c the second moment of area of the cantilever beam
I_p = I_yy + I_zz												  #u cm**4 #c polar second moment of area
k_b1 = 4.73                                                       #c constant for the first bending eigenfrequency
c_t1 = 1 / 3 * (1 - 0.630 / (w / h_) + 0.052 / (w / h_) ** 5)     #c approximation formula
I_t = c_t1 * h_**3 * w  										  #u cm**4 #c approximation formula
nu_b1 = k_b1 ** 2 / 2 / pi / l_ ** 2 * sqrt(E_ * I_yy / A / rho)  #r nub1 #u hertz #c the first bending eigenfrequency
nu_b2 = k_b1 ** 2 / 2 / pi / l_ ** 2 * sqrt(E_ * I_zz / A / rho)  #r nub2 #u hertz #c the first bending eigenfrequency
nu_t1 = 1 / (l_ * 2) * sqrt(G * I_t / (rho * I_p))				  #r nut1 #u hertz #c the first torsion eigenfrequency


##latex <<FreeCAD result
##python
lathon.Parser.add_image("m1.png", scale=0.3, text="first bending mode first axis")
lathon.Parser.add_image("m2.png", scale=0.3, text="first bending mode second axis")
lathon.Parser.add_image("m3.png", scale=0.3, text="first torsion mode")
lathon.Parser.add_image("calculix_result.png", scale=0.6, text="cantilever beam result")
