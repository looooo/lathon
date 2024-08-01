##python
from sympy.physics.units import mm, cm, m
import lathon

##lathon
alpha = 10 * mm + 1 * cm  #c not working
beta_ = 300000 * m
gamma_ = beta_ + alpha  #c not working
gamma_ < beta_ + alpha  #c not working