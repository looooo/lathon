import code

import sympy
from sympy import latex, sympify
from sympy.physics.units import *

import mistletoe
from mistletoe.contrib.mathjax import MathJaxRenderer
from mistletoe.contrib.pygments_renderer import PygmentsRenderer


class MathMarkRenderer(MathJaxRenderer, PygmentsRenderer):
    testoperator = ["=", "<", ">", "=="]
    replacement_map = {}
    prefered_units = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mathjax = '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>\n'
        self.mathjax += '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n'
        self.eq_numbering = '<script>window.MathJax = {tex: {tags: "ams"}};</script>'
        self.interpreter = code.InteractiveInterpreter()
        self.interpreter.locals['render_block'] = True
        self.interpreter.locals['render_equations'] = False
        self.units = {}
        
        exec("from sympy.physics.units import *", self.units)


    def render_document(self, token):
        return super().render_document(token) + self.mathjax + self.eq_numbering

    def remove_first_line(self, content, check):
        """
        remove first line if content starts with check
        """
        content_lines = content.split('\n')
        if content_lines[0].startswith(check):
            content_lines = content_lines[1:]
        return '\n'.join(content_lines)

    def render_block_code(self, token):
        language = token.language
        content = token.content
        if language == 'python':
            self.interpreter.runcode(content)

            render_block = self.interpreter.locals['render_block']
            self.interpreter.locals['render_block'] = True

            render_equations = self.interpreter.locals['render_equations']
            self.interpreter.locals['render_equations'] = False

            content = self.remove_first_line(content, 'render_block')
            content = self.remove_first_line(content, 'render_equations')
            if render_block and not render_equations:
                token.children[0].content = content
                return super().render_block_code(token)
            if render_equations:
                print("hello")
                return self.block_to_latex(content)
        return ''
    
    def block_to_latex(self, content):
        """
        convert block of code to latex
        """
        content_lines = content.split('\n')
        output = ""
        for line in content_lines:
            latex_string = self.python_to_latex(line)
            if latex_string:
                output += latex_string
        return output

    def python_to_latex(self, line):
        """
        convert python code to latex
        """
        outlist = []
        output = ""
        if len(line) > 0:
            line = line.rsplit("#")
            comment = ""
            unit = ""
            manual_unit = None
            reference = None
            for i, st in enumerate(line):
                if i == 0:
                    equations = st
                elif st[0] == "c":   # comment
                    comment = self.replace_leading_space(st[1:])
                elif st[0] == "u":   # unit not sure how to use this
                    unit = self.replace_leading_space(st[1:])
                elif st[0] == "n":   # manual unit
                    manual_unit = self.replace_leading_space(st[1:])
                elif st[0] == "r":   # reference
                    reference = self.replace_tip_space(st[1:])

            # equ handling:
            equations = equations.replace(" ", "")
            equations = self.equation_to_parts(equations)
            output += "\\begin{flalign} \n"
            for equ in equations:
                if equ in self.testoperator:
                    outlist.append(equ)
                else:                 
                    temp = sympify(
                            equ,
                            convert_xor=True,  # ^ -> **
                            strict=False,      # no idea
                            rational=False,    # 1/2 -> 0.5
                            locals=self.units  # eg m -> sympy.physics.units.meter
                            )
                    outlist.append(sympy.latex(temp, mul_symbol="dot"))
            val = value = self.interpreter.locals[equations[0]]
            try:
                value = value.simplify()
                value = value.nsimplify()
            except AttributeError as e:
                pass

            quant = None
            mul_value = 1.
            if unit:
                sym_unit = sympify(unit, locals=self.units)
                value = convert_to(value, sym_unit)
            if hasattr(value, "as_two_terms"):
                value, quant = value.as_two_terms()
                replace_quants = self.prefered_units
                for test_quant, replace in replace_quants:
                    if (quant / test_quant).is_Number:
                        mul_value = quant / test_quant
                        quant = "\\," + sympy.latex(sympify(replace), mul_symbol="dot")
                        break
                else:
                    quant = "\\," + sympy.latex(quant, mul_symbol = "dot")
            # if a value is directly set to a variable
            if str(val) == str(temp) or (val - temp) == 0:
                outlist[-1] = sympy.latex(f"{value * mul_value:.2e}")
            else:
                outlist.append("=")
                outlist.append(sympy.latex(f"{value * mul_value:.2e}"))
            if manual_unit:
                outlist.append(manual_unit)
            elif quant:
                outlist.append(quant)
            for equ in outlist:
                output += equ
            if comment:
                output += "& & \\text{" + comment + "}"
            else:
                output += "& & \\text{""}"
            if reference:
                output += " \\label{" + reference + "}\n"
            output += "\\end{flalign}\n"
            for find, replace in self.replacement_map.items():
                output.replace(find, replace)
            return output
        
    def equation_to_parts(self, string):
        """
        split a equation into parts
        """
        equations = []
        inp = ""
        for i in string:
            if i in self.testoperator:
                if len(inp) > 0:
                    equations.append(inp)
                    inp = ""
                equations.append(i)
            else:
                inp += i
        equations.append(inp)
        return(equations)

    def replace_leading_space(self, string):
        return self.replace_leading_space(string[1:]) if string[0] == " " else string
    
    def replace_ending_space(self, string):
        return self.replace_ending_space(string[:-1]) if string[-1] == " " else string
    
    def replace_tip_space(self, string):
        string = self.replace_leading_space(string)
        string = self.replace_ending_space(string)
        return string


with open('examples/mathmark_example.md', 'r') as fin:
    with MathMarkRenderer() as renderer:
        with open("/Users/lo/tmp/test.html", "w") as fout:
            fout.write(renderer.render(mistletoe.Document(fin)))

