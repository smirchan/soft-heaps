from visualization import SelectVisualizer
from linear_select import select, partition
import numpy as np

lst = np.random.permutation(list(range(1, 100)))
k = 1

viz = SelectVisualizer(sheap_mode=True)
select(k, lst, 1, viz=viz)
viz.viz()