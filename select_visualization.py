from visualization import SelectVisualizer
from linear_select import select, partition
import numpy as np

A = np.random.permutation(list(range(1, 100)))
k=17

viz = SelectVisualizer(sheap_mode=True)
select(k, A, False, False, viz=viz)
viz.viz()