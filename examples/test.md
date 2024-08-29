# mathmark

`mathmark` is a simple program that parses python files and creates a markdown file from this python file. The idea of `mathmark`is to document the process of retriving results for engeneering computation. The mathematics include basic numeric formulars. More advanced tasks can be done with sympy.
One basic idea is to extend python with comments which are used to identify differnt blocks. These blocks are divided by `#{identifier}`

## blocks  

python blocks are seperated by adding these definitions at the top:
- `show_block = False`:
  runs a python code but is not rendering it in the document. By default `show_block` is set to True
- `render_equations`
  runs the python code and renders the equations.

## representing formulars in markdown

\begin{equation}
   E = mc^2
\end{equation}

In equation \eqref{eq:sample}, we find the value of an
interesting integral:

\begin{equation}
  \int_0^\infty \frac{x^3}{e^x-1}\,dx = \frac{\pi^4}{15}
  \label{eq:sample}
\end{equation}

<!---
## code interpreted (not rendered)
--->

```python
render_block = False
from sympy.physics.units import *
```

## code interpreted (rendered)
```python
a = 10
b = 20
for i in range(10):
  i + 1
```

## formulas rendered

```python
render_equations = True
a = 10 * kg
b = 20 * m
c = a * b  #c this is a * b #r eq:test
```

In equation \eqref{eq:test}, we multiply a and b.
