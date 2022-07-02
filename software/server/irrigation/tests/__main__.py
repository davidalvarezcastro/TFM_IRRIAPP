import unittest
import sys
import os


tests = unittest.TestLoader().discover('tests', pattern='test*.py')
result = unittest.TextTestRunner(verbosity=2).run(tests)
if result.wasSuccessful():
    sys.exit(0)

sys.exit(1)
