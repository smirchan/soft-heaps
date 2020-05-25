import random
from sheap_simplified import SoftHeap, null

def randlist(n):
	return [ random.random() for i in range(n) ]

def randperm(n):
	return random.sample(list(range(n)),n)

def build(lst, eps):
	P = SoftHeap(eps)
	for it in lst:
		P.insert(it)
	return P

def extract(P):
	lst = [];
	while P.heap != null:
		lst.append(P.find_min()[0].key)
		P.delete_min()
	return lst
		
def sort(lst, eps):
	print(lst)
	P = build(lst, eps)
	lst1 = extract(P)
	if P.eps == 0:
		for i in range(1,len(lst)):
			if lst1[i]<lst1[i-1]:
				print("BUG!!!")
				raise BUG()
	print(lst1)
	print(" ")
	return lst1

sort(randperm(30), 0)
sort(randperm(30), 0.1)
sort(randperm(30), 0.5)

P=build(randperm(100), 0)
Q=build(randperm(200), 0)
P.meld(Q)
print(extract(P))