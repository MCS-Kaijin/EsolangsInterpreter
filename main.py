import ui


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

interpreters = {
                'Brainf---': bf
                }


gui = ui.load_view('main')

def choose_language(sender):
	global language
	language = sender.items[sender.selected_row]
	gui.name = language
	gui['tableview1'].alpha = 0

gui['tableview1'].data_source = ui.ListDataSource(['Brainf---'])
gui['tableview1'].delegate = ui.ListDataSource(['Brainf---'])
gui['tableview1'].delegate.action = choose_language

def intp(sender):
	global code, inp
	code = gui['textview1'].text
	inp = gui['textfield1'].text
	out = interpreters[language]()
	gui['textview1'].end_editing()
	gui['label1'].text = out
gui['button1'].action = intp

gui.present()
