# -*- coding: utf-8 -*-
"""
Created on Sat May 28 14:19:05 2016

@author: Falaize
"""

from pypHs import pHobj
from utils.tools import myrange
import sympy as sp
from utils.tools import matrix2list


def output_function(phs):
    """
    creates funtion phs.output_function
    """
    if phs.ny() > 0:

        if phs.nx() > 0:
            Vyx = phs.Gx.T*sp.Matrix(phs.dxHd)
        else:
            Vyx = sp.zeros(1, phs.ny())

        if phs.nw() > 0:
            Vyw = phs.Gw.T*sp.Matrix(phs.z)
        else:
            Vyw = sp.zeros(1, phs.ny())

        if phs.ny() > 0:
            Vyu = phs.Jy*sp.Matrix(phs.u)
        else:
            Vyu = sp.zeros(1, phs.ny())

        out = list(Vyx + Vyw + Vyu)
        out = sp.simplify(sp.Matrix(out))
    else:
        out = sp.Matrix(list(list()))

    phs.output = list(out)


def concatenate(phs1, phs2, label=None, path=None):
    """
    Retrun the concatenation of phs1 with phs2 (identical to phs1 + phs2)
    """

    import os

    label = phs1.label + r'_' + phs2.label if label is None else label

    path = os.getcwd() if path is None else path

    phs = pHobj(label, path=path)

    # get storages
    x = phs1.x + phs2.x
    H = phs1.H + phs2.H
    phs.addStorages(x, H)

    # get dissipations
    w = phs1.w + phs2.w
    z = phs1.z + phs2.z
    phs.addDissipations(w, z)

    # get ports
    u = phs1.u + phs2.u
    y = phs1.y + phs2.y
    phs.addPorts(u, y)
    phs.g = phs1.g + phs2.g

    # get parameters
    phs.p = phs1.p + phs2.p
    phs.subs.update(phs1.subs)
    phs.subs.update(phs2.subs)

    # get transformers and gyrators
    phs.connector_u = phs1.connector_u + phs2.connector_u
    phs.connector_y = phs1.connector_y + phs2.connector_y
    phs.connectors = phs1.connectors + phs2.connectors

    # Get structure
    h1 = sp.Matrix.hstack(phs1.Jx, sp.zeros(phs1.nx(), phs2.nx()))
    h2 = sp.Matrix.hstack(sp.zeros(phs2.nx(), phs1.nx()), phs2.Jx)
    Jx = sp.Matrix.vstack(h1, h2)

    h1 = sp.Matrix.hstack(phs1.K, sp.zeros(phs1.nx(), phs2.nw()))
    h2 = sp.Matrix.hstack(sp.zeros(phs2.nx(), phs1.nw()), phs2.K)
    K = sp.Matrix.vstack(h1, h2)

    h11 = phs1.Gx
    h12 = sp.zeros(phs1.nx(), phs2.ny())
    h21 = sp.zeros(phs2.nx(), phs1.ny())
    h22 = phs2.Gx
    h1 = sp.Matrix.hstack(h11, h12)
    h2 = sp.Matrix.hstack(h21, h22)
    Gx = sp.Matrix.vstack(h1, h2)

    h1 = sp.Matrix.hstack(phs1.Jw, sp.zeros(phs1.nw(), phs2.nw()))
    h2 = sp.Matrix.hstack(sp.zeros(phs2.nw(), phs1.nw()), phs2.Jw)
    Jw = sp.Matrix.vstack(h1, h2)

    h1 = sp.Matrix.hstack(phs1.Gw, sp.zeros(phs1.nw(), phs2.ny()))
    h2 = sp.Matrix.hstack(sp.zeros(phs2.nw(), phs1.ny()), phs2.Gw)
    Gw = sp.Matrix.vstack(h1, h2)

    h1 = sp.Matrix.hstack(phs1.Jy, sp.zeros(phs1.ny(), phs2.ny()))
    h2 = sp.Matrix.hstack(sp.zeros(phs2.ny(), phs1.ny()), phs2.Jy)
    Jy = sp.Matrix.vstack(h1, h2)

    phs.addStructure(Jx=Jx, K=K, Gx=Gx, Jw=Jw, Gw=Gw, Jy=Jy)

    phs.Graph.add_edges_from(phs1.Graph.edges(data=True))
    phs.Graph.add_edges_from(phs2.Graph.edges(data=True))
    phs.list_of_edges = phs.Graph.edges(data=True)
    phs.netlist = phs1.netlist + phs2.netlist
    return phs


def copy(phs_origin, phs_copy):
    """
    Copy the content of 'phs_origin' to 'phs_copy'.
    """
    attrs_to_copy = ['x', 'H',
                     'w', 'z',
                     'u', 'y', 'g',
                     'p', 'subs',
                     'connector_u', 'connector_y', 'connectors',
                     'J',
                     'Graph', 'netlist',
                     'config_simu',
                     'label', 'path', 'folders']
    attrs = dir(phs_origin)
    for attr in attrs:
        if attr in attrs_to_copy:
            setattr(phs_copy, attr, getattr(phs_origin, attr))
    phs_copy.addStructure(J=phs_copy.J)


#    # Copy storages
#    phs_copy.x = phs_origin.x
#    phs_copy.H = phs_origin.H
#
#    # Copy dissipations
#    phs_copy.w = phs_origin.w
#    phs_copy.z = phs_origin.z
#
#    # Copy ports
#    phs_copy.u = phs_origin.u
#    phs_copy.y = phs_origin.y
#    phs_copy.g = phs_origin.g
#
#    # Copy parameters
#    phs_copy.p = phs_origin.p
#    phs_copy.subs = phs_origin.subs
#
#    # Copy transformers and gyrators
#    phs_copy.connector_u = phs_origin.connector_u
#    phs_copy.connector_y = phs_origin.connector_y
#    phs_copy.connectors = phs_origin.connectors
#
#    # Copy structure
#    phs_copy.addStructure(J=phs_origin.J)
#
#    # Copy Graph
#    phs_copy.Graph = phs_origin.Graph
#    phs_copy.netlist = phs_origin.netlist


def selfConnect(phs, inds, u1y2=True):

    for i in inds:
        phs.movePort(i, phs.ny()-1)
    Gconnect = phs.J[:-2, -2:]
    if u1y2:
        switch = sp.Matrix([[0, 1], [-1, 0]])
    else:
        switch = sp.Matrix([[0, -1], [1, 0]])

    J = phs.J[:-2, :-2]+Gconnect*switch*Gconnect.T

    expr_u = switch*Gconnect.T*sp.Matrix(phs.dxHd + phs.z + phs.u[:-2])
    for sub in zip(phs.u[-2:], list(expr_u)):
        phs.applySubs({str(sub[0]): sub[1]})

    phs.u = phs.u[:-2]
    phs.y = phs.y[:-2]
    phs.g = phs.g[:-2]

    phs.addStructure(J=J)

    subs = {}
    for dx in phs.dx:
        subs.update({str(dx): 0})
    phs.applySubs(subs)


def stateChange(phs, f):

    x_tilde = sp.symbols(['c'+str(x) for x in phs.x])
    functions_list = [el_f-el_x for (el_f, el_x) in zip(f, x_tilde)]
    g = sp.solve(functions_list, phs.x, dict=True, exclude=phs.p)
    if isinstance(g, list):
        if g.__len__() > 1:
            print "Inverse mapping is not unique. Choose one of:"
            n = 0
            for el_g in g:
                n += 1
                print "\n"
                print str(n)+":"
                print el_g
            n = int(raw_input("Choice?\n"))
            g = g[n-1]
        else:
            g = g[0]
    G = dict(g)
    g = []
    for xx in zip(phs.x, x_tilde):
        if any( xx[0] == k for k in G.keys()):
            g += [G[xx[0]]]
        else:
            g += [xx[1]]
    M = sp.eye(phs.ntot())
    for l in range(phs.nx()):
        for c in range(phs.nx()):
            M[l, c] = f[l].diff(phs.x[c]).doit()
    for sub in zip(phs.x, g):
        M = M.subs(sub[0], sub[1])
    phs.x_old_from_new = g
    phs.J = M*phs.J*M.T
    for n in range(phs.nx()):
        phs.applySubs([(phs.x[n], g[n])])
    phs.x = x_tilde
    for n in range(phs.nxl()):
        phs.diagQ[n] = phs.H.diff(phs.x[n], 2)


def linearVariableChange(phs, index, gain):

    if index < phs.nx():
        n = index
        f = [x for x in phs.x]
        f[n] = f[n]/gain
        phs.stateChange(f)
        phs.applySubs()

    elif (index >= phs.nx()) & (index < phs.nx()+phs.nw()):
        n = index-phs.nx()
        old_symb = phs.w[n]
        new_symb = sp.symbols('c'+str(old_symb))
        old_as_func_of_new = gain*new_symb
        phs.z[n] = gain*phs.z[n].subs(old_symb, old_as_func_of_new)
        phs.w[n] = new_symb
        if n < phs.nwl():
            phs.diagR[n] = phs.z[n].diff(phs.w[n]).doit()
        M = sp.eye(phs.ntot())
        M[index, index] = gain**-1
        phs.applySubs([(old_symb, old_as_func_of_new)])
        phs.J = M*phs.J*M.T

    elif (index >= phs.nx()+phs.nw()) & (index < phs.ntot()):
        n = index-phs.nx()-phs.nw()
        old_symb = phs.u[n]
        M = sp.eye(phs.ntot())
        M[index, index] = gain**-1
        phs.J = M*phs.J*M.T
        phs.diagG[n] = phs.diagG[n]*gain
        phs.applySubs()


def Canonize(phs, nonlinearize=False):

    # for each line of J
    list_ind = range(phs.nx()+phs.nw())
    list_ind.reverse()
    for l in list_ind:
        # analyse element c to find nonzeros
        indices_nonzeros = []
        for c in range(phs.ntot()):
            element_of_J = phs.J[l, c]
            if element_of_J != sp.sympify(0):
                indices_nonzeros.append(c)
        # for each nonzero element
        for c in indices_nonzeros:
            # if J[l,c] is not canonic
            if sp.Abs(phs.J[l, c]) != sp.sympify(1):
                gain = phs.J[l, c]
                # get indices of connected edges
                indices_connections = indices_nonzeros
                indices_connections.remove(c)
                # For each connected element
                phs.linearVariableChange(l, gain)
                for i in indices_connections:
                    # replace with gain = 1/J[l,c]
                    if sp.Abs(phs.J[l, i]) != sp.sympify(1):
                        phs.linearVariableChange(i, gain**-1)
                # replace element l

    if nonlinearize:
        list_ind = range(phs.nxl())
        list_ind.reverse()
        while list_ind:
            n = list_ind.pop()
            list_symbols = list(sp.sympify(phs.diagQ[n]).free_symbols)
            if any( any(el == p for p in phs.p)
                    for el in list_symbols):
                phs.moveStateLinToNLin(n)
                list_ind = [el-1 for el in list_ind]
        list_ind = range(phs.nwl())
        list_ind.reverse()
        while list_ind:
            n = list_ind.pop()
            list_symbols = list(sp.sympify(phs.diagR[n]).free_symbols)
            test_par = any( any(el == p for p in phs.p)
                            for el in list_symbols)
            list_symbols = list(sp.sympify(phs.diagR[n]).free_symbols)
            test_state = any( any(el == x for x in phs.x)
                              for el in list_symbols)
            if any([test_state, test_par]):
                phs.moveDissLinToNLin(n)
                list_ind = [el-1 for el in list_ind]


def moveJcolnrow(phs, indi, indf):
    new_indices = myrange(phs.ntot(), indi, indf)
    J = phs.J[new_indices, new_indices]
    phs.addStructure(J=J)


def move_stor(phs, indi, indf):
    new_indices = myrange(phs.nx(), indi, indf)
    phs.x = [phs.x[el] for el in new_indices]
    moveJcolnrow(phs, indi, indf)
    phs.build(print_latex=False)


def move_diss(phs, indi, indf):
    new_indices = myrange(phs.nw(), indi, indf)
    phs.w = [phs.w[el] for el in new_indices]
    phs.z = [phs.z[el] for el in new_indices]
    moveJcolnrow(phs, phs.nx()+indi, phs.nx()+indf)
    phs.build(print_latex=False)


def move_port(phs, indi, indf):
    new_indices = myrange(phs.ny(), indi, indf)
    phs.u = [phs.u[el] for el in new_indices]
    phs.y = [phs.y[el] for el in new_indices]
    moveJcolnrow(phs, phs.nx()+phs.nw()+indi, phs.nx()+phs.nw()+indf)
    phs.build(print_latex=False)


def split_separate(phs):
    """
    """

    from utils.structure import move_stor, move_diss
    # split storage part
    i = 0
    for _ in range(phs.nx()):
        hess_line = list(phs.hess[i, :].T)
        # remove i-th element
        hess_line.pop(i)
        # if other elements are all 0
        if all( el is sp.sympify(0) for el in hess_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of states vector
            move_stor(phs, i, phs.nx())
    # number of separate components
    phs.nxs = i
    # number of non-separate components
    phs.nxns = phs.nx()-i
    # split dissipative part
    i = 0
    for _ in range(phs.nw()):
        Jacz_line = list(phs.Jacz[i, :].T)
        # remove i-th element
        Jacz_line.pop(i)
        # if other elements are all 0
        if all( el is sp.sympify(0) for el in Jacz_line):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of variables vector
            move_diss(phs, i, phs.nw())
    # number of separate components
    phs.nws = i
    # number of non-separate components
    phs.nwns = phs.nw()-i


def split_linear(phs):
    """
    """
    from utils.structure import move_stor, move_diss
    if not hasattr(phs, 'dxH'):
        phs.build()
    # split storage part
    i = 0
    for _ in range(phs.nx()):
        hess_line = list(phs.hess[i, :].T)
        # init line symbols
        line_symbols = set()
        # collect line symbols
        for el in hess_line:
            line_symbols = line_symbols.union(el.free_symbols)
        # if symbols are not states
        if not any( el in line_symbols for el in phs.x):
            # do nothing and increment counter
            i += 1
        else:
            # move the element at the end of states vector
            move_stor(phs, i, phs.nx())
    # number of linear components
    phs.nxl = i
    # number of non-separate components
    phs.nxnl = phs.nx()-i
    # split dissipative part
    i = 0
    for _ in range(phs.nw()):
        Jacz_line = list(phs.Jacz[i, :].T)
        # init line symbols
        line_symbols = set()
        # collect line symbols
        for el in Jacz_line:
            line_symbols = line_symbols.union(el.free_symbols)
        # if symbols are not dissipation variables
        if not any( el in line_symbols for el in phs.w):
            # do nothing and increment counter
            i += 1
        else:
            # move the element to end of dissipation variables vector
            move_diss(phs, i, phs.nw())
    # number of linear components
    phs.nwl = i
    # number of non-separate components
    phs.nwnl = phs.nw()-i


def reduce_linear_dissipations(phs):
    if not hasattr(phs, 'nwl'):
        split_linear(phs)
    from utils.calculus import compute_jacobian
    phs.zl = compute_jacobian(phs.z[:phs.nwl], phs.w[:phs.nwl])
    Kl = phs.K[:, :phs.nwl]
    Knl = phs.K[:, phs.nwl:]
    Gl = phs.Gw[:phs.nwl, :]
    Gnl = phs.Gw[phs.nwl:, :]
    Jll = phs.Jw[:phs.nwl, :phs.nwl]
    Jlnl = phs.Jw[:phs.nwl, phs.nwl:]
    Jnlnl = phs.Jw[phs.nwl:, phs.nwl:]
    iDw = sp.eye(phs.nwl)-Jll*phs.zl
    Dw = iDw.inv()
    Ktot = sp.Matrix.vstack(-Kl, -Jlnl.T, -Gl.T)
    Rtot = Ktot*phs.zl*Dw*Ktot.T
    phs.w = phs.w[phs.nwl:]
    phs.z = phs.z[phs.nwl:]
    if phs.nx() > 0:
        hstack1 = sp.Matrix.hstack(phs.Jx, -Knl, phs.Gx)
    else:
        hstack1 = sp.zeros(phs.nx(), phs.ntot())
    if phs.nw() > 0:
        hstack2 = sp.Matrix.hstack(Knl.T, Jnlnl, Gnl)
    else:
        hstack2 = sp.zeros(phs.nw(), phs.ntot())
    if phs.ny() > 0:
        hstack3 = sp.Matrix.hstack(-phs.Gx.T, -Gnl.T, phs.Jy)
    else:
        hstack3 = sp.zeros(phs.ny(), phs.ntot())
    phs.nwl = 0
    J = sp.Matrix.vstack(hstack1, hstack2, hstack3)
    phs.addStructure(J=J-Rtot)
    phs.build()
