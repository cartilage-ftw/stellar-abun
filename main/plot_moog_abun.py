import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc

"""
Script for plotting data from abundance output summary file from MOOG.
"""

# Use LaTeX and CMU Serif font.
rc('text', usetex=True)
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

# initialize default vals
avg_abun = std_dev = 0.0
# tell it which element I want to search. 
element = 'Fe I'
star_name = 'the Sun'


def read_element_abun(file_path, element='Fe I'):
	"""
	Reads the abundancy summary output file by MOOG, searches for a specific element's abundance
	in it, and returns it into a pandas DataFrame
	"""
	# wait until you hit this
	text_to_start = 'Abundance Results for Species ' + element + ' ' # the extra ' ' ensures Fe II doesn't get matched
	# stop reading once you hit this.
	text_to_stop = 'average abundance'
	start = stop = -1
	with open(file_path) as summary_file:
		lines = summary_file.readlines()
		for i in range(len(lines)):
			# start reading once you encounter that
			if text_to_start in lines[i]:
				start = i+1
				continue
			if start != -1 and text_to_stop in lines[i]:
				stop = i-1
				break
		num_rows = stop - start
	data = pd.read_csv(file_path, delim_whitespace=True, skiprows=start, nrows=num_rows)
	# clean rows containing NaN values
	data.dropna(inplace=True)
	# getting rid of NaN values may affect the average and std. deviation. estimate them again.
	global avg_abun, std_dev
	avg_abun = np.average(data['abund']).round(3)
	std_dev = np.std(data['abund']).round(3)
	return data


def plot_element_abun(data, element, plot_average=True):
	"""
	Plot abundance (vertical axis) vs EP and other stuff.
	"""
	fig, axes = plt.subplots(figsize=(10, 5), nrows=1, ncols=2, sharey=True)
	axes[0].plot(data['EP'], data['abund'], 'mo', markersize=3)
	axes[0].set_xlabel('Excitation Potential (eV)')
	axes[0].set_ylabel(r'log$_{10}$ $\epsilon$' + f'({element})')
	axes[1].plot(data['EWin'], data['abund'], color='olive', linestyle='', marker='o', markersize=3)
	axes[1].set_xlabel(r'Equivalent Width (m\AA)')
	plt.subplots_adjust(hspace=0, wspace=0)
	# also put the mean value in there as a dashed line.
	if plot_average == True:
		axes[0].hlines(y = avg_abun, xmin = min(data['EP']), xmax = max(data['EP']), color='k', linestyle='--',
		 linewidth=1, label='average')
	plt.suptitle(f'Abundance plots of element {element} in {star_name}.\n mean={avg_abun}, $\sigma={std_dev}$')
	plt.show()


if __name__ == '__main__':
	abun_data = read_element_abun('../data/solar/solar.out2', element)
	plot_element_abun(abun_data, element)
