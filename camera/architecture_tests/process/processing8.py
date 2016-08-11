from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
  return x*x

pool = Pool(processes=4)


print pool.map(f, range(10))
               
res = pool.appy_async(f, (20,))

