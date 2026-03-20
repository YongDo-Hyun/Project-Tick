README_ami.txt for version 7.4 of uVim: Micro Vi IMproved.

This file explains the installation of uVim on Amiga systems.
See README.txt for general information about uVim.


Unpack the distributed files in the place where you want to keep them.  It is
wise to have a "vim" directory to keep your vimrc file and any other files you
change.  The distributed files go into a subdirectory.  This way you can
easily upgrade to a new version.  For example:

  dh0:editors/vim		contains your vimrc and modified files
  dh0:editors/vim/vim54		contains the uVim version 5.4 distributed files
  dh0:editors/vim/vim55		contains the uVim version 5.5 distributed files

You would then unpack the archives like this:

  cd dh0:editors
  tar xf t:vim60bin.tar
  tar xf t:vim60rt.tar

Set the $VIM environment variable to point to the top directory of your uVim
files.  For the above example:

  set VIM=dh0:editors/vim

uVim version 5.4 will look for your vimrc file in $VIM, and for the runtime
files in $VIM/vim54.  See ":help $VIM" for more information.

Make sure the uVim executable is in your search path.  Either copy the uVim
executable to a directory that is in your search path, or (preferred) modify
the search path to include the directory where the uVim executable is.
