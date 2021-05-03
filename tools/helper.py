import math
import numpy as np
from numba import prange, njit
from numba import cuda
from numba.cuda.random import create_xoroshiro128p_states, xoroshiro128p_uniform_float32

"""
Loss = sum_i(sum_j(A[i,j] * abs(i-j)/(m^2)))
"""
def loss(matrix):
    # return loss_gpu(matrix) # use GPU
    return loss_cpu(matrix) # use CPU

@njit
def loss_cpu(elements):
    """ 
    This file directly optimize this loss function.
    calculate the whole matrix
    @return at the scale: Loss / 2
    """
    ret = 0
    l = elements.shape[0]
    _l_1 = 1.0/(l*l)
    for i in range(l):
        for j in range(i):
            if elements[i, j] > 0:
                ret += (i-j) * _l_1 * elements[i, j]  # here because j<i, we can safely ommit abs() for speed.
    return ret

@cuda.jit
def _loss_gpu(matrix, ret):
    x, y = cuda.grid(2)
    if x<matrix.shape[0] and y<matrix.shape[1]: # Important: Don't use early return in CUDA functions, will cause Memory Error. Use cuda-memcheck to check memory.
        if y<x: # only compute half of the matrix
            if matrix[x, y] > 0:
                loss = (x-y) * ret[1] * matrix[x, y]
                cuda.atomic.add(ret, 0, loss)
    
def loss_gpu(matrix):
    """ same as loss(), but run on GPU """
    ret = np.array([0.0, 1/(matrix.shape[0]*matrix.shape[0])], dtype=np.float64)
    threadsperblock = (16, 16)
    blockspergrid_x = math.ceil(matrix.shape[0] / threadsperblock[0])
    blockspergrid_y = math.ceil(matrix.shape[1] / threadsperblock[1])
    blockspergrid = (blockspergrid_x, blockspergrid_y)
    _loss_gpu[blockspergrid, threadsperblock](matrix, ret)
    return ret[0]
