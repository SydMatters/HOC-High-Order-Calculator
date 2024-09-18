from dataclasses import dataclass
from rich import print
from lex import *
from hoc_ast import *


"""
Parser class
Attributes:
  tok : Token. The current token
  next_tok : Token. The next token
  tokens : list. The tokens
Methods:
  _advance : Advance the current token and the next token
  _accept : Accept the next token if it is of type type
  _expect : Expect the next token to be of type type
  expr : Parse an expression
  factor : Parse a factor
  list : Parse a list of expressions
  parse : Parse the tokens

"""
@dataclass
class Parser:
  tok : Token = None
  next_tok : Token = None
  tokens = None
  
  def _advance(self):
    self.tok, self.next_tok = self.next_tok, next(self.tokens, None)
    
  def _accept(self,tok_type):
    if self.next_tok and self.next_tok.type == tok_type:
      self._advance()
      return True
    return False
  
  def _expect(self, type):
    if not self._accept(type):
      raise SyntaxError(f"Expected {type} but got {self.next_tok.type}")
  
  #Each of the methods below parse a different part of the grammar
  def expr(self):
    """
    expr ::= NUMBER
            | '(' expr ')'
            | expr '+' expr
            | expr '-' expr
            | expr '*' expr
            | expr '/' expr
    """
    
    left = self.factor()
    while self._accept('+') or self._accept('-') or self._accept('*') or self._accept('/') or self._accept('%'):
      oper = self.tok.value
      rigth = self.factor()
      left = Binary(oper, left, rigth)
    return left
  
  def factor(self):
    if self._accept('+') or self._accept('-'):
      oper = self.tok.value
      operand = self.factor()
      return Unary(oper, operand)
    
    elif self._accept('NUMBER'):
      return Number(float(self.tok.value))
    elif self._accept('('):
      expr = self.expr()
      self._expect(')')
      return Parentheses(expr)
    else:
      raise SyntaxError(f"Expected NUMBER or '(' but got {self.next_tok.type}")

  def list(self):
    """
    list ::= expr NEWLINE
            list expr NEWLINE
    """
    list = []
    
    list.append(self.expr())
    
    while True:
      
      if self.next_tok == None:
        break
      
      list.append(self.expr())
    
    return list
  
  def parse(self, tokens):
    self.tok = None
    self.next_tok = None
    self.tokens = tokens
    self._advance()
    return self.list()
    
  
  
if __name__ == '__main__':
  lexer = Lexer()
  parser = Parser()
  data = """
  - (1 + 2) * 3
  4 % 5
  """
  tokens = lexer.tokenize(data)
  for token in tokens:
    print(token)
  
  ast = parser.parse(lexer.tokenize(data))
  print(ast)
  
  dot = MakeDot()
  
  for expr in ast:
    expr.accept(dot)
    
  
  ast_dot = dot.generate_dot()
    