from sheap_simplified import SoftHeap
import functools
import timeit
import math
import numpy as np
import matplotlib.pyplot as plt

def partition(pivot, lst):
	L = []
	R = []
	for elem in lst:
		if elem < pivot:
			L.append(elem)
		elif elem > pivot:
			R.append(elem)

	return (L, R)

def select(k, lst, method, viz=None):
	# viz should be a SoftHeapVisualization object
	if viz:
		viz.select_record(k, lst, info="input")

	n = len(lst)
	if k > n or n < 1:
		raise Exception('Invalid k value')

	# Base Case
	if n <= 3:
		lst.sort()
		return lst[k - 1]

	# # Sanity check
	# eps = 0

	# Simple, using Chazelle's constant value for eps
	if method == 1:
		delete_min_calls = max(1, math.floor(n/3))
		eps = 1/3
	# Choose delete_min_calls and eps in ways that leverage soft heap corruption properties
	# to speed up select algorithm
	elif method == 2:
		# Holds delete_min_calls constant, varies eps
		r = k/n
		delete_min_calls = max(1, math.floor(n/3))
		if r >= 1/3:
			eps = r - 1/3
		else:
			eps = 1/10
	elif method == 3:
		# Varies delete_min_calls and eps
		r = k/n
		if r >= 2/3:
			delete_min_calls = max(1, math.floor(2 * n/3))
			eps = r - 2/3
		elif r >= 1/3:
			delete_min_calls = max(1, math.floor(n/3))
			eps = r - 1/3
		else:
			delete_min_calls = k
			eps = r
	elif method == 4:
		# Varies delete_min_calls and eps, tune choice of soft heap (min vs. max)
		r = k/n
		max_heap = False

		if r > 1/2:
			k_h = n - k + 1
			r_h = k_h/n
			max_heap = True
		else:
			k_h = k
			r_h = r
			max_heap = False

		if r_h >= 1/3:
			delete_min_calls = max(1, math.floor(n/3))
			eps = r_h - 1/3
		else:
			delete_min_calls = k_h
			eps = r_h

	sheap = SoftHeap(eps)
	if method == 4 and max_heap:
		lst_h = [-e for e in lst]
		for elem in lst_h:
			sheap.insert(elem)
	else:
		for elem in lst:
			sheap.insert(elem)

	max_seen = float('-inf')
	for i in range(delete_min_calls):
		ptr, key = sheap.find_min()
		elem = ptr.key
		sheap.delete_min()
		if elem > max_seen:
			max_seen = elem

	if method == 4 and max_heap:
		max_seen = -max_seen

	L, R = partition(max_seen, lst)
	if viz:
		viz.select_record(max_seen, L, R, info="partition")

	if len(L) == k - 1:
		return max_seen
	elif len(L) >= k:
		return select(k, L, method, viz=viz)
	else:
		return select(k - len(L) - 1, R, method, viz=viz)

# Run experiment on select k execution time for different values of k on t lists of size 10000
# Using three tuning methods for choosing delete_min calls/corruption parameter within select k
def run_exp1(t):
	ks = list(range(0, 10001, 1000))
	ks[0] = 1
	
	data = {'x': ks, 'y1': [], 'y2': [], 'y3': [], 'y4': []}
	
	# Average execution time over t random permutations/orderings of a list of size 10000
	for i in range(t):
		# print('i', i)
		lst = np.random.permutation(list(range(1, 10001)))

		y1 = []
		y2 = []
		y3 = []
		y4 = []

		for k in ks:
			# print('k', k)
			# Average execution time of select k on lst over 100 run
			t = timeit.timeit(functools.partial(select, k, lst, 1), number=10)/10
			y1.append(t)
			t = timeit.timeit(functools.partial(select, k, lst, 2), number=10)/10
			y2.append(t)
			t = timeit.timeit(functools.partial(select, k, lst, 3), number=10)/10
			y3.append(t)
			t = timeit.timeit(functools.partial(select, k, lst, 4), number=10)/10
			y4.append(t)

		data['y1'].append(y1)
		data['y2'].append(y2)
		data['y3'].append(y3)
		data['y4'].append(y4)

	data['y1'] = np.mean(np.array(data['y1']), axis=0)
	data['y2'] = np.mean(np.array(data['y2']), axis=0)
	data['y3'] = np.mean(np.array(data['y3']), axis=0)
	data['y4'] = np.mean(np.array(data['y4']), axis=0)
	# print(data['y1'].shape[0] == len(ks))

	return data

def make_plot1(data, filename):
	fig, ax = plt.subplots()
	for i in range(1, 5):
		ax.plot(data['x'], data['y' + str(i)])
	ax.set_xlabel('Rank of Element to Select - k')
	ax.set_ylabel('Average Execution Time of Select (seconds)')
	ax.set_title('Average Execution Time of Select (seconds)')
	lgd = plt.legend(['No tuning', 'Tuning eps', 'Tuning delete_min calls and eps', 'Tuning delete_min_calls, eps, and soft heap type'], title='Tuning Method', loc='center left', bbox_to_anchor=(1, 0.5))
	plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight', format='png')

# Run experiment on select k execution time for different list sizes (defaults to selecting minimum)
# Using three tuning methods for choosing delete_min calls/corruption parameter within select k
def run_exp2(p=None):
	lst_sizes = list(range(0, 10001, 1000))
	lst_sizes[0] = 1
	
	data = {'x': lst_sizes, 'y1': [], 'y2': [], 'y3': [], 'y4': []}
	
	for n in lst_sizes:
		lst = np.random.permutation(list(range(1, n + 1)))
		if not p:
			k = 1
		else:
			k = math.ceil(n * p)
		# print(n, k)

		t = timeit.timeit(functools.partial(select, k, lst, 1), number=10)/10
		data['y1'].append(t)
		t = timeit.timeit(functools.partial(select, k, lst, 2), number=10)/10
		data['y2'].append(t)
		t = timeit.timeit(functools.partial(select, k, lst, 3), number=10)/10
		data['y3'].append(t)
		t = timeit.timeit(functools.partial(select, k, lst, 4), number=10)/10
		data['y4'].append(t)

	return data

def make_plot2(data, title, filename):
	fig, ax = plt.subplots()
	for i in range(1, 5):
		ax.plot(data['x'], data['y' + str(i)])
	ax.set_xlabel('List size - n')
	ax.set_ylabel('Average Execution Time of Select')
	ax.set_title(title)
	lgd = plt.legend(['No tuning', 'Tuning eps', 'Tuning delete_min calls and eps', 'Tuning delete_min_calls, eps, and soft heap type'], title='Tuning Method', loc='center left', bbox_to_anchor=(1, 0.5))
	plt.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight', format='png')

def main():
	# Sanity check that select is working correctly
	k = 10000
	lst = np.random.permutation(list(range(1, 10001)))
	# lst = list(range(1, 10001))

	print('No tuning')
	print(select(k, lst, 1))
	t = timeit.timeit(functools.partial(select, k, lst, 1), number=10)/10
	print('Execution time:', t)
	print('')

	print('Tuning eps')
	print(select(k, lst, 2))
	t = timeit.timeit(functools.partial(select, k, lst, 2), number=10)/10
	print('Execution time:', t)
	print('')

	print('Tuning delete_min calls and eps')
	print(select(k, lst, 3))
	t = timeit.timeit(functools.partial(select, k, lst, 3), number=10)/10
	print('Execution time:', t)
	print('')

	print('Tuning delete_min calls and eps, tune choice of soft heap')
	print(select(k, lst, 4))
	t = timeit.timeit(functools.partial(select, k, lst, 4), number=10)/10
	print('Execution time:', t)
	print('')

	# # Runs experiment on select k, varying methods for choosing selection parameters affecting the pivot
	# data = run_exp1(t=1)
	# make_plot1(data, 'exp1.png')

	# data = run_exp2()
	# make_plot2(data, 'Average Execution Time of Select for Minimum Element (seconds)', 'exp2_min.png')

	# data = run_exp2(p=1/3)
	# make_plot2(data, 'Average Execution Time of Select for Rank n/3 Element (seconds)', 'exp2_third.png')

	# data = run_exp2(p=1/2)
	# make_plot2(data, 'Average Execution Time of Select for Median Element (seconds)', 'exp2_med.png')

	# data = run_exp2(p=2/3)
	# make_plot2(data, 'Average Execution Time of Select for Rank 2n/3 Element (seconds)', 'exp2_twothirds.png')

	# data = run_exp2(p=1)
	# make_plot2(data, 'Average Execution Time of Select for Maximum Element (seconds)', 'exp2_max.png')

if __name__ == '__main__':
	main()