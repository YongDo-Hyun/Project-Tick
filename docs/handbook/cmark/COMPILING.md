## Compile and Install cmark

Building the C program (`cmark`) and shared library (`libcmark`)
requires [cmake].  If you modify `scanners.re`, then you will also
need [re2c] \(>= 0.14.2\), which is used to generate `scanners.c` from
`scanners.re`.  We have included a pre-generated `scanners.c` in
the repository to reduce build dependencies.

If you have GNU make, you can simply `make`, `make test`, and `make
install`.  This calls [cmake] to create a `Makefile` in the `build`
directory, then uses that `Makefile` to create the executable and
library.  The binaries can be found in `build/src`.  The default
installation prefix is `/usr/local`.  To change the installation
prefix, pass the `INSTALL_PREFIX` variable if you run `make` for the
first time: `make INSTALL_PREFIX=path`.

For a more portable method, you can use [cmake] manually. [cmake] knows
how to create build environments for many build systems.  For example,
on FreeBSD:

    cmake -S . -B build  # optionally: -DCMAKE_INSTALL_PREFIX=path
    cmake --build build  # executable will be created as build/src/cmark
    ctest --test-dir build
    cmake --install build

Or, to create Xcode project files on OSX:

    cmake -S . -B build -G Xcode
    open build/cmark.xcodeproj

The GNU Makefile also provides a few other targets for developers.
To run a benchmark:

    make bench

For more detailed benchmarks:

    make newbench

To run a test for memory leaks using `valgrind`:

    make leakcheck

To reformat source code using `clang-format`:

    make format

To run a "fuzz test" against ten long randomly generated inputs:

    make fuzztest

To do a more systematic fuzz test with [american fuzzy lop]:

    AFL_PATH=/path/to/afl_directory make afl

Fuzzing with [libFuzzer] is also supported. The fuzzer can be run with:

    make libFuzzer

To make a release tarball and zip archive:

    make archive

## Compile and Install cmark (Windows)

To compile with MSVC and NMAKE:

    nmake /f Makefile.nmake

You can cross-compile a Windows binary and dll on linux if you have the
`mingw32` compiler:

    make mingw

The binaries will be in `build-mingw/windows/bin`.
