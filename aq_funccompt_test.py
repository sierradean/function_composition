import unittest

from aq_funccompt_skeleton import *

class TestStringMethods(unittest.TestCase):


    def test_simple_func(self):
        f1 = simple_func('F', 'x', '+', 8)
        f2 = simple_func('G', 'y', '*', 7)
        self.assertEqual(f1.function_str, 'F(x)')
        self.assertEqual(f1.function_expr, 'x + 8')

        self.assertEqual(f2.function_str, 'G(y)')
        self.assertEqual(f2.function_expr, 'y * 7')

    def test_simple_func_concat_str(self):
        f1 = simple_func('F', 'x', '+', 8)
        f2 = simple_func('G', 'y', '*', 7)

        self.assertEqual(f1.concat_str(f2.function_str), 'F(G(y))')
        self.assertEqual(f2.concat_expr(f1), '(x + 8) * 7')

if __name__ == '__main__':
    unittest.main()

