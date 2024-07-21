# mathmark

`mathmark` is a simple program that parses python files and creates a markdown file from this python file. The idea of `mathmark`is to document the process of retriving results for engeneering computation. The mathematics include basic numeric formulars. More advanced tasks can be done with sympy.
One basic idea is to extend python with comments which are used to identify differnt blocks. These blocks are divided by `#{identifier}`

## blocks  

the python file is diveded in several blocks. The following blocks are possible:
- python code (only interpreted): `#p`
- python code (interpreted and shown): `#pm`
- markdown directly `#m`

## representing formulars in markdown

$a^2 + b^2 = c^2$  
$\alpha + \beta = \gamma$

$$
a^2 + b^2
$$

