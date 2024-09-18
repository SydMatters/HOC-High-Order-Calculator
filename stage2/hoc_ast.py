from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from rich import print
from multimethod import multimeta

from lex import *
from graphviz import Digraph

"""
ATS (Abstract Syntax Tree)
Is a tree representation of the abstract syntactic structure of source code written in a programming language.
Each node of the tree denotes a construct occurring in the source code.
The syntax is "abstract" in not representing every detail appearing in the real syntax.
"""

"""
Design pattern: Visitor
The Visitor pattern is a way of separating an algorithm from an object structure on which it operates.
A practical result of this separation is the ability to add new operations to existing object structures
without modifying those structures.
It is used here because the AST is a complex structure that is difficult to traverse and analyze.
The Visitor pattern allows us to separate the algorithm from the AST structure.
The Visitor pattern is implemented with the multimethod library.
The multimethod library allows us to implement multiple dispatch in Python.
Dispatch significa que se llama a una función diferente dependiendo de los argumentos.

"""

#Abstract classes----------------------------------------------

"""
Visitor class
Metaclass = multimeta
An abstract class of the Visitor pattern
"""
@dataclass
class Visitor(metaclass = multimeta):
  pass

"""
Node class
An abstract class of the AST
Methods:
  accept(self, v: Visitor) -> str : Abstract method for the Visitor pattern

Note: The accept method is an abstract method that must be implemented in the subclasses of the Node class.
The visit methhod belongs to the visitor class because it is a multimethod.
"""
@dataclass
class Node:
  def accept(self, v: Visitor):
    return v.visit(self) 
  
"""
Expression class
Inherits from Node

An abstract class
"""
@dataclass
class Expression (Node):
  pass

"""
Variable class
Inherits from Expression
Attributes:
  name : str. The name of the variable
"""
@dataclass
class Variable (Expression):
  name: str


@dataclass
class Assignment (Expression):
  var: Variable
  expr: Expression 
  
#Instructions---------------------------------------------------

"""
Parentheses class
Inherits from Expression
Attributes:
  expr : Expression. The expression inside the parentheses
"""
@dataclass
class Parentheses (Expression):
  expr: Expression

"""
Bynary class
Represents a binary operation
Inherits from Expression
Attributes:
  operator : str. The operator
  left : Expression. The left operand
  rigth : Expression. The right operand
"""
@dataclass
class Binary (Expression):
  operator : str
  left : Expression
  right : Expression
  

"""
Unary class
Represents a unary operation
Inherits from Expression
Attributes:
  operator : str. The operator
  operand : Expression. The operand
"""
@dataclass
class Unary(Expression):
  operator: str
  operand: Expression

"""
Number class
Inherits from Expression
Attributes:
  value : Union [float, int]. The value of the number
"""
@dataclass
class Number (Expression):
  value: Union [float, int]


"""
MakeDot class
Inherits from Visitor
Attributes:
  dot : Digraph. Graphviz Digraph
  sequence : int. The sequence of the nodes, serves to assign a name to each node
Methods:
  name(self) -> str : Returns the name of a node
  visit(self, n : Number) -> str : Visits a Number node
  visit(self, b : Binary) -> str : Visits a Binary node
  visit(self, u : Unary) -> str : Visits a Unary node
  visit(self, p : Parentheses) -> str : Visits a Parentheses node
  generate_dot(self) -> str : Generates the dot file
  
"""
@dataclass
class MakeDot(Visitor):
  #Default values for the nodes and edges
  node_default = {
    'shape': 'box',
    'style': 'filled',
    'fillcolor': 'lightblue',
    'fontcolor': 'black'
  }
  
  edge_default = {
    'arrowhead': 'none'
  }
  
  #Digraph declaration
  dot = Digraph('hoc_ast')
  dot.attr('node', **node_default)
  dot.attr('edge', **edge_default)
  #Sequence of the nodes  
  sequence = 0
  
  def name(self):
    self.sequence += 1 #Increments the sequence
    return f'n{self.sequence}'
  
  def visit(self, a : Assignment):
    name = self.name()
    self.dot.node(name, label = '=')
    var = a.var.accept(self)
    expr = a.expr.accept(self)
    self.dot.edge(name, var)
    self.dot.edge(name, expr)
    return name
  
  def visit(self, v : Variable):
    name = self.name()
    self.dot.node(name, label= f'{v.name}', shape = 'ellipse', color = 'blue') #Creates a node with the name of the Variable node
    return name
    
  def visit(self, n : Number):
    name = self.name() #Obtains the name of the sequence
    self.dot.node(name, str(n.value)) #Creates a node with the name and the value of the Number node
    return name
  
  def visit(self, b : Binary):
    name = self.name()
    self.dot.node(name, label = b.operator, shape = 'circle', color = 'green') #Creates a node with the name and the operator of the Binary node
    self.dot.edge(name, b.left.accept(self), label = 'left') #Creates an edge from the node name to the left node
    self.dot.edge(name, b.right.accept(self), label = 'right') 
    return name
  
  def visit(self, u: Unary):
    name = self.name()
    self.dot.node(name, label = u.operator, color = 'red', shape = 'octagon')
    operand = u.operand.accept(self)
    self.dot.edge(name, operand)
    return name
  
  def visit(self, p : Parentheses):
    name = self.name()
    self.dot.node(name, label = '( )') 
    expr = p.expr.accept(self)
    self.dot.edge(name, expr)
    return name
  
  def generate_dot(self):
    self.dot.save('hoc_ast.dot') #Save the dot file
    #self.dot.render('hoc_ast', format = 'png', view = True)
    return self.dot.source
  
  