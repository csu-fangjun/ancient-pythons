/* config.h.  NOT Generated automatically by configure.

This is a manually maintained version for the Win32 API */

/* Addtional stuff for NT */
#include <io.h>
/* Fairly standard from here!

/* Define if on AIX 3.
   System headers sometimes define this.
   We just want to avoid a redefinition error message.  */
#ifndef _ALL_SOURCE
/* #undef _ALL_SOURCE */
#endif

/* Define to empty if the keyword does not work.  */
/* #define const  */

/* Define if you have dirent.h.  */
/* #define DIRENT 1 */

/* Define to the type of elements in the array set by `getgroups'.
   Usually this is either `int' or `gid_t'.  */
/* #undef GETGROUPS_T */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef gid_t */

/* Define if your struct tm has tm_zone.  */
/* #undef HAVE_TM_ZONE */

/* Define if you don't have tm_zone but do have the external array
   tzname.  */
#define HAVE_TZNAME

/* Define if on MINIX.  */
/* #undef _MINIX */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef mode_t */

/* Define if you don't have dirent.h, but have ndir.h.  */
/* #undef NDIR */

/* Define to `long' if <sys/types.h> doesn't define.  */
/* #undef off_t */

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef pid_t */

/* Define if the system does not provide POSIX.1 features except
   with this defined.  */
/* #undef _POSIX_1_SOURCE */

/* Define if you need to in order for stat and other things to work.  */
/* #undef _POSIX_SOURCE */

/* Define as the return type of signal handlers (int or void).  */
#define RETSIGTYPE void

/* Define to `unsigned' if <sys/types.h> doesn't define.  */
/* #undef size_t */

/* Define if you have the ANSI C header files.  */
#define STDC_HEADERS 1

/* Define if you don't have dirent.h, but have sys/dir.h.  */
/* #undef SYSDIR */

/* Define if you don't have dirent.h, but have sys/ndir.h.  */
/* #undef SYSNDIR */

/* Define if you can safely include both <sys/time.h> and <time.h>.  */
/* #undef TIME_WITH_SYS_TIME */

/* Define if your <sys/time.h> declares struct tm.  */
#define TM_IN_SYS_TIME 1

/* Define to `int' if <sys/types.h> doesn't define.  */
/* #undef uid_t */

/* Define if the closedir function returns void instead of int.  */
/* #undef VOID_CLOSEDIR */

/* Define if your <unistd.h> contains bad prototypes for exec*()
   (as it does on SGI IRIX 4.x) */
/* #undef BAD_EXEC_PROTOTYPES */

/* Define if your compiler botches static forward declarations
   (as it does on SCI ODT 3.0) */
#define BAD_STATIC_FORWARD 1

/* Define if getpgrp() must be called as getpgrp(0)
   and (consequently) setpgrp() as setpgrp(0, 0). */
/* #undef GETPGRP_HAVE_ARGS */

/* Define this if your time.h defines altzone */
/* #define HAVE_ALTZONE */

/* Define if your compiler supports function prototypes */
#define HAVE_PROTOTYPES

/* Define if  you can safely include both <sys/select.h> and <sys/time.h>
   (which you can't on SCO ODT 3.0). */
/* #undef SYS_SELECT_WITH_SYS_TIME */

/* Define if you want to use SGI (IRIX 4) dynamic linking.
   This requires the "dl" library by Jack Jansen,
   ftp://ftp.cwi.nl/pub/dynload/dl-1.6.tar.Z.
   Don't bother on IRIX 5, it already has dynamic linking using SunOS
   style shared libraries */ 
/* #undef WITH_SGI_DL */

/* Define if you want to emulate SGI (IRIX 4) dynamic linking.
   This is rumoured to work on VAX (Ultrix), Sun3 (SunOS 3.4),
   Sequent Symmetry (Dynix), and Atari ST.
   This requires the "dl-dld" library,
   ftp://ftp.cwi.nl/pub/dynload/dl-dld-1.1.tar.Z,
   as well as the "GNU dld" library,
   ftp://ftp.cwi.nl/pub/dynload/dld-3.2.3.tar.Z.
   Don't bother on SunOS 4 or 5, they already have dynamic linking using
   shared libraries */ 
/* #undef WITH_DL_DLD */

/* Define if you want to compile in rudimentary thread support */
/* #undef WITH_THREAD */

/* Define if you want to use the GNU readline library */
/* #define WITH_READLINE 1 */

/* Define if you have clock.  */
#define HAVE_CLOCK

/* Define if you have ftime.  */
#define HAVE_FTIME

/* Define if you have getpeername.  */
/* #undef HAVE_GETPEERNAME */

/* Define if you have getpgrp.  */
/* #undef HAVE_GETPGRP */

/* Define if you have getpid.  */
/* #undef HAVE_GETPID */

/* Define if you have gettimeofday.  */
/* #undef HAVE_GETTIMEOFDAY */

/* Define if you have getwd.  */
/* #undef HAVE_GETWD */

/* Define if you have lstat.  */
/* #undef HAVE_LSTAT */

/* Define if you have nice.  */
/* #undef HAVE_NICE */

/* Define if you have readlink.  */
/* #undef HAVE_READLINK */

/* Define if you have select.  */
/* #undef HAVE_SELECT */

/* Define if you have setpgid.  */
/* #undef HAVE_SETPGID */

/* Define if you have setpgrp.  */
/* #undef HAVE_SETPGRP */

/* Define if you have setsid.  */
/* #undef HAVE_SETSID */

/* Define if you have siginterrupt.  */
/* #undef HAVE_SIGINTERRUPT */

/* Define if you have symlink.  */
/* #undef HAVE_SYMLINK */

/* Define if you have tcgetpgrp.  */
/* #undef HAVE_TCGETPGRP */

/* Define if you have tcsetpgrp.  */
/* #undef HAVE_TCSETPGRP */

/* Define if you have times.  */
/* #undef HAVE_TIMES */

/* Define if you have uname.  */
/* #undef HAVE_UNAME */

/* Define if you have waitpid.  */
/* #undef HAVE_WAITPID */

/* Define if you have the <dlfcn.h> header file.  */
/* #undef HAVE_DLFCN_H */

/* Define if you have the <fcntl.h> header file.  */
#define HAVE_FCNTL_H 1

/* Define if you have the <signal.h> header file.  */
#define HAVE_SIGNAL_H 1

/* Define if you have the <stdarg.h> header file.  */
#define HAVE_STDARG_H 1

/* Define if you have the <stdarg.h> prototypes.  */
#define HAVE_STDARG_PROTOTYPES

/* Define if you have the <stdlib.h> header file.  */
#define HAVE_STDLIB_H 1

/* Define if you have the <sys/audioio.h> header file.  */
/* #undef HAVE_SYS_AUDIOIO_H */

/* Define if you have the <sys/param.h> header file.  */
/* #define HAVE_SYS_PARAM_H 1 */

/* Define if you have the <sys/select.h> header file.  */
/* #define HAVE_SYS_SELECT_H 1 */

/* Define if you have the <sys/time.h> header file.  */
/* #define HAVE_SYS_TIME_H 1 */

/* Define if you have the <sys/times.h> header file.  */
/* #define HAVE_SYS_TIMES_H 1 */

/* Define if you have the <sys/un.h> header file.  */
/* #define HAVE_SYS_UN_H 1 */

/* Define if you have the <sys/utime.h> header file.  */
#define HAVE_SYS_UTIME_H 1

/* Define if you have the <sys/utsname.h> header file.  */
/* #define HAVE_SYS_UTSNAME_H 1 */

/* Define if you have the <thread.h> header file.  */
/* #undef HAVE_THREAD_H */

/* Define if you have the <unistd.h> header file.  */
/* #define HAVE_UNISTD_H 1 */

/* Define if you have the <utime.h> header file.  */
/* #define HAVE_UTIME_H 1 */

/* Define if you have the dl library (-ldl).  */
/* #undef HAVE_LIBDL */

/* Define if you have the mpc library (-lmpc).  */
/* #undef HAVE_LIBMPC */

/* Define if you have the nsl library (-lnsl).  */
#define HAVE_LIBNSL 1

/* Define if you have the seq library (-lseq).  */
/* #undef HAVE_LIBSEQ */

/* Define if you have the socket library (-lsocket).  */
#define HAVE_LIBSOCKET 1

/* Define if you have the sun library (-lsun).  */
/* #undef HAVE_LIBSUN */

/* Define if you have the termcap library (-ltermcap).  */
/* #undef HAVE_LIBTERMCAP */

/* Define if you have the termlib library (-ltermlib).  */
/* #undef HAVE_LIBTERMLIB */

/* Define if you have the thread library (-lthread).  */
/* #undef HAVE_LIBTHREAD */
