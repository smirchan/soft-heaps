""" Python implementation of "Soft Heaps Simplified" by Kaplan, Tarjan and Zwick.
 	Heavily adapted from code (c) Haim Kaplan, Robert E. Tarjan and Uri Zwick.
"""

import math
INF = float('inf')
T = None

class Item:
	def __init__(e, it):
		e.key = it
		e.next = e

class Node:
	
	def __init__(self, set=None, key=None, rank=None,
				 left=None, right=None, next=None):
		self.set = set
		self.key = key
		self.rank = rank
		self.left = left
		self.right = right
		self.next = next

	"""Self-explanatory helper functions"""

	def is_leaf(self):
		return self.left == null

	def key(self):
		return self.key

	def first(self):
		return self.set.next

	def set_first(self, it):
		self.set.next = it

	def has_more_than_one_element(self):
		return self.first() != self.first().next

	def wire_out_first(self):
		self.set_first(self.first().next)

	def has_items(self):
		return self.set != null

	def swap_children(self):
		self.left, self.right = self.right, self.left

	def move_right_child_left(self):
		self.left = self.right
		self.right = null

	def absorb_left_key(self):
		self.key = self.left.key

	def absorb_left_items(self):
		self.set = self.left.set
		self.left.set = null

	def append_left_items(self):
		self.set.next, self.left.set.next = self.left.set.next, self.set.next
		self.left.set = null

# Global null node
null = Node(key=INF, rank=INF)
null.set = null
null.left = null
null.right = null
null.next = null

def double_even_condition(x):
	return x.rank > T and x.rank % 2 == 0

def defill(x):
	# Merge x's smaller child into it; and keep doing that until
	# you've merged in a leaf
	fill(x)
	# If x.rank is even and greater than T, do it again
	if double_even_condition(x) and not x.is_leaf():
		fill(x)

def fill(x):
	# Ensure x.left has the smaller key of x's two children
	if x.left.key > x.right.key:
		x.swap_children()
	# Merge x.left into x (x may or may not already have items)
	x.absorb_left_key()
	if not x.has_items():
		x.absorb_left_items()
	else:
		x.append_left_items()
	# If x.left is now a leaf, destroy it and move x.right in its place
	if x.left.is_leaf(): 
		x.move_right_child_left()
	# Otherwise, call defill on it
	else:
		defill(x.left)
		
def find_min(H):
	# Assume findable order; H is the root with minimum key,
	# H.set.next is its first item
	return (H.first(), H.key)

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
	# If there's another item, wire out the first element and
	# return it
	if H.has_more_than_one_element(): 
		H.wire_out_first()
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
	# Assuming x and H are in meldable order
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
	z = Node(set=null,
			 rank=x.rank + 1,
			 left=x,
			 right=y)
	# Set the new node's children to x and y, and merge up small children
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

class SoftHeap:
	"""Wrapper class for the soft heap.

		To use:
		
		sheap = SoftHeap(eps)		==> Make a new Soft Heap (0 <= eps < 1)

		sheap.insert(7)				==> 7 is inserted

		ptr, key = sheap.find_min() ==> Get a pointer to the root of minimum key
										and its key

		sheap.delete_min()			==> Deletes an item from the minimum key

		sheap2 = SoftHeap(eps)
		sheap.meld(sheap2)			==> melds sheap2 into sheap1
	"""

	def __init__(self, eps):
		global T
		self.eps = eps
		if self.eps == 0:
			T = INF
		else:
			T = math.ceil(math.log2(3 / eps))
		self.heap = null

	def insert(self, it):
		self.heap = insert(Item(it), self.heap)

	def find_min(self):
		return find_min(self.heap)

	def delete_min(self):
		self.heap = delete_min(self.heap)

	def meld(self, sh):
		self.heap = meld(self.heap, sh.heap)

