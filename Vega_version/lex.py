from dataclasses import dataclass
from rich import print
import sly

import re

"""
Token class
Attributes:
  type : str. The type of the token
  value : str. The value of the token
  lineo : int. The line of the token
"""
@dataclass
class Token:
  type: str
  value: str
  lineo: int = 1
  
"""
Lexer class
Inherits from sly.Lexer
Attributes:
  tokens : list. The tokens
Methods:
  tokenize : Tokenize the input data
""" 
class Lexer(sly.Lexer):
  
  # Constants 
  constants = {
    'PI': 3.141592653589793,
    'E': 2.718281828459045,
    'GAMMA': 0.57721566490153286060,
    'DEG': 57.29577951308232087680,
    'PHI': 1.61803398874989484820,
  }
  
  def token_classify(self, tok):
    if tok in Lexer.constants:
      return Token('CONST', tok)
    elif tok in ['sin', 'cos', 'atan', 'log', 'log10', 'exp', 'sqrt', 'abs', 'int',]:
      return Token('FUNC', tok)
    else:
      return Token('VAR', tok)
  # Set of token names. This is always required
  # List of regular expression rules. (name, pattern)
  tokens = [
    (r'\s+', None),
    (r'[a-zA-Z_][a-zA-Z0-9_]*',     lambda s, tok: Lexer.token_classify(s,tok)),  
    (r'\d+(\.\d+)?([Ee][+-]?\d+)?', lambda s, tok: Token('NUMBER', tok)),
    (r'\^',                         lambda s, tok: Token('^', tok)),
    (r'%',                          lambda s, tok: Token('%', tok)),
    (r'\+',                         lambda s, tok: Token('+', tok)),
    (r'-',                          lambda s, tok: Token('-', tok)),
    (r'\*',                         lambda s, tok: Token('*', tok)),
    (r'/',                          lambda s, tok: Token('/', tok)),
    (r'\(',                         lambda s, tok: Token('(', tok)),
    (r'\)',                         lambda s, tok: Token(')', tok)),
    (r'=',                          lambda s, tok: Token('=', tok)),
    (r'.',                          lambda s, tok: print(f"Illegal Character: '{tok}'")),
  ]
  
  def tokenize(self,data):
    scanner = re.Scanner(self.tokens) # The scanner method from re module is used to tokenize the input data
    results,_ = scanner.scan(data) # The scan method returns a tuple with the tokens and the remaining data
    return iter(results)