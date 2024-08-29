# Example
In this example we are computing the first eigenfrequencies of a cantilever beam. First
we are going to use the analytic solution and then we are going to compare this result
with a computation by FreeCAD via the FEM-workbench.

```python
render_block = False
from numpy import pi
from sympy import sqrt
from sympy.physics.units import m, cm, mm, Pa, kg, s
from matplotlib import pyplot as plt
```

## Definitions
```python
render_equations = True
l_ = 1000. * mm                          	#r eqn:length #c the length of the cantilever beam
w  = 200 * mm                             	#c the width of the cantilever beam
h_ = 100 * mm                            	#c the height of the cantilever beam
A = w * h_                              	#u cm #c the cross section area of the cantilever beam
E_ = 70. * 10**6 * kg / mm / s ** 2     	#c the Young's modulus for aluminium
nu = 0.33 									#c Poisson atio
G = 1 / (2 * (1 + nu)) * E_
rho = 2700. * 10**(-9) * kg / mm ** 3       #c the density of aluminium
```

## Analytic Solution
```python
render_equations = True
I_yy = w * h_ ** 3 / 12                                           #u cm**4 #c the second moment of area of the cantilever beam
I_zz = h_ * w ** 3 / 12                                           #u cm**4 #c the second moment of area of the cantilever beam
I_p = I_yy + I_zz												  #u cm**4 #c polar second moment of area
k_b1 = 4.73                                                       #c constant for the first bending eigenfrequency
c_t1 = 1 / 3 * (1 - 0.630 / (w / h_) + 0.052 / (w / h_) ** 5)     #c approximation formula
I_t = c_t1 * h_**3 * w  										  #u cm**4 #c approximation formula
nu_b1 = k_b1 ** 2 / 2 / pi / l_ ** 2 * sqrt(E_ * I_yy / A / rho)  #r nub1 #u hertz #c the first bending eigenfrequency
nu_b2 = k_b1 ** 2 / 2 / pi / l_ ** 2 * sqrt(E_ * I_zz / A / rho)  #r nub2 #u hertz #c the first bending eigenfrequency
nu_t1 = 1 / (l_ * 2) * sqrt(G * I_t / (rho * I_p))				  #r nut1 #u hertz #c the first torsion eigenfrequency
```

![image](/Users/lo/projects/freecad/lathon/examples/m1.png)
![image](/Users/lo/projects/freecad/lathon/examples/m2.png)
![image](/Users/lo/projects/freecad/lathon/examples/m3.png)