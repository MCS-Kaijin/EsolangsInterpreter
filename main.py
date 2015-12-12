import ui
import re
import random

# to appease the finicky UnboundLocalError
dark_output = ''

# python switch statement
class switch(object):
	def match(self, *args):
		if self.fall or not args:
			return True
		elif self.value in args:
			self.fall = True
			return True
		else:
			return False
	
	def __init__(self, value):
		self.value = value
		self.fall = False
	
	def __iter__(self):
		yield self.match
		raise StopIteration


code, inp, language = None, None, None


# interpreter functions
def bf():
	global code, inp
	tape = []
	tpos = 255
	ipos = 0
	tmp = []
	for i in range(0, 255*2):
		tape.append(0)
	output = ''
	c = 0
	while c < len(code):
		char = code[c]
		for case in switch(char):
			if case('>'):
				tpos += 1
				break
			elif case('<'):
				tpos -= 1
				break
			elif case('+'):
				try: tape[tpos] += 1
				except: tape[tpos] = 1
				break
			elif case('-'):
				try: tape[tpos] -= 1
				except: tape[tpos] = -1
				break
			elif case('.'):
				output += chr(tape[tpos])
				break
			elif case('['):
				if tape[tpos] == 0:
					while not code[c] == ']':
						c += 1
				else:
					tmp.append(c)
				break
			elif case(']'):
				if not tape[tpos] == 0: c = tmp.pop()-1
				break
			elif case(','):
				try: tape[tpos] = ord(inp[ipos])
				except: tape[tpos] = 0
				ipos += 1
				break
		c += 1
	return output

# http://www.esolangs.org/wiki/Dark
def dark():
	global code, inp, dark_out
	control_space, world_block, voicelist = [], [], []
	obj_types = {}
	dark_out = ''
	
	class sign(object):
		def __init__(self, name):
			self.name = name
			self.value = None
			self.funcs = {
			              'scrawl': self.scrawl,
			              'read': self.red,
			              'tear': self.tear,
			              'observe': self.observe,
			              'steal': self.steal
			              }
			control_space.append(self)
		
		def scrawl(self, args):
			if args[0] == '"':
				args.pop()
				args.remove('"')
				try: self.value += ' '+' '.join(args)
				except: self.value = ' '.join(args)
			elif args[0] == '#':
				self.value = int(args[1])
			else:
				string = ''
				for var in world_block:
					if var.name == args[0]:
						string = var.value
						break
				try: self.value += string
				except: self.value = string
		
		def red(self, args=['']):
			voicelist.append(self.value)
			if args[0] == '~': self.value = None
		
		def tear(self, args=[1]):
			v = self.value
			v = list(v)
			v.reverse()
			for i in range(0, int(args[0])):
				v.pop()
			v.reverse()
			self.value = ''.join(v)
		
		def observe(self, args):
			for var in world_block:
				if var.name == args[0]:
					try:
						int(var.value)
						self.value = str(var.value)
					except:
						self.value = var.value[0]
		
		def steal(self, args):
			for var in world_block:
				if var.name == args[0]:
					var.value = self.value[0]
					self.tear()
	
	class stalker(object):
		def __init__(self, name):
			self.name = name
			self.initialized = False
			self.state = 'distant'
			self.buffer = ''
			self.inp_pos = 0
			self.funcs = {
			              'stalk': self.stalk,
			              'control': self.control,
			              'echo': self.echo,
			              'personal': self.personal,
			              'distant': self.distant,
			              'paracusia': self.paracusia,
			              'action': self.action
			              }
			control_space.append(self)
		
		def stalk(self):
			self.initialized = True
		
		def control(self, args):
			if not self.initialized:
				dark_output = 'Murphy\'s Law is working correctly.'
				return
			for var in world_block:
				if args[0] == '#' and var.name == args[1]:
					var.value = int(inp)
					return
				if var.name == args[0]:
					if not self.inp_pos >= len(inp):
						var.value = ord(inp[self.inp_pos])
						self.inp_pos += 1
					else:
						return
		
		def echo(self):
			global dark_output
			if not self.initialized:
				dark_output = 'Murphy\'s Law is working correctly.'
				return
			if self.state == 'distant': self.buffer += voicelist.pop()
			else: dark_output += voicelist.pop()
		
		def personal(self):
			self.state = 'personal'
		
		def distant(self):
			self.state = 'distant'
		
		def paracusia(self):
			global dark_output
			dark_output += self.buffer
			self.buffer = ''
		
		def action(self, args):
			global dark_output
			if not self.initialized:
				dark_output = 'Murphy\'s Law is working correctly'
				return
			for var in world_block:
				if args[0] == '#' and var.name == args[1]:
					if self.state == 'distant': self.buffer += str(var.value)
					else: dark_output += str(var.value)
				if var.name == args[0]:
					print args[len(args)-1]
					if self.state == 'distant': self.buffer += chr(var.value)
					else: dark_output += chr(var.value)
	
	class entropy(object):
		def __init__(self, name):
			self.name = name
			self.value = None
			self.corpses = []
			self.huvaloo = 0
			self.funcs = {
			              'choice': self.choice,
			              'balance': self.balance,
			              'corpse': self.corpse,
			              'stumble': self.stumble,
			              'illusion': self.illusion
			              }
			control_space.append(self)
		
		def choice(self, args):
			val1, val2 = None, None
			try: 
				val1 = int(args[0])
			except:
				for var in world_block:
					if var.name == args[0]: val1 = int(var.value)
			try: 
				val2 = int(args[2])
			except:
				for var in world_block:
					if var.name == args[2]: val2 = int(var.value)
			for case in switch(args[1]):
				if case('=') or case('=='): self.value = val1 == val2
				if case('>'): self.value = val1 > val2
				elif case('<'): self.value = val1 < val2
				elif case('>='): self.value = val1 >= val2
				elif case('<='): self.value = val1 <= val2
				if case('!=') or case('<>'): self.value = val1 != val2
			if not self.value:
				w = args[3]
				print w
				return w
				while not code.split('\n')[w] == self.name+'$balance' and not code.split('\n')[w] == self.name+'$reprogram': w += 1
				return w
		
		def balance(self, i):
			if self.value:
				while not code.split('\n')[i] == self.name+'$reprogram': i += 1
				return i
		
		def corpse(self, args):
			self.corpses.append(self.corpseObj(args[0], args[1]))
		
		def stumble(self, args):
			for crps in self.corpses:
				if crps.name == args[0]: return crps.line_number
		
		def illusion(self, args):
			for crps in self.corpses:
				if crps.name == args[0]: self.corpses.remove(crps)
		
		class corpseObj(object):
			def __init__(self, name, line_number):
				self.name, self.line_number = name, line_number
				
	
	class manipulator(object):
		def __init__(self, name):
			self.name = name
			self.var_slots = 1024
			self.funcs = {
			              'manufacture': self.manufacture,
			              'suicide': self.suicide,
			              'kill': self.suicide,
			              'void': self.void,
			              'genocide': self.genocide,
			              'omnicide': self.omnicide,
			              'chaos': self.chaos,
			              'set': self.set,
			              'add': self.add,
			              'subtract': self.subtract,
			              'multiply': self.multiply,
			              'divide': self.divide
			              }
			control_space.append(self)
		
		def manufacture(self, args):
			if self.var_slots <= 0: return
			if args[3] == 'master':
				self.variable(self, args[0], args[1], args[2], args[3], None)
			else:
				self.variable(self, args[0], args[1], args[2], args[3], args[4])
			self.var_slots -= 1
		
		def suicide(self, args):
			for var in world_block:
				if var.name == args[0] and var.manip == self: world_block.remove(var)
		
		def void(self):
			self.var_slots = 1024
		
		def genocide(self, args):
			for var in world_block:
				if var.manip == self and var.disposition == args[0]: world_block.remove(var)
		
		def omnicide(self):
			for var in world_block:
				if var.manip == self: world_block.remove(var)
		
		def chaos(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]:
					var.value = random.randint(0, (2^int(var.size))-1)
		
		def set(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]: var.value = args[1]
		
		def add(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]: var.value = int(args[1]) + int(args[2])
		
		def subtract(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]: var.value = int(args[1]) - int(args[2])
		
		def multiply(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]: var.value = int(args[1]) * int(args[2])
		
		def divide(self, args):
			for var in world_block:
				if var.manip == self and var.name == args[0]: var.value = int(args[1]) / int(args[2])
		
		class variable(object):
			def __init__(self, manip, name, disposition, size, state, master):
				self.manip, self.name, self.disposition, self.size, self.state, self.master = manip, name, disposition, size, state, master
				self.value = 0
				world_block.append(self)
	
	class hell(object):
		def twist(self, args):
			obj_types[args[0]](args[1])
		
		def consume(self, args):
			for item in control_space:
				if item.name == args[0]: control_space.remove(item)
		
		def empty(self):
			for item in control_space:
				if not item == self: control_space.remove(item)
		
		def brek(self, errortext=['Murphy\'s Law is working correctly.']):
			global dark_output
			dark_output = errortext[0]
			return
		
		def apocalypse(self):
			for item in control_space:
				control_space.remove(item)
			for item in world_block:
				world_block.remove(item)
			for item in voicelist:
				voicelist.remove(item)
		
		def __init__(self, name):
			self.name = name
			control_space.append(self)
			self.funcs = {
			              'twist': self.twist,
			              'consume': self.consume,
			              'empty': self.empty,
			              'break': self.brek,
			              'apocalypse': self.apocalypse
			              }
	
	obj_types = {
	              'hell': hell,
	              'manipulator': manipulator,
	              'stalker': stalker,
	              'sign': sign,
	              'entropy': entropy
	              }
	
	i = 0
	while i < len(code.split('\n')):
		line = code.split('\n')[i]
		tmp = re.match((r'\+(?P<objname>[\w]+) hell'), line)
		if tmp: hell(tmp.group('objname'))
		
		tmp = re.match((r'(?P<objname>[^$]+)\$(?P<func_name>[\w]+) ?(?P<params>.*)'), line)
		if tmp:
			for item in control_space:
				if item.name == tmp.group('objname'):
					for thing in item.funcs.items():
						if thing[0] == tmp.group('func_name'):
							params = tmp.group('params').split(' ')
							try:
								if params == [u'']: params = i
								else: params.append(i)
								tmp1 = item.funcs[tmp.group('func_name')](params)
								if tmp1: i = tmp1
							except TypeError as e:
								item.funcs[tmp.group('func_name')]()
		i += 1
	return dark_output



interpreters = {
                'Brainf---': bf,
                'Dark': dark
                }


gui = ui.load_view('main')

def choose_language(sender):
	global language
	language = sender.items[sender.selected_row]
	gui.name = language
	gui['tableview1'].alpha = 0

gui['tableview1'].data_source = ui.ListDataSource(['Brainf---', 'Dark'])
gui['tableview1'].delegate = ui.ListDataSource(['Brainf---', 'Dark'])
gui['tableview1'].delegate.action = choose_language

def intp(sender):
	global code, inp
	code = gui['textview1'].text
	inp = gui['textfield1'].text
	out = interpreters[language]()
	gui['textview1'].end_editing()
	gui['label1'].text = out
gui['button1'].action = intp

gui['textview1'].autocapitalization_type = ui.AUTOCAPITALIZE_NONE

gui.present()
