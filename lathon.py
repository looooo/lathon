import os
import code
from sympy import latex, sympify, N
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
        self.equunit = ""
        self.equstr = ""

        self._block_dict = {
            "python": self.run_python_block,
            "latex": self.run_latex_block,
            "lathon": self.run_lathon_block,
            "py": self.run_python_block,
            "la": self.run_latex_block,
            "pl": self.run_lathon_block
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
            '\\setlength{\mathindent}{1cm} \n'
            '\\usepackage{graphicx}\n'
            '\\usepackage{titlesec}\n'
            '\\usepackage{gensymb}\n'
            '\\usepackage{float}\n'
            '\AtBeginDocument{%\n'
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
        cls.latex_buffer += "\maketitle\n"

    @classmethod
    def section(cls, name):
        cls.latex_buffer += "\section{" + name + "}\n"

    @classmethod
    def subsection(cls, name):
        cls.latex_buffer += "\subsection{" + name + "}\n"

    @classmethod
    def text(cls, string):
        cls.latex_buffer += string

    @classmethod
    def draw(cls, name="plot", scale=1, text=""):
        import matplotlib.pyplot as plt
        path = check_path("/tmp/lathon/plots/", name, ".png")
        plt.savefig(path)
        cls.latex_buffer += "\\begin{figure}[H]"
        cls.latex_buffer += "\label{figure1}\n"
        cls.latex_buffer += "\centerline{\includegraphics[scale=" + str(scale) + "]{"+ path + "}}"
        cls.latex_buffer += "\\caption{" + text + "}"
        cls.latex_buffer += "\\end{figure}"
        plt.close()

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
        append = "\n\end{document}"
        path = check_path("/tmp/lathon/", "lathon.tex")

        with open(path, "w") as _file:
            _file.write(prepend)
            _file.write(self.latex_string)
            _file.write(append)
            _file.close()
        return path

    def show(self):
        path = self.write()
        os.system("pdflatex -interaction=batchmode -jobname=ausgabe" +
          " -output-directory=" + "/tmp/lathon/ " + path)
        os.system("evince /tmp/lathon/ausgabe.pdf")

    def split_blocks(self, string):
        string = "## py\n" + string
        string = string.rsplit("##")
        for block in string:
            if block:
                block = block.splitlines()
                header = block[0]
                header.rsplit(" ")
                block = '\n'.join(block[1:])
                header = self.make_headline(header)
                self._block_dict[header](block)

    def make_headline(self, header):
        header = header.rsplit(" ")
        header = [i for i in header if i]
        if len(header) == 2:
            h = header[1].rsplit("<")
            depth = len(h)
            if depth == 2:
                self.latex_string += "\section{" + h[-1] + "}\n"
            elif depth == 3:
                self.latex_string += "\subsection{" + h[-1] + "}\n"
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

    def py2la(self, string):
        outlist = []
        output = ""
        if len(string) > 0:
            string = string.rsplit("#")
            comment = ""
            unit = ""
            manual_unit = None
            for i, st in enumerate(string):
                if i == 0:
                    equations = st
                elif st[0] == "c":   # comment
                    comment = self.replace_leading_space(st[1:])
                elif st[0] == "u":
                    unit = self.replace_leading_space(st[1:])
                elif st[0] == "n":
                    manual_unit = self.replace_leading_space(st[1:])

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
                            convert_xor=True,
                            strict=False,
                            rational=False,
                            locals=self.units)
                    outlist.append(latex(temp, mul_symbol="dot"))
            val = value = self.interpreter.locals[equations[0]]
            quant = None
            mul_value = 1.
            if hasattr(value, "as_two_terms"):
                value.nsimplify()
                value, quant = value.as_two_terms()
                replace_quants = (self.file_buffer.prefered_units + 
                                  self.prefered_units)
                if unit:
                    replace_quants = [[sympify(unit, locals=self.units), unit]]
                for test_quant, replace in replace_quants:
                    if (quant / test_quant).is_Number:
                        mul_value = quant / test_quant
                        quant = "\," + latex(sympify(replace), mul_symbol="dot")
                        break
                else:
                    quant = "\," + latex(quant, mul_symbol = "dot")
            if str(val) == str(temp) or (val - temp) == 0:
                outlist[-1] = latex(value * mul_value)
            else:
                outlist.append("=")
                outlist.append(latex(value * mul_value))
            if quant:
                outlist.append(quant)
            elif manual_unit:
                outlist.append(manual_unit)
            for equ in outlist:
                output += equ
            if comment:
                output += "& & \\text{" + comment + "}\n"
            else:
                output += "& & \\text{""}\n"
            output += "\\end{flalign}\n"
            for find, replcae in self.replacement_map.items():
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

