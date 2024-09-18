from dataclasses import dataclass
from rich import print
import sly

import re

@dataclass
class Token:
  type: str
  value: str
  lineo: int = 1
  
#Add the uninary minus and plus operatos
#Add the  % operator
class Lexer(sly.Lexer):
  tokens = [
    (r'\s+', None),
    (r'\d+(\.\d+)?([Ee][+-]?\d+)?', lambda s, tok: Token('NUMBER', tok)),
    (r'%',                          lambda s, tok: Token('%', tok)),
    (r'\+',                         lambda s, tok: Token('+', tok)),
    (r'-',                          lambda s, tok: Token('-', tok)),
    (r'\*',                         lambda s, tok: Token('*', tok)),
    (r'/',                          lambda s, tok: Token('/', tok)),
    (r'\(',                         lambda s, tok: Token('(', tok)),
    (r'\)',                         lambda s, tok: Token(')', tok)),
    (r'.',                          lambda s, tok: print(f"Illegal Character: '{tok}'")),
  ]
  
  def tokenize(self,data):
    scanner = re.Scanner(self.tokens)
    results,_ = scanner.scan(data)
    return iter(results)
  
if __name__ == '__main__':
  lexer = Lexer()
  data = """
  - (1 + 2) * 3
  4 % 5
  """
  tokens = lexer.tokenize(data)
  for token in tokens:
    print(token)