## A few notes on Fortran 77
Online resources for Fortran 77 are not that many. Most that I found were a copy-paste of [this old Stanford tutorial](https://web.stanford.edu/class/me200c/tutorial_77/). There are parts of that tutorial that weren't as helpful, I referred to [this one](https://www2.ph.ed.ac.uk/~playfer/f77_tut.html) for functions and subroutines. Finally, there are [more comprehensive ones](https://www.star.le.ac.uk/~cgp/fortran.html) that I didn't have the time for but am mentioning here in case someone finds it useful.

* Every "physical line" must start with 6 blanks. Comments can, however, start from the first character of the line itself.
* It's stupid how
	```fortran
	real pi = 3.14159
	```
	compiles just fine without any errors, but in reality doesn't take the value ```3.14159```, it will get initialized with some weird number ```5.10E-43```. Declaration and assignments must happen in separate lines (except for constants).
	```fortran
	real pi
	pi = 3.14159
	```
* To make pi a constant
	```fortran
	real pi
	parameter (pi = 3.14159)
	```
	Multiple constants can be assigned in one line
	```fortran
	real a, b, c, d, e, f
	parameter (a = 1.0, b = 314.31, .. c = <insert_value>)
* There's a stupid rule for type inference when the variable type isn't specified. If variable names start with ```i, j, k, m, n```, it's assumed to be an integer. Can be disabled using
	```implicit none```
* A 'main' program is called a 'driver', and subprograms are called 'subroutines' or 'procedures'.
* ```6.67E-11``` is a float while ```6.67D-11``` is a double.
* Constants must be assigned values before variables (otherwise you get an error).
* Apostrophe inside a string is included by writing ```''```
	```fortran
	write(*,*) 'It''s funny, isn''t it?'
	```
* The type conversion method for char -> int is called ```ichar``` (? is that supposed to make sense?).
	To convert a ```real x``` (float) into a double use ```dble(x)```
* There are no ```>=``` etc. operators, one uses
	```fortran
	.LE.	for <=
	.GE.	for >=
	.LT.	for <
	.GT.	for >
	.EQ.	for ==
	.NE.	for /= (or, as in modern languages, !=)
	```
* A lot of empty spaces are added when concatenating two strings (or other types converted into strings)
	```fortran
	  logical a, b
	  integer i
	  i = 1
	  a = .TRUE.
	  b = .TRUE.
	  do while (a .AND. b)
	  	if (i .GE. 5)	b = .FALSE.
		write(*,*) 'F', i
		i = i+1
	  enddo
	  end
	```
	gives the output
	```
	F           1
	F           2
	F           3
	F           4
	F           5
	```
* Indices in Fortran arrays start from 1 (one thing I liked). An explicit index range can be assigned too, e.g.
	```fortran
	real my_numbers(-28:31)
	```
* Loops can be assigned numbered labels
	```fortran
	  integer minkowski_metric(4, 4)
	  integer i, j
	  do 10 i = 1, 4
		do 20 j = 1, 4
			if (i .EQ. j) then
				if (i .EQ. 1) then
					minkowski_metric(i, j) = -1
				else
					minkowski_metric(i,j) = 1
				endif
			else
				minkowski_metric(i,j) = 0
			endif
  20	continue
  10  continue
	```
* Higher dimensional arrays are stored as a 1-D sequence of elements, column by column (i.e. eta(1, 4) is followed by eta(2,1) for a 4x4 matrix eta).
	```fortran
	c This is what printing the minkowski_metric defined above gives using ``write(*,*)``
	    -1.00000000       0.00000000       0.00000000       0.00000000       0.00000000       1.00000000       0.00000000       0.00000000       0.00000000       0.00000000       1.00000000       0.00000000       0.00000000       0.00000000       0.00000000       1.00000000
	c Actually it may not be as apparent in this case, since minkowski_metric is symmetric
	```
* Upto 7 dimensional arrays are allowed
* Functions should (need to) be defined outside the main program. The following is what worked on ```gfortran```
	```fortran
		program Rain
		implicit none

		real r, t, sum, rainfall
		integer m
		write(*, *) 'Enter scalar parameter''t'''
		read(*, *) t

		do 10 m = 1, 12
			r = rainfall(m,t)
			sum = sum + r
			write(*,*)  'Rainfall: ', r
	10  continue

		stop
		end

		real function rainfall(m, t)
	c      implicit none
	c      real t
	c      integer m
		rainfall = t**2 + 4*t - 10.0 + m**2
		if (rainfall .LT. 0.0) rainfall = 0.0
		write(*, *) 'Rainfall in month ', m, ' is ', rainfall
		return
		end
	```
* Functions return only one value. If you want to return more than one (or even none) use a subroutine instead.
* Length of a character string is defined using ```*```, e.g.
	```character*20 name``` for a string of 20 characters
* Subroutines must also be defined outside the main program. They are called using the ```call``` keyword
* Calls to functions/subroutines are by default *call-by-reference* type. So when one does ```call swap_nums(a, b)``` the memory addresses of ```a``` and ```b``` get passed and any changes to them inside ```swap_nums``` are also reflected in the main program. (It had to be this way for subroutines to actually work tbh).