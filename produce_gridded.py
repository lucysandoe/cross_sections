import numpy as np 
import matplotlib.path
import matplotlib.pyplot as plt
import netcdf_functions


def input(filename):
	triangle_file = []
	index_file = []
	with open(filename, 'r') as file:
		for line in file:
			if line[3] == 'Z':
				index_file.append(float(line[4:-2]))
			else:
				string = line.split()
				triangle_file.append(float(string[0]))
				triangle_file.append(float(string[1]))
	return triangle_file, index_file

# grid
def make_grid(lonmin, lonmax, latmin, latmax, stepsize):
	lons = np.arange(lonmin, lonmax, stepsize)
	lats = np.arange(latmin, latmax, stepsize)
	grid = []
	for i in range(len(lats)):
		for j in range(len(lons)):
			grid.append([lons[j], lats[i]])
	return grid, lons, lats

def make_triangles(triangles):
	new_triangles = []
	for i in range(0, len(triangles), 6):
		triangle = np.empty([3, 2])
		triangle[0][0] = triangles[i]
		triangle[0][1] = triangles[i+1] 
		triangle[1][0] = triangles[i+2]
		triangle[1][1] = triangles[i+3]
		triangle[2][0] = triangles[i+4]
		triangle[2][1] = triangles[i+5]
		new_triangles.append(triangle)
	return new_triangles

def find_in_triangles(triangles, index_file, grid):
	val_arr = np.nan*np.ones(len(grid))
	for j in range(len(grid)):
		for i in range(len(triangles)):
			tripath = matplotlib.path.Path(triangles[i])
			if tripath.contains_point(grid[j]):
				val_arr[j] = index_file[i]
				break
	return val_arr

def configure_vals(val_arr, lons, lats):
	new_vals = []
	for i in range(0, len(val_arr), len(lons)):
		new_vals.append(np.array(val_arr[i:i+len(lons)]))
	return new_vals

def seperate_coords(grid):
	xdata = []
	ydata = []
	for grdpt in grid:
		xdata.append(grdpt[0])
		ydata.append(grdpt[1])
	return xdata, ydata


def output(xdata, ydata, vals, outdir, indexfile, outfile):
	valfile = open(outdir+indexfile, 'w')
	for val in vals:
		valfile.write(str(val)+'\n')
	valfile.close()
	netcdf_functions.produce_output_netcdf(xdata, ydata, vals, 'per year', outdir+outfile);
	# netcdf_functions.flip_if_necessary(outdir+outfile);
	return

myfile, myvals = input("../2D_Strain/Results/Results_Delaunay/max_shear.txt")
mygrid, mylons, mylats = make_grid(-125, -121, 39, 42.2, 0.05)
mytri = make_triangles(myfile)
mygridvals = find_in_triangles(mytri, myvals, mygrid)
mynewvals = configure_vals(mygridvals, mylons, mylats)
print(len(mynewvals))
print(len(mylats))

myx, myy = seperate_coords(mygrid)
output(mylons, mylats, mynewvals, '../2D_Strain/Results/Results_Delaunay/', 'max_shear_index_file.txt','max_shear.nc')


# plt.plot(myx,myy,'.')

# print(len(mygrid))
# print(len(mygridvals))
# print(mygridvals[11])
# print(np.max(mygridvals))
# print(np.min(mygridvals))
# print(np.mean(mygridvals))

