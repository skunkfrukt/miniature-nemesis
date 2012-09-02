from .. import gui
import unittest

class TestGameMenu(unittest.TestCase):
    def setUp(self):
        self.empty_menu = gui.GameMenu()
        self.default_menu = gui.GameMenu(['first','second','third'])
        self.non_wrapping_menu = gui.GameMenu(['first','second','third'], wrap = False)
        self.different_initial_index_menu = gui.GameMenu(['first','second','third'], initial_option = 1);
        
    def test_default_initial_option(self):
        assertEqual(0, self.default_menu.get_option())
        
    
if __name__ == '__main__':
    unittest.main()