import random
import math
import os
import sys

class function_composition(object):
	"""
	Summary: function composition object that 
	organizes our logic

	Parameters:
	simple_func function_list: a list of simple_func objects to pick from
	"""
	def __init__(self, function_list):
		self.function_list = function_list
	
	def __rand_pick_func(self, num_functions, allow_repetition=False):
		if allow_repetition:
			return random.choices(self.function_list, k=num_functions)
		return random.sample(self.function_list, k=num_functions)

	@staticmethod
	def func_str(fn_list):
		"""
		outputs the function string like F(H(x)) 
		"""
		so_far = fn_list[-1].function_str
		for i in range(len(fn_list) - 2, -1, -1):
			so_far = fn_list[i].concat_str(so_far)
		return so_far
	
	@staticmethod
	def func_expression_str(fn_list):
		"""
		outputs the function expression like: (x - 1) * 2
		"""
		so_far = fn_list[-1].function_expr
		for i in range(len(fn_list) - 2, -1, -1):
			if fn_list[i + 1].need_enclosure:
				so_far = f"({so_far})"
			so_far = fn_list[i].concat_expr(so_far)
		return so_far

	def generate(self, num_functions, num_choices, num_questions=1):
		"""
		generate our question

		Parameters:
		int num_functions: number of functions to choose from
			if num_functions > len(number of given functions)
			repetition will occur
		
		int num_choices: number of choices to generate. Exactly one of these
			choices is correct.
		
		int num_questions: number of questions to generate. Default is 1

		Returns:
		num_questions len list of
		[answer functions list, index of correct answer, choices (list of functions list)]
		"""
		assert 1 <= num_functions
		assert 1 < num_choices and num_choices <= math.factorial(len(self.function_list))
		assert 1 <= num_questions and num_questions <= math.factorial(len(self.function_list))

		generated_ans_set = set()

		all_questions = []

		for k in range(num_questions):

			while True:
				ans_list = self.__rand_pick_func(num_functions, num_functions > len(self.function_list))
				ans_func_str = self.func_str(ans_list) # e.g. F(H(x))
				if ans_func_str not in generated_ans_set:
					generated_ans_set.add(ans_func_str)
					break
			existing_fn = set()

			
			existing_fn.add(ans_func_str)

			choices = [None] * num_choices
			ans_pos = random.randint(0, num_choices - 1)
			choices[ans_pos] = ans_list
			
			for i in range(0, num_choices):
				if i != ans_pos:
					while True:
						c = ans_list[:]
						random.shuffle(c)
						c_str = self.func_str(c)
						if c_str != ans_func_str and c_str not in existing_fn:
							choices[i] = c
							existing_fn.add(c_str)
							break

			all_questions.append([ans_list, ans_pos, choices])
		return all_questions


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
	__need_enclose_ops = ('+', '-', '^')

	__simple_ops = ('+', '-', '*', '^', '%')

	def __init__(self, name, arg_name, operation, number):
		self.name = name
		self.arg_name = arg_name
		self.operation = operation
		self.number = number 
		self.need_enclosure = self.operation in self.__need_enclose_ops
		self.function_str = f"{self.name}({self.arg_name})"
		self.function_expr = self.concat_expr(arg_name)
		
	def concat_str(self, param):
		return f"{self.name}({param})"


	def concat_expr(self, nested_expr):
		if self.operation in self.__simple_ops:
			return f"{nested_expr} {self.operation} {self.number}"
		elif self.number is None and nested_expr is None:
			return f"{self.operation}()"
		elif self.number is None:
			return f"{self.operation}({nested_expr})"
		elif nested_expr is None:
			return f"{self.operation}({self.number})"
		else:
			raise RuntimeError("simple_func class does not support complex functions")


	def concat_fn(self, nest_fn):
		if nest_fn.need_enclosure:
			new_arg = f"({nest_fn.function_expr})"
		else:
			new_arg = nest_fn.function_expr
		return self.concat_expr(new_arg)


class file_writer(object):

	template_start = '<html><head><script type="">'
	template_js=	'var form = document.querySelector("form");var log = document.querySelector("#log"); form.addEventListener("submit", function(event) {var data = new FormData(form); var output = "";for (const entry of data) {output = output + entry[0] + "=" + entry[1] + "\r"};log.innerText = output;event.preventDefault();}, false)</script></head>'
	
	template_body = '''\
		<body>
			<p>If we were given {0} functions: </p>
			<p style="text-align: center"> {1} </p> 
			<p>... and you wanted to calculate:</p>
			<p style="text-align: center"> {2} </p> 
			<p>...how would you compose the functions to get that? (select ONE)</p>
		</body>
	'''

	template_form =	'''\
		<form>
		<div>
			<input type="radio" id="funcComp1" name="funcComp" value="a">
			<label for="funcComp1">{0}</label>
			<input type="radio" id="funcComp2" name="funcComp" value="b">
			<label for="funcComp2">{1}</label>
			<input type="radio" id="funcComp3" name="funcComp" value="c">
			<label for="funcComp3">{2}</label>
			<input type="radio" id="funcComp4" name="funcComp" value="d">
			<label for="funcComp4">{3}</label>
			<input type="radio" id="funcComp5" name="funcComp" value="e">
			<label for="funcComp5">{4}</label>
		</div>
		</form>
	'''
	template_submit = '<pre id="log"></pre><button>Submit</button>'
	template_end = '</body></html>\n'

	def __init__(self, file, fn_comp, num_functions, num_choices, num_questions=1):
		self.file = file
		self.fn_comp = fn_comp
		self.num_functions = num_functions
		self.num_choices = num_choices
		self.num_questions = num_questions

	def dump(self):
		"""
		creates html contents and dumps to file
		"""
		generated_questions = self.fn_comp.generate(self.num_function, self.num_choices, self.num_questions)
		for i in range(len(generated_questions)):
			ans_list, ans_pos, choices = generated_questions[i]
	