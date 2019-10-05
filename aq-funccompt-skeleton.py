import random
import math
from string import Template

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



