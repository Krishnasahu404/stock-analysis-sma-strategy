import unittest
import pandas as pd
from datetime import datetime

class TestDataValidation(unittest.TestCase):
    
    def setUp(self):
        self.df = pd.DataFrame({
            'date': [datetime(2024, 9, 9)],
            'close': [100.5],
            'high': [105.0],
            'low': [95.0],
            'open': [98.0],
            'volume': [1000],
            'instrument': ['AAPL']
        })
    
    def test_data_types(self):
        
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.df['date']))
        for col in ['close', 'high', 'low', 'open']:
            self.assertTrue(pd.api.types.is_float_dtype(self.df[col]))
        
        self.assertTrue(pd.api.types.is_integer_dtype(self.df['volume']))
        # Check if 'instrument' is string
        self.assertTrue(pd.api.types.is_string_dtype(self.df['instrument']))

if __name__ == '__main__':
    unittest.main()
