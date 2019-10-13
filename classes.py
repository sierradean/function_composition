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
	__need_enclose_ops = ('+', '-', '^', '/')

	simple_ops = ('+', '-', '*', '/', '^', '%')

	def __init__(self, name, arg_name, operation, number):
		self.name = name
		self.arg_name = arg_name
		self.operation = operation
		self.number = number 
		self.need_enclosure = self.operation in self.__need_enclose_ops
		self.function_str = f"{self.name}({self.arg_name})"
		self.function_expr = self.concat_expr(arg_name)
		self.function_str_expr_html = f"<strong>{self.function_str} = {self.function_expr}</strong>"
		
	def concat_str(self, param, html=False):
		if html:
			return f"<strong>{self.name}({param})</strong>"
		return f"{self.name}({param})"


	def concat_expr(self, nested_expr):
		if self.operation in self.simple_ops:
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
<script type="">
	'''
	template_js = r'''
	var form = document.querySelector("form");
	var log = document.querySelector("#log"); 
	form.addEventListener("submit", function(event) {
		var data = new FormData(form); 
		var output = "";
		for (const entry of data) {
			output = output + entry[0] + "=" + entry[1] + "\r"
		};
		log.innerText = output;
		event.preventDefault();
	}, false)</script>
</head>
<body>
	'''
	
	template_body = r'''
	<p>If we were given {0} functions: </p>
	<p style="text-align: center"> {1} </p> 
	<p>... and you wanted to calculate:</p>
	<p style="text-align: center"> {2} </p> 
	<p>...how would you compose the functions to get that? (select ONE)</p>
	'''

	template_form =	r'''
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
	template_submit = r'''
	<pre id="log"></pre>
	<button>Submit</button>
	'''
	hr = r'''
	<hr>
	'''
	template_end = r'''
</body>
</html>
	'''

	def __init__(self, file, fn_comp, num_functions, num_choices, num_questions=1, body_only=False):
		self.file = file
		self.fn_comp = fn_comp
		self.num_functions = num_functions
		self.num_choices = num_choices
		self.num_questions = num_questions
		self.body_only = body_only

	def dump(self):
		"""
		creates html contents and dumps to file
		"""
		if not self.body_only:
			self.file.write(self.template_start)
			self.file.write(self.template_js)
		generated_questions = self.fn_comp.generate(self.num_functions, self.num_choices, self.num_questions)
		for i in range(len(generated_questions)):
			ans_list, ans_pos, choices = generated_questions[i]
			ans_list_copy = ans_list[:]
			random.shuffle(ans_list_copy)
			fn_body = ", ".join([f.function_str_expr_html for f in ans_list_copy])
			template_body = self.template_body.format(self.num_functions, fn_body, function_composition.func_expression_str(ans_list))
			form = r'''
	<form>
	<div>
'''
			form += "\n".join([f'<input type="radio" id="funcComp{j+1}" name="funcComp" value="{j+1}"><label for="funcComp{j+1}">{function_composition.func_str(choices[j])}</label>' for j in range(len(choices))])
			form += r'''
	</div>
	</form>
'''
			self.file.write("".join([template_body, form, self.template_submit, self.hr]))
		if not self.body_only:
			self.file.write(self.template_end)
		self.file.write("\n")