import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import rc
from scipy.stats import linregress

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
star_name = 'Sgr37001487'

# I don't remember what the following was for.
'''species_list = ['Na I', 'Mg I', 'Ca I', 'Sc II', 'Ti I', 'Ti II', 'Cr I',
				'Mn I', 'Ni I', 'Y  II', 'Ba II']

sp_abun_list = [5.126, 7.108, 6.119, 2.954, 4.787, 4.953, 4.919, 5.53, 6.912, 6.873, 6.172, 1.97, 1.645]

sp_atomic_num = [11.0, 12.0, 20.0, 21.1, 22.0, 22.1, 24.0, 25.0, 26.0, 26.1, 28.0, 39.1, 56.1]'''

'''fig = plt.figure(figsize=(6, 6))
plt.plot(sp_atomic_num, sp_abun_list, 'o--', color='gray', mfc='m')
plt.xlabel('Atomic Number (Z)')
plt.ylabel('$log_{10}\epsilon(Z)$')
plt.show()'''


def linear_func(x, m, c):
	"""
	Straight lines!
	"""
	return m*x + c


def read_element_abun(file_path, element='Fe I', drop_nan=False):
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
	if element == 'O I':
		print(data)
	# clean rows containing NaN values
	if drop_nan == True:
		data.dropna(inplace=True)
		data.reset_index(drop=True, inplace=True)
	# getting rid of NaN values may affect the average and std. deviation. estimate them again.
	if len(data) == 0: # if this becomes an empty df
		print(f'Careful: you may not have measured {element}')
		return None

	global avg_abun, std_dev
	avg_abun = np.average(data['abund']).round(3)
	std_dev = np.std(data['abund']).round(3)
	return data

# The following array was copied from Jan Ryzbicki's Chempy
# these are photospheric abundances
lodders_abundances = [12.00,10.93,3.28,1.32,2.81,8.39,7.86,8.73,4.44,8.05,6.29,7.54,6.46,\
		7.53,5.45,7.16,5.25,6.50,5.11,6.31,3.07,4.93,3.99,5.65,5.50,7.46,\
		4.90,6.22,4.27,4.65,3.10,3.59,2.32,3.36,2.56,3.28,2.38,2.90,2.20,\
		2.57,1.42,1.94,1.78,1.10,1.67,1.22,1.73,0.78,2.09,1.03,2.20,1.57,\
		2.27,1.10,2.18,1.19,1.60,0.77,1.47,0.96,0.53,1.09,0.34,1.14,0.49,\
		0.95,0.14,0.94,0.11,0.73,-0.14,0.67,0.28,1.37,1.36,1.64,0.82,1.19,\
		0.79,2.06,0.67,0.08,-0.52]
asplund09_abundances = [12.00,10.93,3.26,1.30,2.79,8.43,7.83,8.69,4.42,7.93,6.24,7.60,6.45,\
		7.51,5.41,7.12,5.23,6.40,5.03,6.34,3.15,4.95,3.93,5.64,5.43,7.50,\
		4.99,6.22,4.19,4.56,3.04,3.65,2.30,3.34,2.54,3.25,2.52,2.87,2.21,\
		2.57,1.46,1.88,1.75,0.91,1.57,0.94,1.71,0.80,2.04,1.01,2.18,1.55,\
		2.24,1.08,2.18,1.10,1.58,0.72,1.42,0.96,0.52,1.07,0.30,1.10,0.48,\
		0.92,0.10,0.84,0.10,0.85,-0.12,0.85,0.26,1.40,1.38,1.62,0.92,1.17,\
		0.90,1.75,0.65,0.02,-0.54]
numbers = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12,  13,\
		14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,\
		27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,\
		40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,\
		54, 55, 56, 57, 58, 59, 60, 62, 63, 64, 65, 66, 67,\
		68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80,\
		81, 82, 83, 90, 92]


def read_all_elements(file_name, fe_h):
	"""
	TODO: Make a method that reads the entire summary output file, instead of one element
	at a time
	"""
	elements = ['O  I', 'Na I', 'Mg I', 'Al I', 'Si I', 'Ca I', 'Ti I', 'Mn I', 'Ni I',  'La II', 'Eu II']
	z_nums = [8, 11, 12, 13, 14, 20, 22, 25, 28, 57, 63]
	for i in range(len(elements)):
		el = elements[i]
		el_data = read_element_abun(file_name, element=elements[i], drop_nan=True)
		#print(el_data)
		if el_data is not None:
			avg = np.average(el_data['abund']).round(2)
			std = np.std(el_data['abund']).round(2)

			solar_ab = lodders_abundances[numbers.index(z_nums[i])]
			print(f"A({el}) = {avg}, std = {std}, N_lines = {len(el_data)} \n" +
			f"[{el}/H] = {(avg-solar_ab):.2f}, [{el}/Fe] = {(avg-solar_ab-fe_h):.2f}")


def plot_element_abun(data, element, plot_average=True):
	"""
	Plot abundance (vertical axis) vs EP and other stuff.
	"""
	fig, axes = plt.subplots(figsize=(10, 5), nrows=1, ncols=2, sharey=True)
	axes[0].plot(data['EP'], data['abund'], color='m', linestyle='', marker='o', markersize=3)
	axes[0].set_xlabel('Excitation Potential (eV)')
	axes[0].set_ylabel(r'log$_{10}$ $\epsilon$' + f'({element})')
	axes[1].plot(data['EWin'], data['abund'], color='olive', linestyle='', marker='o', markersize=3)
	axes[1].set_xlabel(r'Equivalent Width (m\AA)')
	plt.subplots_adjust(hspace=0, wspace=0)
	print(f'{element} avg: {avg_abun} sigma: {std_dev}')
	# also put the mean value in there as a dashed line.
	if plot_average == True:
		axes[0].hlines(y = avg_abun, xmin = min(data['EP']), xmax = max(data['EP']), color='k', linestyle='--',
		 linewidth=1, label='average')
	plt.suptitle(f'Abundance plots of element {element} in {star_name}.\n mean={avg_abun}, $\sigma={std_dev}$')
	#plt.show()


def plot_differential_abun(target_data, standard_data, element='Fe I', plot_average=True):
	"""
	target_data -- of the target star
	standard_data -- of the differential standard being used (e.g. Arcturus)
	"""
	# take the difference to find "differetial" abundance
	diff_abund = target_data['abund'] - standard_data['abund']
	#display(target_data['abund'])
	target_data['diff_abund'] = diff_abund
	target_data.dropna(inplace=True)
	target_data.reset_index(drop=True, inplace=True)
	fig, axes = plt.subplots(figsize=(10,5), nrows=1, ncols=2, sharey=True)
	
	axes[0].plot(target_data['EP'], target_data['diff_abund'], 'mo', markersize=3)
	axes[0].set_xlabel('Excitation Potential (eV)')
	axes[0].set_ylabel(r'$\Delta$' + f'[{element[:2]}/H]')
	axes[1].plot(target_data['EWin'], target_data['diff_abund'], color='olive', linestyle='', marker='o', markersize=3)
	axes[1].set_xlabel(r'Equivalent Width (m\AA)')
	plt.subplots_adjust(hspace=0, wspace=0)
	# also put the mean value in there as a dashed line.
	avg_diff_abun = np.average(target_data['diff_abund']).round(3)
	std_dev = np.std(target_data['diff_abund']).round(3)
	if plot_average == True:
		axes[0].hlines(y = avg_diff_abun, xmin = min(target_data['EP']), xmax = max(target_data['EP']), color='k', linestyle='--',
		 linewidth=1, label='average')
	plt.suptitle(f'Differential abundance plots of element {element} in {star_name}.\n mean={avg_diff_abun}, $\sigma={std_dev}$')
	plt.show()


def check_bad_lines(data, tolerance=0.5, diff=True):
	# print lines
	print(f'Lines with abundances outside {tolerance} dex of the average:')
	data.reset_index(inplace=True)
	print([(f"{data['wavelength'][i]}: {data['abund'][i]}") for i in range(len(data))
		if abs(data['diff_abun'][i] - np.average(data['diff_abun'])) > tolerance])


def plot_logg_var(file_path):
	data = pd.read_csv(file_path, sep='\t')
	fig = plt.figure(figsize=(6,6))
	plt.plot(data['log g'], data['Fe I'], color='gray', linestyle='--', marker='s', mfc='m', label='Fe I')
	plt.plot(data['log g'], data['Fe II'], marker='^', color='olive', linestyle='-.', label='Fe II')
	plt.xlabel('$\log g$')
	plt.ylabel('A(Fe)')
	plt.legend()
	plt.plot()


def plot_ionization_eqm(diff=False):
	"""
	Parameters:
	diff: whether or not to use line-by-line differential 
	"""
	fig, axes = plt.subplots(figsize=(13, 6.5), nrows=1, ncols=2)

	abund_col = 'abund'
	iron_i_data['diff_abun'] = iron_i_data['abund'] - diff_iron_i['abund']
	iron_ii_data['diff_abun'] = iron_ii_data['abund'] - diff_iron_ii['abund']
	iron_i_data.dropna(inplace=True)
	iron_ii_data.dropna(inplace=True)
	#print(iron_i_data)
	if diff == False:
		plt.ylabel('$\log_{10} \epsilon (\mathrm{Fe})$', fontsize=14)
	else:
		abund_col = 'diff_abun'
		plt.ylabel('$\Delta$[Fe/H]', fontsize=14)
	fe_i_av = np.average(iron_i_data[abund_col])
	print(f'Fe I: Average:{fe_i_av:.3f}, Sigma:{np.std(iron_i_data[abund_col]):.3f}.'
			+ f" [Fe I/H] = {(fe_i_av - 0.45):.2f}")
			#+ f" Standard zero-point: {np.average(diff_iron_i['abund']):.3f}")
	fe_ii_av = np.average(iron_ii_data[abund_col])
	print(f'Fe II: Average:{fe_ii_av:.3f}, Sigma:{np.std(iron_ii_data[abund_col]):.3f}.'
			+ f" [Fe II/H] = {(fe_ii_av - 0.45):.2f}")
			#+ f" Standard zero-point: {np.average(diff_iron_i['abund']):.3f}")
	axes[0].plot(iron_i_data['EP'], iron_i_data[abund_col], label='Fe I', color='cornflowerblue',
					marker='o', linestyle='', markersize=6, mec='black', mew=0.3)
	axes[0].plot(iron_ii_data['EP'], iron_ii_data[abund_col], label='Fe II', color='deeppink',
					marker='D', linestyle='', markersize=6, mec='black', mew=0.3)

	# now fit a straight line passing through the data points to determine slope.
	data_both = iron_i_data.copy().append(iron_ii_data)
	#print(data_both)

	lin_fit = linregress(data_both['EP'], data_both[abund_col])
	print(lin_fit)
	ep_range = np.linspace(min(data_both['EP']), max(data_both['EP']), num=len(data_both))
	lin_abun_fit = lin_fit.slope*ep_range + lin_fit.intercept
	
	# plot straight line fit
	axes[0].plot(ep_range, lin_abun_fit, ls='--', color='gray', label='average')
	axes[0].set_xlabel('Excitation Potential', fontsize=14)

	axes[1].plot(iron_i_data['EWin'], iron_i_data[abund_col], marker='o', color='silver', ls='', mec='k',
				mew=0.2, label='Fe I')
	axes[1].plot(iron_ii_data['EWin'], iron_ii_data[abund_col], marker='D', color='tab:pink', ls='', mec='k',
				mew=0.2, label='Fe II')
	axes[1].set_xlabel('Equivalent Width ($m\mathrm{\AA}$)', fontsize=14)

	for ax in axes:
		ax.minorticks_on()
		ax.tick_params(axis='both', which='major', labelsize=14)
		ax.legend(fontsize=12)
	plt.title(f"A(Fe I) Average:{np.average(iron_i_data[abund_col]):.3f} ; Sigma:{np.std(iron_i_data)[abund_col]:.3f}")
	plt.tight_layout()
	
	fe_i_av = np.average(iron_i_data[abund_col])
	plt.ylim(fe_i_av+0.4, fe_i_av-0.4)
	
	if diff == True:
		#plt.ylim(fe_i_av-0.41, fe_i_av+0.41)
		plt.savefig('diff_ionization_equm.png', dpi=300)
	else:
		plt.savefig('ionization_equm.png', dpi=300)
	plt.show()


def plot_ew_wavelength(target_data, diff_data, diff=True):
	fig = plt.figure(figsize=(6,6))
	if diff == True:
		plt.plot(target_data['wavelength'], target_data['abund']-diff_data['abund'], ls='', marker='o',
				mfc='cornflowerblue', mec='k', mew=0.2)
	plt.xticks(fontsize=12)
	plt.yticks(fontsize=12)
	plt.xlabel('Wavelength', fontsize=12)
	plt.ylabel('Abundance', fontsize=12)
	plt.show()

use_old_method = False

if __name__ == '__main__':
	#plot_logg_var('../data/sgr/sgr3700/fe_ionization_eq.txt')
	if use_old_method == True:
		# use Arcturus as a differential standard
		standard_data = read_element_abun('../data/arcturus/arcturus.out2', element='Fe I', drop_nan=False)
		# target star
		target_data = read_element_abun('../data/sgr/sgr4210/sgr4210.out2', element='Fe I', drop_nan=True)
		print(target_data)
		#
		plot_differential_abun(target_data, standard_data, element=element, plot_average=False)
	else:
		#for e in species_list:
		#	element = e
		abun_out = '../data/sgr/sgr4210/sgr4210.out2'
		diff_out = '../data/arcturus/arcturus.out2'
		iron_i_data = read_element_abun(abun_out, element='Fe I', drop_nan=False)
		#print(len(iron_i_data))
		iron_ii_data = read_element_abun(abun_out, element='Fe II', drop_nan=False)
		
		diff_iron_i = read_element_abun(diff_out, element='Fe I', drop_nan=False)
		diff_iron_ii = read_element_abun(diff_out, element='Fe II', drop_nan=False)
		#plot_ew_wavelength(iron_i_data, diff_iron_i)
		#print(iron_ii_data)
		#print(diff_iron_ii)
		if len(iron_i_data) != len(diff_iron_i):
			print(f'Line lengths for target: {len(iron_i_data)}, {len(iron_ii_data)}')
			raise Exception('Error: Fe I line lists for target and standard are not equal in length.'
					+ ' Check abundance summary again!')
		if len(iron_ii_data) != len(diff_iron_ii):
			raise Exception('Error: Fe II line lists for target and standard are not equal in length. Check again!')
		
		read_all_elements(abun_out, fe_h=-0.18)

		plot_ionization_eqm(diff=True)
		check_bad_lines(iron_i_data, 0.25)
		#plot_element_abun(iron_i_data, element, plot_average=True)
		#plot_element_abun(fe_ii_data, element='Fe II', plot_average=False)
		plt.show()
	

