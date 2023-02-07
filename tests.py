################################################################## 
# Unitests - not ready yet
################################################################## 

import pandas as pd
import numpy as np
import unittest
from states import states_builder, add_states, transitions, preform_test
from scipy.stats import chi2_contingency

class TestStatesBuilderFunctions(unittest.TestCase):
    def test_states_builder(self):
        # Test the state builder function with valid inputs
        quarter = 3
        make = 'MISS'
        value = 2
        previous_quarter = 2
        previous_make = 'MAKE'
        previous_value = 3
        expected_output = ('MAKE_3', 'MISS_2')
        self.assertEqual(states_builder(quarter, make, value, previous_quarter, previous_make, previous_value), expected_output)
        
        # Test the state builder function when the previous quarter is greater than the current quarter
        quarter = 2
        make = 'MAKE'
        value = 3
        previous_quarter = 3
        previous_make = 'MISS'
        previous_value = 2
        expected_output = ('START', 'MAKE_3')
        self.assertEqual(states_builder(quarter, make, value, previous_quarter, previous_make, previous_value), expected_output)
        
        # Test the state builder function when the previous make is missing
        quarter = 3
        make = 'MAKE'
        value = 2
        previous_quarter = 2
        previous_make = np.nan
        previous_value = np.nan
        expected_output = ('START', 'MAKE_2')
        self.assertEqual(states_builder(quarter, make, value, previous_quarter, previous_make, previous_value), expected_output)

class TestTransitionsFunction(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({'QUARTER': [1, 2, 3, 4, 1, 2, 3, 4],
                                'MAKE_MISS': ['MAKE', 'MAKE', 'MISS', 'MISS', 'MISS', 'MISS', 'MAKE', 'MAKE'],
                                'VALUE': [2, 2, 2, 3, 2, 3, 2, 2]})
        
    def test_transitions(self):
        expected = pd.DataFrame({'make_2': [0.5, 0.0], 'miss_2': [0.0, 0.5], 'miss_3': [0.5, 0.0], 'make_3': [0.0, 0.5]},
                                index=['make_2', 'miss_2'])
        result = transitions(self.df)
        
        np.testing.assert_array_almost_equal(expected, result)        
        
class TestAddStates(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'QUARTER': [1, 1, 1, 2, 2, 3, 3],
            'MAKE_MISS': ['MISS', 'MISS', 'MAKE', 'MAKE', 'MISS', 'MAKE', 'MAKE'],
            'VALUE': [2, 2, 3, 2, 2, 2, 3]
        })

    def test_add_states(self):
        add_states(self.df)
        self.assertIn('PREV_STATE', self.df.columns)
        self.assertIn('STATE', self.df.columns)
        self.assertEqual(len(self.df.columns), 5)

    def test_states_correctness(self):
        add_states(self.df)
        expected_prev_states = ['START', 'MISS_2', 'MISS_2', 'MAKE_3', 'MAKE_2', 'MAKE_2', 'MAKE_2']
        expected_states = ['MISS_2', 'MISS_2', 'MAKE_3', 'MAKE_2', 'MISS_2', 'MAKE_2', 'MAKE_3']
        self.assertListEqual(self.df['PREV_STATE'].tolist(), expected_prev_states)
        self.assertListEqual(self.df['STATE'].tolist(), expected_states)

class TestPreformTest(unittest.TestCase):

    def test_preform_test(self):
        # create a sample DataFrame for testing purposes
        df = pd.DataFrame({
            'QUARTER': [1, 2, 3, 4, 1, 2, 3, 4],
            'MAKE_MISS': ['MISS', 'MAKE', 'MISS', 'MAKE', 'MISS', 'MAKE', 'MISS', 'MAKE'],
            'VALUE': [2, 2, 3, 3, 2, 2, 3, 3]
        })
        
        cross, result = preform_test(df)
        chi2, p, dof, expected = chi2_contingency(cross)
        
        # check if the function returns a correct result of chi2_contingency test
        self.assertEqual(result[0], chi2)
        self.assertEqual(result[1], p)
        self.assertEqual(result[2], dof)
        np.testing.assert_array_almost_equal(result[3], expected)

if __name__ == '__main__':
    unittest.main()


