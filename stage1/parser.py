from dataclasses import dataclass
from rich import print
from lex import *
from hoc_ast import *


"""
Clase Parser
Se encarga de parsear los tokens

Atributos:
  tok de tipo Token
  next_tok de tipo Token
  tokens de tipo iter

"""
@dataclass
class Parser:
  tok : Token = None
  next_tok : Token = None
  tokens = None
  
  #Metodo _advance: Avanza el token actual y el siguiente token
  def _advance(self):
    self.tok, self.next_tok = self.next_tok, next(self.tokens, None)
    
  #Meotodo _accept: Verifica si el siguiente token es de tipo type, si es así avanza el token
  def _accept(self,tok_type):
    if self.next_tok and self.next_tok.type == tok_type:
      self._advance()
      return True
    return False
  
  #Metodo _expect: Verifica si el siguiente token es de tipo type, si no lo es lanza una excepción
  def _expect(self, type):
    if not self._accept(type):
      raise SyntaxError(f"Expected {type} but got {self.next_tok.type}")
  
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
    