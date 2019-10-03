import random
import math
import os
import sys

class function_composition(object):
	"""
	Summary: function composition object that 
	organizes our logic

	Parameters:
	file object: a file object that can be written to

	simple_func function_list: a list of simple_func objects to pick from
	"""
	def __init__(self, file, function_list):
		self.file = file
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

	def generate(self, num_functions, num_choices):
		"""
		generate our question

		Parameters:
		int num_functions: number of functions to choose from
			if num_functions > len(number of given functions)
			repetition will occur
		
		int num_choices: number of choices to generate. Exactly one of these
			choices is correct.
		
		Returns:
		answer functions list, index of correct answer, choices (list of functions list)
		"""
		assert 1 < num_functions
		assert 1 < num_choices and num_choices <= math.factorial(len(self.function_list))

		ans_list = self.__rand_pick_func(num_functions, num_functions > len(self.function_list))
		existing_fn = set()

		ans_func_str = self.func_str(ans_list) # e.g. F(H(x))
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
		return ans_list, ans_pos, choices


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




