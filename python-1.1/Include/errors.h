#ifndef Py_ERRORS_H
#define Py_ERRORS_H
#ifdef __cplusplus
extern "C" {
#endif

/***********************************************************
Copyright 1991, 1992, 1993, 1994 by Stichting Mathematisch Centrum,
Amsterdam, The Netherlands.

                        All Rights Reserved

Permission to use, copy, modify, and distribute this software and its 
documentation for any purpose and without fee is hereby granted, 
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in 
supporting documentation, and that the names of Stichting Mathematisch
Centrum or CWI not be used in advertising or publicity pertaining to
distribution of the software without specific, written prior permission.

STICHTING MATHEMATISCH CENTRUM DISCLAIMS ALL WARRANTIES WITH REGARD TO
THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS, IN NO EVENT SHALL STICHTING MATHEMATISCH CENTRUM BE LIABLE
FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

******************************************************************/

/* Error handling definitions */

void err_set PROTO((object *));
void err_setval PROTO((object *, object *));
void err_setstr PROTO((object *, char *));
object *err_occurred PROTO((void));
void err_get PROTO((object **, object **));
void err_clear PROTO((void));

/* Predefined exceptions */

extern DL_IMPORT object *AccessError;
extern DL_IMPORT object *AttributeError;
extern DL_IMPORT object *ConflictError;
extern DL_IMPORT object *EOFError;
extern DL_IMPORT object *IOError;
extern DL_IMPORT object *ImportError;
extern DL_IMPORT object *IndexError;
extern DL_IMPORT object *KeyError;
extern DL_IMPORT object *KeyboardInterrupt;
extern DL_IMPORT object *MemoryError;
extern DL_IMPORT object *NameError;
extern DL_IMPORT object *OverflowError;
extern DL_IMPORT object *RuntimeError;
extern DL_IMPORT object *SyntaxError;
extern DL_IMPORT object *SystemError;
extern DL_IMPORT object *SystemExit;
extern DL_IMPORT object *TypeError;
extern DL_IMPORT object *ValueError;
extern DL_IMPORT object *ZeroDivisionError;

/* Convenience functions */

extern int err_badarg PROTO((void));
extern object *err_nomem PROTO((void));
extern object *err_errno PROTO((object *));

extern void err_badcall PROTO((void));

extern object *err_getexc PROTO((void));

extern int sigcheck PROTO((void)); /* In sigcheck.c or signalmodule.c */

#ifdef __cplusplus
}
#endif
#endif /* !Py_ERRORS_H */
