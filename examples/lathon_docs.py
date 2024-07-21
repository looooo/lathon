##latex
# \tableofcontents
# \newpage

##latex <lathon introduction
# lathon is a tool for documentation of numerical computation of tasks usually arising in engineering fields.
# python is used to compute the formulas and latex is then used for the documentation. Files that are able to be parsed with 
# lathon should also be valid python files, and therefore should run with a python interpreter directly, but this won't result 
# in a latex document.

##latex <<blocks
# the lathon blocks are seperated by two \lstinline{##} following an instruction. The instruction must be one of these entities:
# \begin{itemize}
#   \item \lstinline{##python}: 
#   This block will be executed by the python interpreter and is not added to the document.
#   \item \lstinline{##lathon}: 
#   This block will be executed by the python interpreter and is added to the document. 
#   Only python one line instructions are allowed. lathon is writing the instruction plus the 
#   result of the instruction to the document. (eg.: a = b + c = 100). Units can be added with sympy.
#   \item \lstinline{##latex}:
#   This block will be added to the document directly. \# is used to make sure this line is not run by
#   the python interpreter.
#   \item \lstinline{##code}
#   This block will be executed by the python interpreter and is added to the document as a code block.
# \end{itemize}

##latex <<lathon python API by example
# \lstinputlisting[language=python]{doc.py}
# \newpage
