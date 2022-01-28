# stellar-abun
This repository includes _some_ (yes, _some_ not all) scripts that I wrote since the summer of 2021 while working on galactic chemical evolution using stellar spectroscopy. I thought these would be of use to some people (e.g. reading/writing whitespace delimited line lists ready for MOOG use).

Let me also use this space to publicly advertise the [summer project report](https://drive.google.com/file/d/1V9NzxcFLuNGBogPOag89tqD2v8sC7Vvb/view?usp=sharing) I wrote (which was _practically_ read by two people -- my internship advisor and I). P.S. I think the report is actually good for something jotted down in a week y'all.

I decided to jot down a few notes digitally and make them public.
* [Notes on Fortran 77](notes/Fortran77_Notes.md) I took while learning it.
* A few things I encountered while [installing IRAF on Manjaro](notes/IRAF_Install.md) Linux. **2022 update**: I didn't face most of the issues this time. And.. I'm feeling nostalgic while writing this (now stop reading if you're getting bored!)

I also plan(ned) to upload certain journal [article summaries](notes/articles/).

***
SIMBAD Entries
For our target Sagittarius dSph stars

[Sgr37001487](http://simbad.u-strasbg.fr/simbad/sim-id?Ident=%409039375&Name=2MASS%20J18542499-3031568&submit=submit)
... too lazy to add the rest here.

***
A few things about MOOG:
* If you don't have a license for SuperMongo (SM), install this variant of [MOOG without SM](https://github.com/MingjieJian/moog_nosm). There are many repos which have a MOOG variant which doesn't need SM.
	* There's also [pymoog](https://github.com/MingjieJian/pymoog) created by the same group of people. It's MOOG without SM + python routines for plotting.
* Andy Casey and Alex Ji invented [Spectroscopy Made Harder (SMHR)](https://github.com/andycasey/smhr) which is a modification of MOOG.
	* Older versions of MOOG didn't have Rayleigh scattering (strictly speaking, there was an approximation which didn't take it into account properly). Jennifer Sobeck (UWash) added an improvement to her own version, and Chris Sneden thought he added that to the 2017 MOOG but he actually forgot to. 
		* Rayleigh scattering is important for the most metal poor stars at smaller wavelengths (below 4500A). Alex said the systematic difference it makes is of ~0.1 dex.
		* more automated spectrum synthesis, reducing the user time it takes.
		* improved error analysis