import lathon

parser = lathon.Parser()
parser.parse_file("test1.py")
parser.parse_file("test2.py")
parser.show()