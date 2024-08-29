import mistletoe
from mistletoe.contrib.mathjax import MathJaxRenderer

class MathMarkRenderer(MathJaxRenderer):
    def __init__(self, **kwargs):
        """
        Args:
            **kwargs: additional parameters to be passed to the ancestors'
                      constructors.
        """
        super().__init__(**kwargs)
        self.mathjax = '<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>\n'
        self.mathjax += '<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n'
        self.eq_numbering = '<script>window.MathJax = {tex: {tags: "ams"}};</script>'


    def render_document(self, token):
        return super().render_document(token) + self.mathjax + self.eq_numbering

with open('examples/test.md', 'r') as fin:
    with MathMarkRenderer() as renderer:
        print(renderer.render(mistletoe.Document(fin)))