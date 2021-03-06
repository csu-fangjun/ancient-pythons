"""Pseudo terminal utilities."""

# Bugs: No signal handling.  Doesn't set slave termios and window size.
#	Only tested on Linux.
# See:  W. Richard Stevens. 1992.  Advanced Programming in the 
#	UNIX Environment.  Chapter 19.
# Author: Steen Lumholt -- with additions by Guido.

from select import select
import os, FCNTL
import tty

STDIN_FILENO = 0
STDOUT_FILENO = 1
STDERR_FILENO = 2

CHILD = 0

def master_open():
	"""Open pty master and return (master_fd, tty_name).
	SGI and Linux/BSD version."""
	try:
		import sgi
	except ImportError:
		pass
	else:
		try:
		    tty_name, master_fd = sgi._getpty(FCNTL.O_RDWR, 0666, 0)
		except IOError, msg:
			raise os.error, msg
		return master_fd, tty_name
	for x in 'pqrstuvwxyzPQRST':
		for y in '0123456789abcdef':
			pty_name = '/dev/pty' + x + y
			try:
				fd = os.open(pty_name, FCNTL.O_RDWR)
			except os.error:
				continue
			return (fd, '/dev/tty' + x + y)
	raise os.error, 'out of pty devices'

def slave_open(tty_name):
	"""Open the pty slave and acquire the controlling terminal.
	Return the file descriptor.  Linux version."""
	# (Should be universal? --Guido)
	return os.open(tty_name, FCNTL.O_RDWR)

def fork():
	"""Fork and make the child a session leader with a controlling terminal.
	Return (pid, master_fd)."""
	master_fd, tty_name = master_open() 
	pid = os.fork()
	if pid == CHILD:
		# Establish a new session.
		os.setsid()

		# Acquire controlling terminal.
		slave_fd = slave_open(tty_name)
		os.close(master_fd)

		# Slave becomes stdin/stdout/stderr of child.
		os.dup2(slave_fd, STDIN_FILENO)
		os.dup2(slave_fd, STDOUT_FILENO)
		os.dup2(slave_fd, STDERR_FILENO)
		if (slave_fd > STDERR_FILENO):
			os.close (slave_fd)

	# Parent and child process.
	return pid, master_fd

def writen(fd, data):
	"""Write all the data to a descriptor."""
	while data != '':
		n = os.write(fd, data)
		data = data[n:]

def read(fd):
	"""Default read function."""
	return os.read(fd, 1024)

def copy(master_fd, master_read=read, stdin_read=read):
	"""Parent copy loop.
	Copies  
	  	pty master -> standard output	(master_read)
	  	standard input -> pty master	(stdin_read)"""
	while 1:
		rfds, wfds, xfds = select(
			[master_fd, STDIN_FILENO], [], [])
		if master_fd in rfds:
			data = master_read(master_fd)
			os.write(STDOUT_FILENO, data)
		if STDIN_FILENO in rfds:
			data = stdin_read(STDIN_FILENO)
			writen(master_fd, data)

def spawn(argv, master_read=read, stdin_read=read):
	"""Create a spawned process."""
	if type(argv) == type(''):
		argv = (argv,)
	pid, master_fd = fork()
	if pid == CHILD:
		apply(os.execlp, (argv[0],) + argv)
	mode = tty.tcgetattr(STDIN_FILENO)
	tty.setraw(STDIN_FILENO)
	try:
		copy(master_fd, master_read, stdin_read)
	except:
		tty.tcsetattr(STDIN_FILENO, tty.TCSAFLUSH, mode)
