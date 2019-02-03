#!/usr/bin/env python
# -*- coding: utf-8 -*-
from javalang.tree import (BinaryOperation, CatchClause, DoStatement,
                           ForStatement, IfStatement, Node, SwitchStatement,
                           TernaryExpression, WhileStatement)


def complexity(body):
    comp = 0
    for expr in body:
        comp += _count_recursive(expr)
    return comp


def _count_recursive(expr, parent=None, comp=0, nesting=0):
    # pylint: disable=W0612,W0613
    new_comp = _calc_for_expression(expr, parent, nesting)
    new_nesting = nesting
    if isinstance(expr, Node):
        inc_neasting = _increments_nesting(expr, parent)
        if inc_neasting:
            new_nesting += 1
        for child in expr.children:
            new_comp += _count_recursive(child, expr, new_comp, new_nesting)
        if inc_neasting:
            new_nesting -= 1
    if isinstance(expr, list):
        for child in expr:
            new_comp += _count_recursive(child, expr, new_comp, new_nesting)
    return new_comp


def _calc_for_expression(expr, parent, nesting):
    if isinstance(expr, BinaryOperation):
        operator = expr.operator
        if operator in ("||", "&&"):
            return 1
    if isinstance(expr, TernaryExpression):
        return 1
    if isinstance(expr, IfStatement):
        if _is_elseif(expr, parent):
            count = 1
            if _has_else(expr):
                count += 1
            return count
        count = 1 + nesting
        if _has_else(expr):
            count += 1
        return count
    if _is_loop(expr) or isinstance(expr, (SwitchStatement, CatchClause)):
        return 1 + nesting
    return 0


def _increments_nesting(expr, parent):
    is_elseif = _is_elseif(expr, parent)
    if (isinstance(expr, IfStatement) and not is_elseif) or isinstance(
            expr, (SwitchStatement, CatchClause)) or _is_loop(expr):
        return True
    return False


def _is_loop(expr):
    if isinstance(expr, (DoStatement, ForStatement, WhileStatement)):
        return True
    return False


def _has_else(if_statement):
    if if_statement.else_statement and not isinstance(
            if_statement.else_statement, IfStatement):
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
