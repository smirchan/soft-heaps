from visualization import SelectVisualizer
from linear_select import select, partition
import numpy as np

np.random.seed(0)
lst = np.random.permutation(list(range(1, 101)))
k = 100

viz = SelectVisualizer(sheap_mode=True)
select(k, lst, 4, viz=viz)
viz.viz()