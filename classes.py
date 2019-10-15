import random
import math
import os
import textwrap

class function_composition(object):
	"""
	Summary: function composition object that 
	organizes our logic

	Parameters:
	simple_func function_list: a list of simple_func objects to pick from
	"""
	def __init__(self, function_list):
		assert function_list and len(function_list) > 0
		self.function_list = function_list
	
	def __rand_pick_func(self, num_functions):
		assert num_functions <= len(self.function_list)
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
		assert num_functions <= len(self.function_list)
		assert 1 <= num_functions
		assert 1 < num_choices and num_choices <= math.factorial(len(self.function_list))
		assert 1 <= num_questions and num_questions <= math.factorial(len(self.function_list))

		generated_ans_set = set()

		all_questions = []

		for k in range(num_questions):

			while True:
				ans_list = self.__rand_pick_func(num_functions)
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
						if c_str not in existing_fn:
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
	__need_enclose_ops = ('+', '-', '/', '%')

	simple_ops = {	'+' : r' + ', 
					'-' : r' - ', 
					'*' : r' \times ', 
					'/' : r' \div ', 
					'^' : r'^', 
					'%' : r' \% '
				}

	def __init__(self, name, arg_name, operation, number):
		self.name = name
		self.arg_name = arg_name
		self.operation = operation
		self.number = number 
		self.need_enclosure = self.operation in self.__need_enclose_ops
		self.function_str = f"{self.name}({self.arg_name})"
		self.function_expr = self.concat_expr(arg_name)
		# for convenience, violating abstraction a bit
		self.function_str_expr = f"{self.function_str} = {self.function_expr}"
		
	def concat_str(self, param):
		return f"{self.name}({param})"


	def concat_expr(self, nested_expr):
		if self.operation in self.simple_ops.keys():
			return f"{nested_expr}{self.simple_ops[self.operation]}{self.number}"
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

	def __repr__(self):
	 return f"{self.function_str} = {self.function_expr}"

class file_writer(object):
	"""
	Summary:
	Generalized writer object to construct html outputs

	Parameters:
	File Object file: an opened python file object to dump the output

	function_composition fn_comp: a function composition object that generates the questions

	int num_functions: number of functions to use

	int num_choices: number of choices to have 

	int num_questions=1: number of questions to generate

	bool body_only=False: do not include html <html>, <heads>, etc headers in output 
	"""

	template_start = r'''
<html>
<head>
</head>
<body>
	'''
	
	template_body = r'''
	<p class="mx-5 my-2 text-left font-weight-bold">If we were given {0} functions: </p>
	<p class="text-center font-weight-bold">{1}</p> 
	<p class="mx-5 my-2 text-left font-weight-bold">... and you wanted to calculate:</p>
	<p class="text-center font-weight-bold">{2}</p> 
	<p class="mx-5 my-2 text-left font-weight-bold">...how would you compose the functions to get that? (select ONE)</p>
	'''

	hr = rf'''
	<hr>
	'''
	# extra function_composition path: os.path.dirname(os.path.realpath(__file__))
	mathjax = r'''
	<script id="MathJax-script" async 
		src="./packages/MathJax-master/es5/tex-chtml.js">
	</script>
	'''
	mathjax_online = r'''
	<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
	<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
	'''

	bootstrap = r'''
	<link rel="stylesheet" href="packages/bootstrap-4.3.1-dist/css/bootstrap.css">
	<script src="packages/bootstrap-4.3.1-dist/js/bootstrap.js"></script>
	'''

	bootstrap_online = r'''
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
		integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
		integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
		crossorigin="anonymous"></script>
	'''

	template_end = r'''
</body>
</html>
	'''

	def __init__(self, file, fn_comp, num_functions, num_choices, num_questions=1, body_only=False, is_web=False):
		self.file = file
		self.fn_comp = fn_comp
		self.num_functions = num_functions
		self.num_choices = num_choices
		self.num_questions = num_questions
		self.body_only = body_only
		self.is_web = is_web

	def dump(self):
		"""
		creates html contents and dumps to file
		"""
		if not self.body_only:
			self.file.write(self.template_start)

		generated_questions = self.fn_comp.generate(self.num_functions, self.num_choices, self.num_questions)
		
		for i in range(len(generated_questions)):
			ans_list, ans_pos, choices = generated_questions[i]
			display_fn = ans_list[:]
			random.shuffle(display_fn)
			fn_body = " ".join([f"$${f.function_str_expr}$$" for f in display_fn])
			template_body = self.template_body.format(self.num_functions, fn_body, f"$${function_composition.func_expression_str(ans_list)}$$")
			form = textwrap.indent('''<div class="container-fluid">\n<div class="row mx-5">''', '\n')

			form += "\n".join([rf'''
			<div class="col py-2 border border-dark">
				<div class="form-check form-check-inline">
					<input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1"
						value="option1">
					<label class="form-check-label" for="inlineRadio1">
							\({function_composition.func_str(choices[j])}\)
					</label>
				</div>
			</div>
			'''for j in range(len(choices))])
			form += textwrap.indent('</div>\n</div>', '\n')
			self.file.write("".join([template_body, form, self.hr]))

		# script tags
		if self.is_web:
			self.file.write(self.bootstrap_online)
			self.file.write(self.mathjax_online)
		else:
			self.file.write(self.bootstrap)
			self.file.write(self.mathjax)

		if not self.body_only:
			self.file.write(self.template_end)
		self.file.write("\n")
