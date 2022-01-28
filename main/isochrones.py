"""
Methods that I use for dealing with the BaSTI stellar isochrones
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib import rc

# Use LaTeX and CMU Serif font.
rc('text', usetex=True)
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

##'iso_12gyr_z002.txt'
# 13 Gyr with z=0.004 seems to fit well?
file_name = 'iso_13gyr_z002.txt'#'wz203y248o.t610000_c03hbs'# 'wz203y248o.t610000_c03hbs' 10 Gyr
path = '../data/sgr/'#isoz23o_c03hbs/'
age_gyr = 13
iso_file_list = os.listdir(path)
M_V = -1.419
error_low = 0.156
error_high = -0.145
V_K = 3.210

# I derived the photometric temp from the RM05 calibration
T_eff = np.log10(4102) # log scale

def plot_isochrone(file_name, col):
	"""
	Plot a single isochrone out of the folder
	:param file_name:
	:return:
	"""
	isochrone_data = pd.read_csv(path+file_name, skiprows=8, delim_whitespace=True,
					names=['(M/Mo)in', '(M/Mo)', 'log(L/Lo)', 'logTe', 'Mv', '(U-B)', '(B-V)', '(V-I)',
					 '(V-R)', '(V-J)', '(V-K)', '(V-L)', '(H-K)'])
	our_point = isochrone_data[abs(isochrone_data['(V-K)'] - V_K) <= 0.05]
	print(our_point)
	ax.minorticks_on()

	plt.plot(isochrone_data['(V-K)'], isochrone_data['Mv'], color=col, linestyle='--',
				 label=f'Z=0.002, [Fe/H]=-0.96, t={age_gyr} Gyr')
	plt.ylim(max(isochrone_data['Mv']) + 0.5, min(isochrone_data['Mv']) - 0.5)
	plt.xlim(min(isochrone_data['(V-K)'])-0.1, max(isochrone_data['(V-K)']+0.1)) # invert axes if using T_eff on x-axis

if __name__ == '__main__':
	fig, ax = plt.subplots(figsize=(6, 6))
	sorted_file_list = sorted(iso_file_list, reverse=True)
	colors = ['magenta', 'pink', 'cyan', 'limegreen', 'red']
	#plots = []
	#for i in range(5):
	#	file_name = sorted_file_list[i]
	#	age_myr = int(file_name[13:18])
	#	plot_isochrone(file_name, age_myr, 'gray')
	plot_isochrone(file_name, 'gray')
	plt.plot(V_K, M_V, color='dodgerblue', marker='*', ms=12, mec='k', mew=0.2, ls='', label='J18542499-3031568')
	# plot error bar
	#plt.errorbar(T_eff, M_V, yerr=(error_high+error_low)/2)
	#plt.xlabel(r'$\log T_{\mathrm{eff}}$')
	plt.xticks(fontsize=14)
	plt.yticks(fontsize=14)
	plt.xlabel(r'$(V-K)_0$', fontsize=14)
	plt.ylabel(r'$M_V$', fontsize=14)
	#plt.ylabel(r'$\log (L/L\odot)$')
	plt.legend(loc='upper left', fontsize=12)
	#plt.legend(bbox_to_anchor=(0.5, 1.05))
	plt.tight_layout()
	plt.savefig('isochrone_vk_scale.png', dpi=300)
	plt.show()