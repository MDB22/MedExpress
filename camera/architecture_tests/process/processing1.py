from multiprocessing import Pool


def f(x):
  return x*x

p = Pool(5)
print(p.map(f, [1, 2, 3]))


# maybe use the pool and then grab each of the frames in order
