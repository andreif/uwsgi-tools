import sys
import unittest


def main():
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(1 if result.errors else 0)


if __name__ == '__main__':
    main()
