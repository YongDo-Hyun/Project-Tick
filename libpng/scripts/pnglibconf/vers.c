/* vers.c - define format of libpng.vers
 *
 * Copyright (c) 2011-2014 Glenn Randers-Pehrson
 *
 * This code is released under the libpng license.
 * For conditions of distribution and use, see the disclaimer
 * and license in png.h
 */

#define PNG_EXPORTA(type, name, args, attributes)\
        PNG_DFN " @" SYMBOL_PREFIX "@@" name "@;"

PNG_DFN "@" PNGLIB_LIBNAME "@ {global:"

#include "../../png.h"
PNG_DFN "  ptpng_adler32;"
PNG_DFN "  ptpng_crc32;"
PNG_DFN "  ptpng_deflate;"
PNG_DFN "  ptpng_deflateInit2_;"
PNG_DFN "  ptpng_deflateReset;"
PNG_DFN "  ptpng_inflate;"
PNG_DFN "  ptpng_inflateInit2_;"
PNG_DFN "  ptpng_inflateReset;"
PNG_DFN "  ptpng_inflateReset2;"

PNG_DFN "local: *; };"
