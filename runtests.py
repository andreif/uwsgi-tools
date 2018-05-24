import sys
import unittest


def main():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(not result.wasSuccessful())


if __name__ == '__main__':
    main()
