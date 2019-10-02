import random
import math
import os
from string import Template


class function_composition(object):
	"""
	Summary: function composition object that 
	organizes our logic

	Parameters:
	string path: path to directory to write file

	string file_name: file name to write the final results to

	simple_func function_list: a list of simple_func objects to pick from

	int num_functions: number of functions to pick from function_list
						if num_functions > len(function_list) that means
						repetition is allowed
	
	int num_choices: number of choices to present to the user

	bool allow_repetition: whether to allow picking the same function from
						function_list more than once
	"""
	def __init__(self, path, file_name, function_list, num_functions, 
			num_choices, allow_repetition=False):
		assert num_functions > 0
		assert num_choices > 1
		self.path = path
		self.file_name = file_name
		self.function_list = function_list
		self.num_functions = num_functions
		self.choices = num_choices
		self.allow_repetition = allow_repetition

		file_path = os.path.join(path, file_name)
		try:
			self.file = open(file_path, 'w+')
		except OSError:
			self.file = None
			print(f"Cannot open: {file_path} to output file")
			return
	
	def __del__(self):
		if self.file:
			self.file.close()
	
	def __pick_func(self):
		if self.allow_repetition:
			return random.choices(self.function_list, k=self.num_functions)
		return random.sample(self.function_list, k=self.num_functions)

	@staticmethod
	def simple_func_str(fn_list):
		so_far = fn_list[-1].function_str
		for i in range(len(fn_list) - 2, -1, -1):
			so_far = fn_list[i].function_concat_str(so_far)
		return so_far
	
	@staticmethod
	def func_expression_str(fn_list):
		so_far = fn_list[-1].function_expr
		for i in range(len(fn_list) - 2, -1, -1):
			so_far = fn_list[i].function_concat_expr(fn_list[i + 1])
		return so_far



class simple_func(object):
	"""
	Summary: a simple function that takes in one parameter and
			does a single function

	Parameters:
	string name: name of function e.g. F, G, W etc.

	string arg_name: name of input e.g. x, y, z

	string operation: a single operation e.g. '+', '-', '*', '^' etc

	int/float number: a single number, either integer or float
	"""

	# operations that require paratheses when enclosed in another function
	# 	e.g. if F(x) = x + 1, G(x) = x^2. Then F(G(x)) = (x + 1)^2 
	#	where x + 1 needs to be enclosed in paratheses
	__need_enclose_ops = ('+', '-')

	__simple_ops = ('+', '-', '*', '^', '%')

	def __init__(self, name, arg_name, operation, number):
		self.name = name
		self.arg_name = arg_name
		self.operation = operation
		self.number = number 
		self.need_enclosure = self.operation in self.__need_enclose_ops
		self.function_str = f"{self.name}({self.arg_name})"
		self.function_expr = self.__function_expr(arg_name, operation, number)
		
	def function_concat_str(self, param):
		return f"{self.name}({param})"


	def function_concat_expr(self, nest_fn):
		if nest_fn.need_enclosure:
			new_arg = f"({nest_fn.function_expr})"
		else:
			new_arg = nest_fn.function_expr
		return self.__function_expr(new_arg, self.operation, self.number)


	def __function_expr(self, arg_name, operation, number):
		if operation in self.__simple_ops:
			return f"{name}{operation}{number}"
		elif number is None and arg_name is None:
			return f"{operation}()"
		elif number is None:
			return f"{operation}({arg_name})"
		elif arg_name is None:
			return f"{operation}({number})"
		else:
			raise RuntimeError("simple_func class does not support complex functions")



#right now this always assumes there will be one exponential and  two linear  fns
#this is the  way it  is in the example problem
#this can probably be abstracted more but I just started off like this 
exponentials = [2,3,4] #possible exponetial factors  
symbols = ["+", "-", "*"] #possible expoenential  fns
html_file = open(r"test_html_write.html", "r+") #may need to change file path to work



exp = random.choice(exponentials) #sets the  exponential
lin1 = random.choice(symbols) #choses the first linear fn (i.e.  the + in x +  7)
lin2 = random.choice(symbols)  
num1 = random.randrange(1,10) #choses the first  linear  value (i.e. the  7 in x+7)
num2 = random.randrange(1,10)

#creates each of the  fns, right now it always  sets x to be the exponential
#and g&h to be the lienar so this should be abstracted as well
f = "x <sup>" + str(exp) + "</sup>" 
g = "x" + lin1 + str(num1)
h = "x" + lin2 + str(num2)

correct = "" #ignore for now

fns = [[f],[g],[h]] #creates a list of the fns (set as lists so it can be shuffled bc I couldnt shuffle string objects)

#sets the func_comp order (i.e. F(G(x)) vs (G(F(x))))
def set_order(lst):
	random.shuffle(lst)
	return lst

#sets the goal or final blank on HTML using the determined order from set_order
def substitue(lst):
	print("Input list:", lst)
	full_lst = [x[0] for x in lst]
	print(full_lst)
	final_comp = full_lst[0]
	
	final_comp = final_comp.replace("x", "(" + full_lst[1] + ")")
	
	final_comp =final_comp.replace("x", "(" + full_lst[2] + ")")
	
	return final_comp

#create 5 randomized unique possible solutions
def create_solns(lst):
	sols = []
	temp = "x"
	print("Sols input original:" , lst)
	mod_lst = list(lst)

	while len(sols) < 5:
		for i in mod_lst:
			if i == [f]:
				temp = temp.replace("x", "F(x)")
			elif i == [g]:
				temp = temp.replace("x", "G(x)")
			elif i == [h]:
				temp = temp.replace("x", "H(x)")

		if temp not in sols:
			sols.append(temp)	
		temp = "x"
		random.shuffle(mod_lst)
	correct = sols[0]
	random.shuffle(sols)
	return sols

	
#calls set_order & orders the fns
ordered_fns = set_order(fns)

#creates HTML for the functions
blank_1 = "\n<strong>F(x)</strong> = " + f + "\n<strong>G(x)</strong>=  " + g + "\n<strong>H(x)</strong> = " + h

#creates entire html for the rest of page
template_start = '<html><head><script type="">'
template_js=	'var form = document.querySelector("form");var log = document.querySelector("#log"); form.addEventListener("submit", function(event) {var data = new FormData(form); var output = "";for (const entry of data) {output = output + entry[0] + "=" + entry[1] + "\r"};log.innerText = output;event.preventDefault();}, false)</script></head>'
template_body = '<body><p>If we were given three functions: </p ><p style="text-align: center"> {0} </p> <p>... and you wanted to calculate:</p><p style="text-align: center"> {1} </p> <p>...how would you compse the <a></a> functions to get that? (select ONE)</p>'
template_form =	'<form><div><input type="radio" id="funcComp1"name="funcComp" value="a"><label for="funcComp1">{0}</label><input type="radio" id="funcComp2"name="funcComp" value="b"><label for="funcComp2">{1}</label><input type="radio" id="funcComp3"name="funcComp" value="c"><label for="funcComp3">{2}</label><input type="radio" id="funcComp4"name="funcComp" value="d"><label for="funcComp4">{3}</label><input type="radio" id="funcComp5"name="funcComp" value="e"><label for="funcComp5">{4}</label></div></form>'
template_submit = '<pre id="log"></pre><button>Submit</button>'
template_end = '</body></html>'

#calls create_sols
sols = create_solns(ordered_fns)

#writes all the html to an external HTML file that can then be opened to view in browser
#subsitutes all py values into templates given above as well
html_file.writelines( [template_start, template_js, template_body.format(blank_1, substitue(ordered_fns)), template_form.format(sols[0], sols[1], sols[2], sols[3], sols[4]), template_submit,template_end] )




