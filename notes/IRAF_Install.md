## A bit of trouble I had installing IRAF on Manjaro

### Update (2022)
I installed IRAF, X11IRAF and MOOG ([this version](https://github.com/MingjieJian/moog_nosm)) on ArcoLinux this January, and it all went smoothly. Perhaps many of the issues I had complained about got patched. But this is good news, right?(!)

### IRAF
Firstly, make sure you extract the ```.tar.gz``` properly. One problem that I faced was that when I extracted a ```.zip``` some of the files which were supposed to be symlinks (symbolic links) turned out to be normal text files (which was wrong!).

And don't download the 2018 snapshot release, clone the GitHub repository itself. The reason being there are patches that were made in 2020 that fixed an error I got

```bash
/usr/bin/ld: xppcode.o:/home/aayush/Documents/iraf-2.16.1-2018.11.01/unix/boot/spp/xpp/xppcode.c:109: multiple definition of `errflag'; xppmain.o:/home/aayush/Documents/iraf-2.16.1-2018.11.01/unix/boot/spp/xpp/xppmain.c:21: first defined here
collect2: error: ld returned 1 exit status
make: *** [Makefile:19: sysgen] Error 1
```

Fortunately, this error [had been discussed in an issue](https://github.com/iraf-community/iraf/issues/110) and one of the maintainers had patched it.

After running the tests upon installation, I got
```bash
Test summary:     127 passed
      2 skipped
      1 xfailed
```
At first sight the ```1 xfailed``` concerned me but then I figured out the 'x' in xfailed is for 'e**x**pected' failure. So this is all good.

### X11IRAF
#### Note:
You need to have IRAF installed first, before installing X11IRAF.

Now assuming IRAF is installed, let's look at what troubles I ran into:
While running ```make```
I got errors such as
```c
ism.c:15:10: fatal error: tcl/tcl.h: No such file or directory
   15 | #include <tcl/tcl.h>
      |          ^~~~~~~~~~~
compilation terminated.
```

I understood what the problem was from [this askubuntu thread](https://askubuntu.com/questions/366909/error-tcl-h-not-found-no-such-file-or-directory). In Ubuntu, ```tcl``` is placed in ```/usr/include/tcl``` and not ```/usr/include```. The package release is likely configured for Ubuntu-like distros, but on Arch (and consequently, in Manjaro) it would be in ```/usr/include/``` (at least that was the case for me). So I edited the source code of the files I got these errors in -- replacing ```#include <tcl/tcl.h>``` to ```#include <tcl.h>```. The files I had to edit in the X11IRAF source were
* ximtool/ism.c
* ximtool/ism_wcspix.c
* ximtool/xim_client.c
* obm/ObmP.h (due to Obm.c)

And then it couldn't find a command ```mkpkg```. This led to the error
```bash
cd clients && mkpkg || true
/bin/sh: line 1: mkpkg: command not foun
```
Apparently, ```mkpkg``` is a command used to install IRAF packages. One needs to have IRAF installed first.

That would get rid of that error.

Then I had this error after having the above resolved.
```
Warning: file `x_ism.o' not found
Warning: file `libpkg.a' not found
gcc: error: libmain.o: No such file or directory
gcc: error: libex.a: No such file or directory
gcc: error: libsys.a: No such file or directory
gcc: error: libvops.a: No such file or directory
gcc: error: libos.a: No such file or directory
gcc: error: libVO.a: No such file or directory
```
But it faded away when I recompiled again a bit later. I'm not sure why; I wonder if it had to do with me being able to fix the ```$iraf``` environment variable correctly.

After that, ```make``` gave me the following output

```bash
(base) [aayush@aayush-tuf x11iraf-2.0-2020.06.15]$ make
make -C xgterm
make[1]: Entering directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xgterm'
make[1]: Nothing to be done for 'all'.
make[1]: Leaving directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xgterm'
make -C ximtool
make[1]: Entering directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool'
cd clients && mkpkg || true
warning: library `libpkg.a' not found
xc -c -w idxstr.x ism.x wcsgfterm.x
ar r /home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool/clients/libpkg.a idxstr.o ism.o wcsgfterm.o
ar: creating /home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool/clients/libpkg.a
xc -c -w t_wcspix.x wcimage.x wcmef.x wcmspec.x wcunknown.x
ar r /home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool/clients/libpkg.a t_wcspix.o wcimage.o wcmef.o wcmspec.o wcunknown.o
ranlib libpkg.a
Updated 8 files in libpkg.a
xc -c -w x_ism.x
xc -Nz   -z x_ism.o libpkg.a -o ism_wcspix.e -lds -lxtools -liminterp -lslalib
make[1]: Leaving directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool'
```
And then when I did ```# make install```
```bash
(base) [aayush@aayush-tuf x11iraf-2.0-2020.06.15]$ sudo make install
[sudo] password for aayush: 
make -C xgterm
make[1]: Entering directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xgterm'
make[1]: Nothing to be done for 'all'.
make[1]: Leaving directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xgterm'
make -C ximtool
make[1]: Entering directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool'
cd clients && mkpkg || true
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
cannot translate logical name `hlib'envinit: cannot open `'
Warning, mkpkg line 0: cannot open `hlib$mkpkg.inc'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
Warning, mkpkg line 13: dependency file `<config.h>' not found
Warning, mkpkg line 13: dependency file `<mach.h>' not found
Warning, mkpkg line 13: dependency file `<xwhen.h>' not found
Subdirectory lib is up to date
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
Warning, mkpkg line 10: dependency file `<ctype.h>' not found
Warning, mkpkg line 10: dependency file `<time.h>' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
os.zgtenv: cannot follow link `/usr/include/iraf.h'
os.zgtenv: cannot follow link `/usr/include/iraf.h'
environment variable `iraf' not found
Warning, mkpkg line 12: dependency file `ctype.h' not found
Warning, mkpkg line 12: dependency file `<imhdr.h>' not found
Warning, mkpkg line 12: dependency file `<imio.h>' not found
Warning, mkpkg line 12: dependency file `<math.h>' not found
Warning, mkpkg line 12: dependency file `time.h' not found
Warning, mkpkg line 12: dependency file `<mwset.h>' not found
Warning, mkpkg line 12: dependency file `<pkg/skywcs.h>' not found
Warning, mkpkg line 15: dependency file `ctype.h' not found
Subdirectory wcspix is up to date
Library libpkg.a is up to date
/bin/bash: -c: line 1: syntax error near unexpected token `null'
/bin/bash: -c: line 1: `xc (null)   -z x_ism.o libpkg.a -o ism_wcspix.e -lds -lxtools -liminterp -lslalib'
Warning, mkpkg line 3: module `relink' not found or returned error
make[1]: Leaving directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/ximtool'
make -C xtapemon
make[1]: Entering directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xtapemon'
cc    -c -o classnames.o classnames.c
cc    -c -o types.o types.c
cc    -c -o xtapemon.o xtapemon.c
cc  -o xtapemon classnames.o types.o xtapemon.o -lXaw3d -lXmu -lXt -lX11 -lm
make[1]: Leaving directory '/home/aayush/Documents/x11iraf-2.0-2020.06.15/xtapemon'
mkdir -p /usr/local/bin /usr/local/man/man1
install -m755 xgterm/xgterm /usr/local/bin
install -m755 xgterm/xgterm.man /usr/local/man/man1/xgterm.1
tic xgterm/xgterm.terminfo
install -m755 ximtool/ximtool /usr/local/bin
install -m755 ximtool/ximtool.man /usr/local/man/man1/ximtool.1
if [ -x ximtool/clients/ism_wcspix.e ] ; then \
    install -m755 ximtool/clients/ism_wcspix.e /usr/local/bin ; \
fi
```