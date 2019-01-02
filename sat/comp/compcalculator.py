#!/usr/bin/env python
# -*- coding: utf-8 -*-
from javalang.tree import ConstructorDeclaration
from javalang.tree import MethodDeclaration
from javalang.tree import Node
from javalang.tree import IfStatement
from javalang.tree import WhileStatement
from javalang.tree import ForStatement
from javalang.tree import DoStatement
from javalang.tree import TernaryExpression
from javalang.tree import BinaryOperation
from javalang.tree import SwitchStatement
from javalang.tree import CatchClause
from javalang.tree import Literal

def complexity(body):
        compl = 0
        for expr in body:
            c = _count_recursive(expr)
            compl += c
        return compl

def _count_recursive(expr, parent=None, count=0, nesting=0):
   new_count = _calc_for_statement(expr, parent, nesting)
   new_nesting = nesting
   if isinstance(expr, Node):
       inc_neasting = _increments_nesting(expr, parent)
       if inc_neasting:
           new_nesting += 1
           print("increase neasting to "+str(new_nesting)+" for "+str(type(expr)))
       for child in expr.children:
           new_count += _count_recursive(child, expr,
                                              new_count, new_nesting)
       if inc_neasting:
           new_nesting -= 1
   if isinstance(expr, list):
       for child in expr:
           new_count += _count_recursive(child, expr, 
                                              new_count, new_nesting)
   # print(str(type(expr))+" "+str(new_count))
   return new_count

def _calc_for_statement(expr, parent, nesting):
   if isinstance(expr, BinaryOperation):
       op = expr.operator
       if op == "||" or op == "&&":
           print("returning 1 for Binary")
           return 1
   if isinstance(expr, TernaryExpression):
       print("returning 1 for Ternary")
       return 1
   if isinstance(expr, SwitchStatement):
       print("returning "+str(1+nesting)+" for Switch")
       return 1+nesting
   if isinstance(expr, CatchClause):
       print("returning "+str(1+nesting)+" for Catch")
       return 1+nesting
   if isinstance(expr, IfStatement):
       count = 0
       if _is_nullcheck(expr):
           print("returning 0 for nullcheck")
           return 0
       if _is_elseif(expr,parent):
           print("returning 1 for else if")
           count = 1
           if expr.else_statement and not isinstance(expr.else_statement, IfStatement):
               count += 1
               print("adding 1 for else to else if")
           return count
       count = 1+nesting
       if expr.else_statement and not isinstance(expr.else_statement, IfStatement):
           count += 1
           print("adding 1 for else")
       print("returning "+str(count)+" for If")
       return count
   if isinstance(expr, WhileStatement):
       print("returning "+str(1+nesting)+" for While")
       return 1+nesting
   if isinstance(expr, ForStatement):
       print("returning "+str(1+nesting)+" for For")
       return 1+nesting
   if isinstance(expr, DoStatement):
       print("returning "+str(1+nesting)+" for Do")
       return 1+nesting
   return 0

def _is_nullcheck(if_statement):
   cond = if_statement.condition
   if isinstance(cond, BinaryOperation):
       op = cond.operator
       left = cond.operandl
       right = cond.operandr
       if (op == "!=") and (_is_nullvalue(left) or _is_nullvalue(right)):
           return False #When is a null check ignored
   return False

def _is_nullvalue(expr):
   if isinstance(expr, Literal):
       if expr.value == "null":
           return True
   return False

def _increments_nesting(expr,parent):
   is_elseif = _is_elseif(expr, parent)
   if (isinstance(expr, IfStatement) and not is_elseif)  or isinstance(expr, SwitchStatement) or isinstance(expr, CatchClause) or isinstance(expr, ForStatement) or isinstance(expr, WhileStatement) or isinstance(expr, DoStatement):
       return True
   return False

def _is_elseif(expr, parent):
   return isinstance(parent, IfStatement) and parent.else_statement == expr