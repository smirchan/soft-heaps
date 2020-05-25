from graphviz import *
from PIL import Image
import matplotlib.pyplot as plt
import os
import shutil
from sheap_simplified import SoftHeap
from sheap_simplified_test import *

"""
To use the visualization:

=== Initialization ===

	viz = SoftHeapVisualizer()					==> Make a visualizer
													Optional args:
													dir  --> where to save output files?
													view --> should visualization open files live?
															 either way, images will be saved to dir

	sheap = SoftHeapVisualizable(eps=0.1)		==> Make a new soft heap		

=== Mode 1: Keep track of edits ===

	viz.watch(sheap)							==> Watch everything you do to the heap

	for i in range(5):							==> Perform operations on the heap
		sheap.insert(i)

	viz.export_animation(step_duration=1000)	==> Export a gif


=== Mode 2: Just view the final output ====

	for i in range(5):							==> Perform operations on the hap
		sheap.insert(i)

	viz.viz(sheap)								==> Save final image
"""

class SoftHeapVisualizer:

	def __init__(self, dir="viz_output", view=False):
		self.font = "helvetica bold"
		self.cmd_font = "courier bold"
		self.cmd_color = 'blue'
		self.corrupted_color = 'pink'
		self.uncorrupted_color = '#eefdec'
		self.step = 0
		self.dir = dir
		self.view = view
		self.cache = None
		if os.path.exists(self.dir):
			shutil.rmtree(self.dir)
		path = os.path.join(self.dir, 'images')
		os.makedirs(path)

	def watch(self, sheap):
		sheap.set_watcher(self)
		self.viz(sheap)

	def export_animation(self, step_duration):
		print("Exporting animation...")
		step_imgs = []
		for i in range(self.step):
			img = Image.open('./{}/images/step_{}.png'.format(self.dir, i))
			step_imgs.append(img.copy())
			img.close()
		max_w = max([img.size[0] for img in step_imgs])
		max_h = max([img.size[1] for img in step_imgs])
		resized_imgs = []
		for img in step_imgs:
			resized = Image.new(img.mode, (max_w, max_h), (255, 255, 255))
			resized.paste(img, (0, 0))
			resized_imgs.append(resized)
		out = './{}/animation.gif'.format(self.dir)
		resized_imgs[0].save(out, save_all=True, append_images=resized_imgs[1:], duration=step_duration)

	def get_item_list(self, node):
		items = []
		start = node.first_item()
		curr = start
		while True:
			items.append(curr.key)
			curr = curr.next
			if curr == start:
				break
		return items

	def desc(self, node):
		if node == SoftHeap.null:
			return "<<TABLE BORDER='0' CELLBORDER='1' CELLPADDING='1'><TR><TD>NULL</TD></TR></TABLE>>"
		else:
			items = self.get_item_list(node)
			color = ""
			if len(items) > 1 or (len(items) == 1 and items[0] != node.key):
				color = self.corrupted_color
			else:
				color = self.uncorrupted_color
			label = f"<<TABLE BORDER='0' CELLBORDER='1'><TR><TD>{node.key}</TD></TR>\
					<TR><TD BGCOLOR='{color}'><FONT POINT-SIZE='10'>{str(items)[1:-1]}</FONT></TD></TR></TABLE>>"
			return label
	
	def name(self, node):
		return str(id(node))

	def add_node(self, node, graph):
		graph.node(self.name(node), self.desc(node), fontname=self.font, shape="plain")

	def add_edge(self, node1, node2, graph, label=None):
		graph.edge(self.name(node1), self.name(node2), label=label, fontname=self.font)

	def viz_roots(self, heap):
		r = Digraph(name='roots')
		curr = heap
		with r.subgraph(name="roots_cluster", graph_attr={"rank": "same"}) as ro:
			while True:
				self.add_node(curr, ro)
				r.subgraph(self.viz_root(curr))
				if curr == SoftHeap.null:
					break
				self.add_edge(curr, curr.next, r, "next")
				curr = curr.next
		return r

	def viz_root(self, heap):
		r = Digraph(name=self.name(heap)+"_tree")
		def dfs(root):
			if root.left != SoftHeap.null:
				self.add_node(root.left, r)
				self.add_edge(root, root.left, r, "L")
				dfs(root.left)
			if root.right != SoftHeap.null:
				self.add_node(root.right, r)
				self.add_edge(root, root.right, r, "R")
				dfs(root.right)
		dfs(heap)
		return r

	def viz(self, sheap, view=False, title=" ", use_cached=False):
		if use_cached and self.cache is not None:
			dot = cache
		else:
			dot = Digraph(format='png')
			r = self.viz_roots(sheap.heap)
			dot.subgraph(r)
		if title is not None:
			dot.attr(label=title)
			dot.attr(labelloc='t')
			dot.attr(labeljust='l')
			dot.attr(fontname=self.cmd_font)
			dot.attr(fontcolor=self.cmd_color)
		dot.render('./{}/images/step_{}'.format(self.dir, self.step))
		if view or self.view:
			im = Image.open('./{}/images/step_{}.png'.format(self.dir, self.step))
			im.show()
			# plt.imshow(im)
			# plt.show()
		self.step += 1
		self.cached = dot


class SoftHeapVisualizable(SoftHeap):

	def __init__(self, eps, funcs_to_watch=['delete_min', 'find_min', 'meld', 'insert']):
		SoftHeap.__init__(self, eps)
		self.funcs_to_watch = funcs_to_watch
		self.watcher = None

	def set_watcher(self, watcher):
		self.watcher = watcher
		for attr in dir(self):
			if attr in self.funcs_to_watch:
				setattr(self, attr, self.viz_func(getattr(self, attr)))

	def viz_func(self, func):
		def wrapper(*args, **kwargs):
			call_name = "{}({})".format(func.__name__, str(args)[1:-2])
			print("Visualizing {}".format(call_name))
			self.watcher.viz(self, title=call_name, use_cached=True)
			func(*args, **kwargs)
			self.watcher.viz(self, title=call_name + " - done")
		return wrapper


if __name__ == "__main__":
	viz = SoftHeapVisualizer(view=False, dir="viz_test")
	sheap = SoftHeapVisualizable(eps=0.4)
	viz.watch(sheap)

	for i in range(24):
		sheap.insert(i)
	for i in range(12):
		sheap.delete_min()

	viz.export_animation(step_duration=500)
	
	"""
	Or, you could do something like:
	
	viz = SoftHeapVisualizer(view=False, dir="viz_test")
	sheap = SoftHeapVisualizable(eps=0.4)

	for i in range(128):
		sheap.insert(i)
	for i in range(64):
		sheap.delete_min()

	viz.viz(sheap)
	"""
