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

def select(k, lst, tune_dmcs, tune_eps):
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
	if not tune_dmcs and not tune_eps:
		delete_min_calls = max(1, math.floor(n/3))
		eps = 1/3
	# Choose delete_min_calls and eps in ways that leverage soft heap corruption properties
	# to speed up select algorithm
	elif not tune_dmcs:
		# Holds delete_min_calls constant, varies eps
		r = k/n
		delete_min_calls = max(1, math.floor(n/3))
		if r > 1/3:
			eps = r - 1/3
		else:
			eps = 1/10
	else:
		# Varies delete_min_calls and eps
		r = k/n
		if r >= 2/3:
			delete_min_calls = max(1, math.floor(2 * n/3))
			eps = r - 2/3
			# delete_min_calls = max(1, math.floor(k/2))
			# eps = r - ((k/2)/n)
		elif r >= 1/3:
			delete_min_calls = max(1, math.floor(n/3))
			eps = r - 1/3
		else:
			delete_min_calls = k
			eps = r

	sheap = SoftHeap(eps)
	for elem in lst:
		sheap.insert(elem)

	max_seen = float('-inf')
	for i in range(delete_min_calls):
		ptr, key = sheap.find_min()
		elem = ptr.key
		sheap.delete_min()
		if elem > max_seen:
			max_seen = elem

	L, R = partition(max_seen,lst)

	if len(L) == k - 1:
		return max_seen
	elif len(L) >= k:
		return select(k, L, tune_dmcs, tune_eps)
	else:
		return select(k - len(L) - 1, R, tune_dmcs, tune_eps)

def run_experiment():
	ks = list(range(0, 10001, 1000))
	ks[0] = 1
	
	data = {'x': ks, 'y1': [], 'y2': [], 'y3': []}
	
	t = 1
	# Average execution time over t random permutations/orderings of a list of numbers [1,...,1000]
	for i in range(t):
		# print('i', i)
		lst = np.random.permutation(list(range(1, 10001)))

		y1 = []
		y2 = []
		y3 = []

		for k in ks:
			# print('k', k)
			# Average execution time of select k on lst over 100 runs
			t = timeit.timeit(functools.partial(select, k, lst, False, False), number=100)/100
			y1.append(t)
			t = timeit.timeit(functools.partial(select, k, lst, False, True), number=100)/100
			y2.append(t)
			t = timeit.timeit(functools.partial(select, k, lst, True, True), number=100)/100
			y3.append(t)

		data['y1'].append(y1)
		data['y2'].append(y2)
		data['y3'].append(y3)

	data['y1'] = np.mean(np.array(data['y1']), axis=0)
	data['y2'] = np.mean(np.array(data['y2']), axis=0)
	data['y3'] = np.mean(np.array(data['y3']), axis=0)
	# print(data['y1'].shape[0] == len(ks))

	return data

def make_plot(data):
	fig, ax = plt.subplots()
	for i in range(1, 4):
		ax.plot(data['x'], data['y' + str(i)])
	ax.set_xlabel('k')
	ax.set_ylabel('Average Execution Time of Select (seconds)')
	ax.set_title('Average Execution Time of Select (seconds) vs. k')
	lgd = plt.legend(['No tuning', 'Tuning eps', 'Tuning delete_min calls and eps'], title='Tuning Method', loc='center left', bbox_to_anchor=(1, 0.5))
	plt.savefig('select_exps.png', bbox_extra_artists=(lgd,), bbox_inches='tight', format='png')

def main():
	# Sanity check that select is working correctly
	k = 1
	lst = np.random.permutation(list(range(1, 10001)))
	print('No tuning')
	print(select(k, lst, False, False))
	print('Tuning eps')
	print(select(k, lst, False, True))
	print('Tuning delete_min calls and eps')
	print(select(k, lst, True, True))

	# # Runs experiment on linear selection parameter tuning methods
	# data = run_experiment()
	# make_plot(data)

if __name__ == '__main__':
	main()