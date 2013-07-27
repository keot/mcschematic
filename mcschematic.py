#!/usr/bin/env python

import itertools, sys
from pymclevel import mclevel
from numpy import zeros, array

default_location = "/tmp/eee/world/level.dat"

materials = ("Powered Rail", "Detector Rail", "Rail", "Activator Rail")

def main(*args):
	# Load the world
	level = mclevel.fromFile(default_location)

	# Convert material names into a material id tuple
	material_ids = tuple(level.materials[material_name].ID for material_name in materials)

	for (chunk, slices, point) in level.getAllChunkSlices():

			for x, a in enumerate(chunk.Blocks):
				for y, b in enumerate(a):
					for z, c in enumerate(b):
						if c in material_ids:
							(cx, cz) = chunk.chunkPosition
							print "{0}\t{1}\t{2}\t{3}\t{4}".format(cx * 16, cz * 16, x, y, z)

	print "Done!"
	
	return 0

if (__name__ == "__main__"):
	sys.exit(main(*sys.argv) )
