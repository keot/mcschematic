#!/usr/bin/env python

import itertools, sys, uuid, numpy
from pymclevel import mclevel

default_location = "/tmp/eee/world/level.dat"

rail_names = ("Powered Rail", "Detector Rail", "Rail", "Activator Rail")

def adjacentRail(this_rail, search_rail):
	# Returns true if this_rail tuple(x, z, y) is adjacent to search_rail
	tx, tz, ty = this_rail
	sx, sz, sy = search_rail

	if (sx == tx):
		if (sy == ty + 1):
			return True
		if (sy == ty - 1):
			return True
		if (sz == tz + 1):
			return True
		if (sz == tz - 1):
			return True
	
	if (sy == ty):
		if (sx == tx + 1):
			return True
		if (sx == tx - 1):
			return True
		if (sz == tz + 1):
			return True
		if (sz == tz + 1):
			return True
	
	if (sz == tz):
		if (sx == tx + 1):
			return True
		if (sx == tx - 1):
			return True
		if (sy == ty + 1):
			return True
		if (sy == ty - 1):
			return True
	
	return False

def main(*args):
	# Load the world
	level = mclevel.fromFile(default_location)
	chunks = level.chunkCount

	sys.stderr.write("Found %d chunks in '%s'.\n" % (chunks, default_location) )

	# Convert material names into a material id tuple
	rail_ids = tuple(level.materials[material_name].ID for material_name in rail_names)

	rail_locations = list() # output

	# Iterate through every chunk
	for c, (chunk, slices, point) in enumerate(level.getAllChunkSlices() ):
		(cx, cz) = chunk.chunkPosition
		rails = (chunk.Blocks == any(rail_ids) )

		# If there are any rails...
		if rails.any():
			# rails contains three lists [x,z,y] of the full chunk, containing booleans
			i = rails.nonzero() # indicies of true items
			number = len(i[0]) # number of rails
			for n in range(0, number):
				rail_locations.append(( (cx*16) + i[0][n], (cz*16) + i[1][n], i[2][n] ))
		
		# Print progress
		if (c+1) % 100 == 0:
			sys.stderr.write("\r%.2f%% complete. (%d chunks remaining...)            " % (100.0*(float(c) / chunks), chunks - c) )
			sys.stderr.flush()

	# Output the data
	sys.stdout.write("#x\tz\ty\n")
	
	for location in rail_locations:
		sys.stdout.write("%d\t%d\t%d\n" % location)

	sys.stderr.write("\nDone!\n")

	return 0

if (__name__ == "__main__"):
	sys.exit(main(*sys.argv) )
