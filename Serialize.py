class Boolean(object) :
	""" Class representing PHP boolean """
	def __init__(self, value) :
		if value != 0 and value != 1 :
			raise ValueError("Invalid boolean value")
		self.value = value

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'b:%d;' % self.value

class Null(object) :
	""" Class representing PHP null """
	def __init__(self) :
		pass

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'N;'

class Integer(object) :
	""" Class representing PHP integer """
	def __init__(self, value) :
		if not isinstance(value, int) :
			raise ValueError("Invalid integer value")
		self.value = value

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'i:%d;' % self.value

class Double(object) :
	""" Class representing PHP double """
	def __init__(self, value) :
		if not isinstance(value, float) :
			raise ValueError("Invalid double value")
		self.value = value

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'd:%f' % self.value

class String(object) :
	""" Class representing PHP string """
	def __init__(self, value) :
		if not isinstance(value, str) :
			raise ValueError("Invalid string value")
		self.value = value

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 's:%d:"%s"' % (
			len(self.value),
			self.value
			)

class Array(object) :
	""" Class representing PHP array """
	def __init__(self, arr) :
		if isinstance(arr, dict) :
			self.arr = arr
		elif isinstance(arr, list) :
			self.arr = {}
			for i in xrange(len(arr)) :
				self.arr[Integer(i)] = arr[i]
		else :
			raise ValueError("Invalid array value")

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'a:%d:{%s}' % (
			len(self.arr), 
			''.join(
				[str(k)+str(v) for k,v in self.arr.iteritems()]
			))

class Property(object) :
	""" Class representing a PHP object field """
	def __init__(self, name, value) :
		self.name	= String(name)
		self.value	= value

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return '%s;%s' % (
			str(self.name),
			str(self.value)
			)

class Object(object) :
	""" Class representing a PHP object """
	def __init__(self, name) :
		self.name 	= name
		self.props 	= []

	def add_publ(self, name, value) :
		""" Adds a public field """
		self.props.append(
			Property(name, value)
		)	
		return self
	
	def add_prot(self, name, value) :
		""" Adds a protected field """
		self.props.append(
			Property('\x00*\x00%s' % name, value)
		)
		return self
	
	def add_priv(self, name, value) :
		""" Adds a private field """
		self.props.append(
			Property('\x00%s\x00%s' % (self.name, name), value)
		)
		return self

	def __repr__(self) :
		return str(self)
	def __str__(self) :
		return 'O:%d:"%s":%d:{%s};' % (
			len(self.name),
			self.name,
			len(self.props),
			''.join(
				[str(prop) for prop in self.props]
			))

if __name__ == '__main__' :
	o = Object('Obj').add_priv(
			'priv', Integer(2)
		).add_prot(
			'prot', Integer(1)
		).add_publ(
			'publ', Integer(0) 
		).add_publ(
			'arr', Array([Integer(1), Integer(2), Integer(3)]
		))
	print(o)
