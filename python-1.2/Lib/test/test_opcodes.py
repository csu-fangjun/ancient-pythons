# Python test set -- part 2, opcodes

from test_support import *


print '2. Opcodes'
print 'XXX Not yet fully implemented'

print '2.1 try inside for loop'
n = 0
for i in range(10):
	n = n+i
	try: 1/0
	except NameError: pass
	except ZeroDivisionError: pass
	except TypeError: pass
	try: pass
	except: pass
	try: pass
	finally: pass
	n = n+i
if n <> 90:
	raise TestFailed, 'try inside for'


print '2.2 raise class exceptions'

class AClass: pass
class BClass(AClass): pass
class CClass: pass

try: raise AClass()
except: pass

try: raise AClass()
except AClass: pass

try: raise BClass()
except AClass: pass

try: raise BClass()
except CClass: raise TestFailed
except: pass

a = AClass()
b = BClass()

try: raise AClass, b
except BClass, v: raise TestFailed
except AClass, v:
	if v != b: raise TestFailed


try: raise b
except AClass, v:
	if v != b: raise TestFailed

try:  raise BClass, a
except TypeError: pass
