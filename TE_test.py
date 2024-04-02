import pyinform
import numpy as np


source_node = np.array([2*x**2 + 4*x + 10 for x in range(100)])
dest_node = np.array([2*(x-1)**2 + 4*(x-1) + 10 for x in range(100)])

print(pyinform.transfer_entropy(source_node, dest_node, k=1))


