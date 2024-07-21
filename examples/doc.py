import lathon

parser = lathon.Parser()
parser.parse_file("lathon_docs.py")
parser.parse_file("lathon_example.py")
parser.show()