import unittest
# import sys
# sys.path.append('.')

from .. import src.TheGame.explosion.Explosion as ExplosionClass

ani = ExplosionClass()

class Test(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    pass

if __name__ == '__main__':
    # begin the unittest.main()
    unittest.main()
