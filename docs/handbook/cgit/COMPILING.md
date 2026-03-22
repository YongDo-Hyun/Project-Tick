## Compile cgit

Building cgit involves building a proper version of Git. How to do this
depends on how you obtained the cgit sources:

a) Please go to cgit folder.

b) You first need to initialize and update the Git submodule if you are not init submodules.:

    $ git submodule init     # register the Git submodule in .git/config
    $ $EDITOR .git/config    # if you want to specify a different url for git
    $ git submodule update   # clone/fetch and checkout correct git version

b) If you're building from a cgit tarball, you can download a proper git
version like this:

    $ make get-git

When either a) and ( b) or c) ) has been performed, you can build and install cgit like
this:

    $ make
    $ sudo make install

This will install `cgit.cgi` and `cgit.css` into `/var/www/htdocs/cgit`. You
can configure this location (and a few other things) by providing a `cgit.conf`
file (see the Makefile for details).

If you'd like to compile without Lua support, you may use:

    $ make NO_LUA=1

And if you'd like to specify a Lua implementation, you may use:

    $ make LUA_PKGCONFIG=lua5.1

If this is not specified, the Lua implementation will be auto-detected,
preferring LuaJIT if many are present. Acceptable values are generally "lua",
"luajit", "lua5.1", and "lua5.2".
