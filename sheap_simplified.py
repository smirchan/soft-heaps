""" Python implementation of "Soft Heaps Simplified" by Kaplan, Tarjan and Zwick.
 	Derived from code (c) Haim Kaplan, Robert E. Tarjan and Uri Zwick,
 	but heavily adapted.
"""

import math
INF = float('inf')

"""
To use:
	
	sheap = SoftHeap(eps)		==> Make a new Soft Heap (0 <= eps < 1)

	sheap.insert(7)				==> 7 is inserted

	ptr, key = sheap.find_min() ==> Get a pointer to the root of minimum key
									and its key

	sheap.delete_min()			==> Deletes an item from the minimum key

	sheap2 = SoftHeap(eps)
	sheap.meld(sheap2)			==> melds sheap2 into sheap1
"""

class Item:
	"""Class hat defines an item in a linked list.
	"""

	def __init__(self, it):
		self.key = it
		self.next = self


class Node:
	"""	Class that defines a heap node which can hold one or more Items,
		and low-level helper functions.
	"""

	def __init__(self, set=None, key=None,
				 left=None, right=None, next=None):
		self.set = set
		self.key = key
		self.left = left
		self.right = right
		self.next = next

	def is_leaf(self):
		return self.left == SoftHeap.null

	def first_item(self):
		return self.set.next

	def set_first_item(self, it):
		self.set.next = it

	def has_multiple_items(self):
		return self.first_item() != self.first_item().next

	def wire_out_first_item(self):
		self.set_first_item(self.first_item().next)

	def delete_items(self):
		self.set = SoftHeap.null

	def has_items(self):
		return not self.set == SoftHeap.null

	def swap_children(self):
		self.left, self.right = self.right, self.left

	def move_right_child_left(self):
		self.left = self.right
		self.right = SoftHeap.null

	def absorb_left_key(self):
		self.key = self.left.key

	def absorb_left_items(self):
		self.set = self.left.set
		self.left.set = SoftHeap.null

	def append_left_items(self):
		self.set.next, self.left.set.next = self.left.set.next, self.set.next
		self.left.set = SoftHeap.null


class SoftHeapNode(Node):
	""" Class that defines a node in the soft heap and higher-level functions
		to manipulate them.  This is the meat of the algorithm.
	"""

	def __init__(self, set=None, key=None,
				 left=None, right=None, next=None,
				 rank=None, T=None):
		Node.__init__(self, set, key, left, right, next)
		self.rank = rank
		self.T = T

	def double_even_condition(self):
		return self.rank > self.T and self.rank % 2 == 0

	def defill(self):
		# Merge our smaller child into us; and keep doing that until
		# we've merged in a leaf
		self.fill()
		# If our rank is even and greater than T, do it again
		if self.double_even_condition() and not self.is_leaf():
			self.fill()

	def fill(self):
		# Ensure our left child has the smaller key of our two children
		if self.left.key > self.right.key:
			self.swap_children()
		# Merge our left child into us (we may or may not already have items)
		self.absorb_left_key()
		if not self.has_items():
			self.absorb_left_items()
		else:
			self.append_left_items()
		# If our left child is now a leaf, destroy it and move our
		# right child in its place
		if self.left.is_leaf(): 
			self.move_right_child_left()
		# Otherwise, call defill on it
		else:
			self.left.defill()

	def find_min(self):
		# Assume findable order; we are root of minimum key (of the heap
		# that we represent)
		return (self.first_item(), self.key)

	def rank_swap(self):
		# Swap us with the next heap node if next has a smaller rank
		x = self.next
		if self.rank <= x.rank: 
			return self
		else:
			self.next = x.next
			x.next = self 
			return x

	def key_swap(self):
		# Swap us with the next heap node if next has a smaller key
		x = self.next
		if self.key <= x.key: 
			return self
		else:
			self.next = x.next
			x.next = self
			return x

	def delete_min(self):
		# Assume findable order; we are the root with minimum key
		# If we have more than one item, wire out the first_item element and
		# return it
		if self.has_multiple_items(): 
			self.wire_out_first_item()
			return self
		# If there's only one item
		else:
			# Delete that item
			self.delete_items()
			k = self.rank
			# If we are a leaf, make ourselves the next tree
			if self.is_leaf(): 
				L = self.next
				self = L
			# If we are not a leaf, raise small child (recursively),
			# and if we have an even rank beyond T, do this again
			else:
				self.defill()
			# Restore findable order
			return self.reorder(k)

	def reorder(self, k):
		# Implemented recursively: while self.next has rank < k, 
		# swap self with self.next if it's lower --> sorted by rank;
		# walking backwards, swap self with self.next if self.next has
		# smaller key --> findable order
		if self.next.rank < k: 
			self = self.rank_swap()
			self.next = self.next.reorder(k)
		return self.key_swap()

	def make_root(self, e):
		# Make a root node with no children whose sole item is e
		e.next = e
		x = SoftHeapNode(set=e, key=e.key,
						 left=SoftHeap.null, right=SoftHeap.null, next=SoftHeap.null,
						 rank=0, T= self.T)
		return x

	def insert(self, it):
		# Assuming we is in findable order, make us into meldable order,
		# meldable_insert us with the new root
		# The result is in meldable order, so convert us to findable order
		e = Item(it)
		return self.rank_swap().meldable_insert(self.make_root(e)).key_swap()

	def meldable_insert(self, x):
		# Assuming x and self are in meldable order
		# If x should come before us in meldable order
		if x.rank < self.rank:
			# Make us into findable order, and add x to the beginning
			# --> x is now in meldable order
			x.next = self.key_swap()
			return x
		# If x's rank matches ours, link x and us
		else:
			# Make a new tree with x and us, make our next into meldable order
			# and recurse
			return self.next.rank_swap().meldable_insert(x.link(self))

	def link(self, y):
		# Make a new node with 1 bigger rank than us and y
		z = SoftHeapNode(set=SoftHeap.null,
					 	 rank=self.rank + 1,
					 	 left=self,
					 	 right=y,
					 	 T=self.T)
		# Set the new node's children to us and y, and merge up small children
		z.defill()
		return z

	def meld(self, other):
		# Make self and other meldable, call meldable_meld
		# The result is meldable so make it findable
		return self.rank_swap().meldable_meld(other.rank_swap()).key_swap()

	def meldable_meld(self, other):
		# Assuming self and other are meldable
		# Make us the one with lower rank
		if self.rank > other.rank:
			self, other = other, self
		if other == SoftHeap.null: 
			return self
		else:
			# Recursively meld after first element, then meldable_insert the first
			# element
			return other.meldable_meld(self.next.rank_swap()).meldable_insert(self)


class SoftHeap:
	"""Wrapper class for the soft heap.
	"""

	# Global null node
	null = SoftHeapNode(key=INF, rank=INF)
	null.set = null
	null.left = null
	null.right = null
	null.next = null

	def __init__(self, eps):
		self.eps = eps
		if self.eps == 0:
			self.T = INF
		else:
			self.T = math.ceil(math.log2(3 / self.eps))
		self.heap = SoftHeapNode()
		self.heap = SoftHeap.null
		self.heap.T = self.T

	def insert(self, it):
		self.heap = self.heap.insert(it)

	def find_min(self):
		return self.heap.find_min()

	def delete_min(self):
		self.heap = self.heap.delete_min()

	def meld(self, other):
		self.heap = self.heap.meld(other.heap)

