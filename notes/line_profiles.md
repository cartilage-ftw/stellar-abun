A good resource for learning about nucleosynthesis, spectral lines and equivalent widths is [this 66-page lecture slides pdf](http://research.iac.es/congreso/itn-gaia2013//media/Primas2.pdf) by Francesca Primas of ESO, Garching.

### What causes broadening of spectral lines?
There is an intrinsic limit on how sharp a spectral line can be due to energy-time uncertainty. A shorter lifetime of an atom in an excited state corresponds to larger uncertainty in energy and thus a corresponding dispersion in the energy of the emitted photon.

This *natural width* is usually of Lorentzian in shape. However, this shape isn't generally seen, except in the wings of lines from low pressure environments like nebulae, see [this](http://www-star.st-and.ac.uk/~kw25/teaching/nebulae/lecture08_linewidths.pdf). Other line profiles dominate over the natural one in most cases.

#### Collisional broadening
When two atoms collide, there is a slight pertubation which and affects the phase of the emitted radiation and frequent collisions (effectively) reduce the lifetime of the state even further (the link above has a nice illustration of this on slide 5). The corresponding Fourier transform then has a larger line width. Since collisions dominate in high density environment, there is greater broadening in dwarfs than is in giants of the same spectral type.

#### Doppler broadening
Since atoms in a gas are constantly moving, there is an inherent broadnening due to the thermal motion of the atoms. Thermal lines have a Gaussian profile (owing to the velocity distribution function being proportional to $e^{-v^2}$).

It is worth remembeing that the thermal broadening is proportional to $\sqrt{\frac{T}{m}}$ so higher temperatures have more thermal broadening, and broadening also depends on weight of the atom.

#### Voigt profile
Convolution of the thermal Gaussian and natural/collisional Lorentzian is called the "Voigt profile". There isn't a simple analytic form of it. The shape of a Voigt core is similar to that of a Gaussian while the wings extend like  Lorentzian.