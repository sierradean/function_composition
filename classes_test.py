import unittest
import tempfile

from classes import *

class TestFunctionComposition(unittest.TestCase):

    # Run before every test
    def setUp(self):
        self.f1 = simple_func('F', 'x', '+', 8)
        self.f2 = simple_func('G', 'x', '*', 7)
        self.f3 = simple_func('H', 'x', '^', 2)

        self.f4 = simple_func('G', 'y', '*', 7)

        self.fn_list = [self.f1, self.f2, self.f3]


    def test_simple_func(self):
        self.assertEqual(self.f1.function_str, 'F(x)')
        self.assertEqual(self.f1.function_expr, 'x + 8')

        self.assertEqual(self.f4.function_str, 'G(y)')
        self.assertEqual(self.f4.function_expr, 'y * 7')

    def test_simple_func_concat_str(self):
        self.assertEqual(self.f1.concat_str(self.f4.function_str), 'F(G(y))')
        self.assertEqual(self.f2.concat_fn(self.f1), '(x + 8) * 7')

    def test_function_composition(self):
        s = function_composition.func_str(self.fn_list)
        self.assertEqual(s, 'F(G(H(x)))')

        x = function_composition.func_expression_str(self.fn_list)
        self.assertEqual(x, '(x ^ 2) * 7 + 8')

    def test_function_comp_generate(self):

        Composer = function_composition(self.fn_list)
        # for high confidence, we run this 100 times
        for i in range(100):
            ans_list, ans_pos, choices = Composer.generate(3, 5)
            choices_str = [function_composition.func_str(l) for l in choices]
            self.assertTrue(len(set(choices_str)) == len(choices_str))
            self.assertEqual(function_composition.func_str(choices[ans_pos]), 
                        function_composition.func_str(ans_list))


if __name__ == '__main__':
    unittest.main()

