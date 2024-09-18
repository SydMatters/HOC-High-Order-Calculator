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
      raise SyntaxError(f'Expected {type} but got {self.next_tok.type}') 
    
  def assignment (self, var):
    """
    assignment ::= VAR '=' expr
    """
    self._expect('=')
    expr = self.expr()
    
    if isinstance (expr, Variable) and self.next_tok.type == '=':
      expr = self.assignment(expr)
      
    return Assignment(var, expr)
    
    
  #Each of the methods below parse a different part of the grammar
  def expr(self):
    """
    expr ::= NUMBER
          VAR
          asgn
          BLTIN ( expr )
          expr + expr
          expr - expr
          expr * expr
          expr / expr
          expr ^ expr
          ( expr )
          '-' expr
          '+' expr
    """
      
    left = self.factor()
    
    if self._accept('^'):
      exp = self.expr()
      left = Exponentiation(left, exp)
    
    while self._accept('+') or self._accept('-') or self._accept('*') or self._accept('/') or self._accept('%'):
      oper = self.tok.value
      rigth = self.factor()
      if oper == '/' and isinstance(rigth, Number) and rigth.value == 0:
        raise ValueError("Division by zero")
      left = Binary(oper, left, rigth)
      
    return left
  
  def factor(self):
    if self._accept('+') or self._accept('-'):
      oper = self.tok.value
      operand = self.factor()
      return Unary(oper, operand)
    elif self._accept('NUMBER'):
      return Number(float(self.tok.value))
    elif self._accept('CONST'):
      return Number(Lexer.constants[self.tok.value])
    elif self._accept('FUNC'):
      func = self.tok.value
      self._expect('(')
      expr = self.expr()
      self._expect(')')
      return Function(func, expr)
    elif self._accept('VAR'):
      return Variable(self.tok.value)
    elif self._accept('('):
      expr = self.expr()
      self._expect(')')
      return Parentheses(expr)
    else:
      raise SyntaxError(f"Expected NUMBER, VAR, FUNC, CONST or '(' but got {self.next_tok.type}")

  def list(self):
    """
    list ::= list \n
          list expr \n
          list asgn \n
    """
    list = []
    
    while self.next_tok != None:
      if self._accept('VAR'):
        var = Variable(self.tok.value)
        if self.next_tok and self.next_tok.type == '=':
          list.append(self.assignment(var))
        else:
          list.append(var)
      else:
        list.append(self.expr())
      
      if self.next_tok is None:
        break
      
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
  
  x = y = cos(x^5) + sin(x + y + z) + (a/b) + (cos(PI) - sin(E - PHI))

  1.5 ^ 2.3

  exp(2.3*log(1.5))

  atan(1)*DEG

  x = y = z = 0

  y = 5 ^ (2 ^ 3)


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
    