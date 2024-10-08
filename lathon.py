import os
import sys
import code
import re

import sympy
from sympy import latex, sympify
from sympy.physics.units import *


def use_units(units):
    Parser.prefered_units = units


def check_path(path, name, suffix="", nr=0):
    _dir = os.path.dirname(path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    if os.path.isfile(path + name + str(nr) + suffix):
        return check_path(path, name, suffix, nr + 1)
    else:
        return path + name + str(nr) + suffix


class Parser(object):
    testoperator = ["=", "<", ">", "=="]
    replacement_map = {}
    latex_buffer = ''
    prefered_units = []

    def __init__(self):
        self.interpreter = code.InteractiveInterpreter()

        self._block_dict = {
            "python": self.run_python_block,
            "latex": self.run_latex_block,
            "lathon": self.run_lathon_block,
            "code": self.run_code_block,
            }
        self.units = {}
        self.latex_string = ''
        exec("from sympy.physics.units import *", self.units)
        self.prependtext = (
            '\\documentclass[ngerman,fleqn,a4paper]{article}\n'
            '\\usepackage[utf8]{inputenc}\n'
            '\\usepackage{babel}\n'
            '\\usepackage{a4wide}\n'
            '\\usepackage{amsmath}\n'
            '\\setlength{\\mathindent}{1cm} \n'
            '\\usepackage{graphicx}\n'
            '\\usepackage{titlesec}\n'
            '\\usepackage{gensymb}\n'
            '\\usepackage{float}\n'
            '\\usepackage{listings}\n'
            '\\AtBeginDocument{%\n'
            '   \\abovedisplayskip=4pt plus 3pt minus 4pt\n'
            '   \\abovedisplayshortskip=0pt plus 3pt\n'
            '   \\belowdisplayskip=3pt plus 3pt minus 3pt\n'
            '   \\belowdisplayshortskip=0pt plus 3pt minus 3pt\n'
            '}')

    @classmethod
    def title(cls, title, author=""):
        cls.latex_buffer += "\\title{" + title + "}\n"
        if author:
            cls.latex_buffer += "\\author{" + author + "}\n"
        cls.latex_buffer += "\\maketitle\n"

    @classmethod
    def section(cls, name):
        cls.latex_buffer += "\\section{" + name + "}\n"

    @classmethod
    def subsection(cls, name):
        cls.latex_buffer += "\\subsection{" + name + "}\n"

    @classmethod
    def text(cls, string):
        cls.latex_buffer += string

    @classmethod
    def draw(cls, name="plot", scale=1, text=""):
        import matplotlib.pyplot as plt
        path = check_path("/tmp/lathon/plots/", name, ".png")
        plt.savefig(path)
        cls.latex_buffer += "\\begin{figure}[H]"
        cls.latex_buffer += "\\label{figure1}\n"
        cls.latex_buffer += "\\centerline{\\includegraphics[scale=" + str(scale) + "]{"+ path + "}}"
        cls.latex_buffer += "\\caption{" + text + "}"
        cls.latex_buffer += "\\end{figure}"
        plt.close()
    
    @classmethod
    def add_image(cls, path, scale=1, text=""):
        cls.latex_buffer += "\\begin{figure}[H]"
        cls.latex_buffer += "\\label{figure1}\n"
        cls.latex_buffer += "\\centerline{\\includegraphics[scale=" + str(scale) + "]{"+ path + "}}"
        cls.latex_buffer += "\\caption{" + text + "}"
        cls.latex_buffer += "\\end{figure}"

    @property
    def file_buffer(self):
        return self.interpreter.locals["lathon"].Parser

    def clean_buffer(self):
        self.file_buffer.latex_string=""


    def parse_file(self, file_name):
        self.interpreter.runcode("import lathon\n")
        self._parse_file(file_name)

    def _parse_file(self, file_name):
        with open(file_name) as _file:
            self.parse(_file.read())

    def parse_me(self):
        import inspect
        filename = inspect.getouterframes(inspect.currentframe())[1][1]
        self.interpreter.runcode("import lathon\n")
        self.interpreter.runcode("__name__ = '__not_main__'")
        self.file_buffer.latex_buffer = ""
        self._parse_file(filename)

    def parse(self, string):
        self.interpreter.runcode("import lathon\n")
        self.split_blocks(string)

    def write(self):
        prepend = self.prependtext
        prepend += "\\begin{document}\n"
        append = "\n\\end{document}"
        path = check_path("/tmp/lathon/", "lathon.tex")

        with open(path, "w") as _file:
            _file.write(prepend)
            _file.write(self.latex_string)
            _file.write(append)
        return path

    def show(self):
        path = self.write()
        os.system("pdflatex -interaction=batchmode -jobname=ausgabe" +
                  " -output-directory=" + "/tmp/lathon/ " + path)
        os.system("evince /tmp/lathon/ausgabe.pdf")

    def split_blocks(self, string):
        # string = "## python\n" + string
        string = string.rsplit("\n##")
        # removing the first two identifiers
        if string[0][:2] == "##":
            string[0] = string[0][2:]
        for block in string:
            if block:
                block = block.splitlines()
                header = block[0]
                block = '\n'.join(block[1:])
                header = self.make_headline(header)
                self._block_dict[header](block)

    def make_headline(self, header):
        header = header.split(" ", 1)
        header = [i for i in header if i]
        if len(header) == 2:
            h = header[1].rsplit("<")
            depth = len(h)
            if depth == 2:
                self.latex_string += "\\section{" + h[-1] + "}\n"
            elif depth == 3:
                self.latex_string += "\\subsection{" + h[-1] + "}\n"
        return header[0]

    def run_python_block(self, block):
        self.interpreter.runcode(block)
        self.latex_string += self.file_buffer.latex_buffer
        self.file_buffer.latex_buffer = ""

    def run_latex_block(self, block):
        self.latex_string += block

    def run_lathon_block(self, block):
        block = block.splitlines()
        for line in block:
            if line:
                self.interpreter.runcode(line)
                self.latex_string += self.py2la(line)

    def run_code_block(self, block):
        self.interpreter.runcode(block)
        self.latex_string += "\\begin{lstlisting}\n"
        self.latex_string += block
        self.latex_string += "\n\\end{lstlisting}\n"

    def equtoparts(self, string):
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


    def py2la(self, string):
        outlist = []
        output = ""
        if len(string) > 0:
            string = string.rsplit("#")
            comment = ""
            unit = ""
            manual_unit = None
            reference = None
            for i, st in enumerate(string):
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
            equations = self.equtoparts(equations)
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
                replace_quants = (self.file_buffer.prefered_units + 
                                  self.prefered_units)
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

    def isstringnumber(self, string):
        try:
            float(string)
        except ValueError:
            return(False)
        else:
            if string in ("True", "False"):
                return(False)
            else:
                return(True)

def python2latex():
    if len(sys.argv) < 2:
        print("usage: python2latex <filename>")
        sys.exit(1)
    with open(sys.argv[1]) as _file:
        string_file = _file.read()
    my_parser = Parser()
    my_parser.parse(string_file)
    my_parser.show()
