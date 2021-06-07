from collections import deque

def dequefilter(deck, condition):
    for _ in range(0, len(deck)):
        item = deck.popleft()
        if condition(item):
            deck.append(item)

def bbox_intersections(seta, setb):
	active_a = deque([])
	active_b = deque([])
	instructions = []
	intersections = []
	def add_to(o, bounds, l):
		l.append( (o, bounds) )
		if l == active_a:
			other = active_b
		else:
			other = active_a
		for (o2, bounds2) in other:
			if bounds.overlaps(bounds2):
				intersections.append( (o, o2) )

	def remove_from(o, bounds, l):
		dequefilter(l, lambda i: i[0] != o)

	for a in seta:
		bounds = a.bounds()
		instructions.append((bounds.left, a, bounds, add_to, active_a))
		instructions.append((bounds.right, a, bounds, remove_from, active_a))
	for b in setb:
		bounds = b.bounds()
		instructions.append((bounds.left, b, bounds, add_to, active_b))
		instructions.append((bounds.right, b, bounds, remove_from, active_b))
	instructions = sorted(instructions, key=lambda i:i[0])
	for key, o, bounds, verb, activelist in instructions:
		verb(o, bounds, activelist)
	return intersections

if __name__ == "__main__":
	from beziers.path.geometricshapes import Rectangle
	from beziers.point import Point
	left = [
		Rectangle(100,70,origin=Point(50,50)),
		Rectangle(30,100,origin=Point(80,150)),
		Rectangle(50,50,origin=Point(200,0)),
	]
	right = [
		Rectangle(100,30,origin=Point(120,0)),
		Rectangle(50,50,origin=Point(0,0)),
		Rectangle(100,250,origin=Point(30,200)),
	]

	import matplotlib.pyplot as plt
	fig, ax = plt.subplots()
	for p in left:
		p.clone().plot(ax,color="blue")
	for p in right:
		p.clone().plot(ax,color="red")
	intersections = bbox_intersections(left,right)
	for l,r in intersections:
		[p.plot(ax,fill="green") for p in l.intersection(r)]
	plt.show()
