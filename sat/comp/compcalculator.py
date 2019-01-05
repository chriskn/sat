#!/usr/bin/env python
# -*- coding: utf-8 -*-
from javalang.tree import (BinaryOperation, BlockStatement, CatchClause,
                           ConstructorDeclaration, DoStatement, ForStatement,
                           IfStatement, Literal, MemberReference,
                           MethodDeclaration, Node, SwitchStatement,
                           TernaryExpression, WhileStatement)


def complexity(body):
    compl = 0
    for expr in body:
        c = _count_recursive(expr)
        compl += c
    return compl


def _count_recursive(expr, parent=None, count=0, nesting=0):
    new_count = _calc_for_expression(expr, parent, nesting)
    new_nesting = nesting
    if isinstance(expr, Node):
        inc_neasting = _increments_nesting(expr, parent)
        if inc_neasting:
            new_nesting += 1
        for child in expr.children:
            new_count += _count_recursive(child, expr,
                                          new_count, new_nesting)
        if inc_neasting:
            new_nesting -= 1
    if isinstance(expr, list):
        for child in expr:
            new_count += _count_recursive(child, expr,
                                          new_count, new_nesting)
    return new_count


def _calc_for_expression(expr, parent, nesting):
    if isinstance(expr, BinaryOperation):
        op = expr.operator
        if op == "||" or op == "&&":
            return 1
    if isinstance(expr, TernaryExpression):
        return 1
    if isinstance(expr, SwitchStatement):
        return 1+nesting
    if isinstance(expr, CatchClause):
        return 1+nesting
    if isinstance(expr, IfStatement):
        if _is_elseif(expr, parent):
            count = 1
            if _has_else(expr):
                count += 1
            return count
        count = 1+nesting
        if _has_else(expr):
            count += 1
        return count
    if isinstance(expr, WhileStatement):
        return 1+nesting
    if isinstance(expr, ForStatement):
        return 1+nesting
    if isinstance(expr, DoStatement):
        return 1+nesting
    return 0


def _increments_nesting(expr, parent):
    is_elseif = _is_elseif(expr, parent)
    if (isinstance(expr, IfStatement) and not is_elseif) or isinstance(expr, SwitchStatement) or isinstance(expr, CatchClause) or isinstance(expr, ForStatement) or isinstance(expr, WhileStatement) or isinstance(expr, DoStatement):
        return True
    return False


def _has_else(if_statement):
    if if_statement.else_statement and not isinstance(if_statement.else_statement, IfStatement):
        return True
    return False


def _is_elseif(expr, parent):
    return isinstance(parent, IfStatement) and parent.else_statement == expr

# def _is_nullvalue(expr):
#    if isinstance(expr, Literal):
#        if expr.value == "null":
#            return True
#    return False

# def _is_nullcheck(if_statement):
#    cond = if_statement.condition
#    if isinstance(cond, BinaryOperation):
#        op = cond.operator
#        left = cond.operandl
#        right = cond.operandr
#        if (op == "!=") and (_is_nullvalue(left) or _is_nullvalue(right)):
#            return True
#    return False

# def _is_elvis(if_statement):
#    if _is_nullcheck(if_statement):
#        cond = if_statement.condition
#        left = cond.operandl
#        right = cond.operandr
#        varibale = None
#        if isinstance(left, MemberReference):
#            varibale = left
#        elif isinstance(right, MemberReference):
#            varibale = right
#        else:
#            return False
#        childblocks = [block for block in if_statement.children if isinstance(block, BlockStatement)]
#        if not childblocks:
#            return False
#        blockstatements = childblocks[0].statements
#        if _uses_variable(blockstatements, varibale.member):
#            return True
#    return False

# def _uses_variable(statements, variable_name):
#     for st in statements:
#         if variable_name in st.expression.children:
#             return True
#     return False
