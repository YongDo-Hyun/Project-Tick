/* vi:set ts=8 sts=4 sw=4:
 *
 * VIM - Micro Vi IMproved	by Bram Moolenaar
 *
 * Do ":help uganda"  in uVim to read copying and usage conditions.
 * Do ":help credits" in uVim to see a list of people who contributed.
 * See README.txt for an overview of the uVim source code.
 */

/* Visual Studio 2005 has 'deprecated' many of the standard CRT functions */
#if _MSC_VER >= 1400
# define _CRT_SECURE_NO_DEPRECATE
# define _CRT_NONSTDC_NO_DEPRECATE
#endif

/* cproto fails on missing include files */
#ifndef PROTO
# include <io.h>
#endif
