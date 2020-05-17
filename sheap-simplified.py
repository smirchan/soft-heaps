""" Python implementation of "Soft Heaps Simplified"
 	by Haim Kaplan, Robert E. Tarjan and Uri Zwick.
 	Adapted from code (c) Haim Kaplan, Robert E. Tarjan and Uri Zwick.
"""

INF = float('inf')
T = INF
# T = 2

class Item:

	def __init__(e,it):
		e.key = it
		e.next = e
		
class Node:
	pass

# Global null node
null = Node()
null.set = null
null.key = INF
null.rank = INF
null.left = null
null.right = null
null.next = null


def defill(x):
	# Merge x's smaller child into it; and keep doing that until
	# you've merged in a leaf
	fill(x)
	# If x.rank is even and greater than T, do it again
	if x.rank > T and x.rank % 2 == 0 and x.left != null:
		fill(x)

def fill(x):
	# Ensure x.left has the smaller key of x's two children
	if x.left.key > x.right.key:
		x.left, x.right = x.right, x.left
	# Merge x.left into x (x may or may not already have items)
	x.key = x.left.key
	if x.set == null:
		x.set = x.left.set
	else:
		x.set.next, x.left.set.next = x.left.set.next, x.set.next
	x.left.set = null
	# If x.left is now a leaf, destroy it and move x.right in its place
	if x.left.left == null: 
		x.left = x.right
		x.right = null
	# Otherwise, call defill on it
	else:
		defill(x.left)
		
def make_heap():
	return null

def find_min(H):
	# Assume findable order; H is the root with minimum key,
	# H.set.next is its first item
	return (H.set.next, H.key)

def rank_swap(H):
	# Swap H and H.next if H.next has a smaller rank
	x = H.next
	if H.rank <= x.rank: 
		return H
	else:
		H.next = x.next
		x.next = H 
		return x

def key_swap(H):
	# Swap H and H.next if H.next has a smaller rank
	x = H.next
	if H.key <= x.key: 
		return H
	else:
		H.next = x.next
		x.next = H
		return x

def delete_min(H):
	# Assume findable order; H is the root with minimum key
	# and H.set.next is its first item
	e = H.set.next
	# If there's another item, wire out the first element and
	# return it
	if e.next != e: 
		H.set.next = e.next
		return H
	# If there's only one item
	else:
		# Delete that item
		H.set = null
		k = H.rank
		# If H is a leaf, destroy H and point it to the next tree
		if H.left == null: 
			L = H.next
			H = L
		# If H is not a leaf, raise small child (recursively),
		# and if it has an even rank beyond T, do this again
		else:
			defill(H)

		# Restore findable order
		return reorder(H, k)
  
def reorder(H, k):
	# Implemented recursively: while H.next has rank < k, 
	# swap H with H.next if it's lower --> sorted by rank;
	# walking backwards, swap H with H.next if H.next has
	# smaller key --> findable order
	if H.next.rank < k: 
		H = rank_swap(H)
		H.next = reorder(H.next, k)
	return key_swap(H)

def insert(e, H):
	# Assuming H is in findable order, make H into meldable order,
	# meldable_insert it with the new root
	# The result is in meldable order, so convert it to findable order
	return key_swap(meldable_insert(make_root(e), rank_swap(H))) 

def make_root(e):
	# Make a root node with no children whose sole item is e
	x = Node()
	e.next = e
	x.set = e
	x.key = e.key
	x.rank = 0
	x.left = null
	x.right = null
	x.next = null
	return x

def meldable_insert(x, H):
	# Assuming x is and H are in meldable order
	# If x should come before H in meldable order
	if x.rank < H.rank:
		# Make H into findable order, and add x to the beginning
		# --> x is now in meldable order
		x.next = key_swap(H)
		return x
	# If x's rank matches H's, link x and H
	else:
		# Make a new tree with x and H, make H.next into meldable order
		# and recurse
		return meldable_insert(link(x, H), rank_swap(H.next))

def link(x, y):
	# Make a new node with 1 bigger rank than x and y
	z = Node()
	z.set = null
	z.rank = x.rank + 1
	# Set the new node's children to x and y, and merge up small children
	z.left = x
	z.right = y
	defill(z)
	return z


def meld(H1, H2):
	# Make H1 and H2 meldable, call meldable_meld
	# The result is meldable so make it findable
	return key_swap(meldable_meld(rank_swap(H1), rank_swap(H2)))

def meldable_meld(H1, H2):
	# Assuming H1 and H2 are meldable
	# Make H1 the one with lower rank
	if H1.rank > H2.rank:
		H1,H2 = H2,H1
	if H2 == null: 
		return H1
	else:
		# Recursively meld after first element, then meldable_insert the first
		# element
		return meldable_insert(H1, meldable_meld(rank_swap(H1.next), H2))


import random

def randlist(n):
	return [ random.random() for i in range(n) ]

def randperm(n):
	return random.sample(list(range(n)),n)

def build(lst):
	P = make_heap()
	for it in lst:
		P=insert(Item(it),P)
	return P

def extract(P):
	lst = [];
	while P!=null:
		lst.append(find_min(P)[0].key)
		P = delete_min(P)
	return lst
		
def sort(lst):
	print(lst)
	P = build(lst)
	lst1 = extract(P)
	if T==INF:
		for i in range(1,len(lst)):
			if lst1[i]<lst1[i-1]:
				print("BUG!!!")
				raise BUG()
	print(lst1)
	print(" ")
	return lst1

sort(randperm(100))

T=3
sort(randperm(100))

T=INF
P=build(randperm(100))
Q=build(randperm(200))
print(extract(meld(P,Q)))