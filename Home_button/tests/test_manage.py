import os
import sys
import unittest
from unittest.mock import patch

class TestManagePy(unittest.TestCase):

    def setUp(self):
        self.manage_py_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../manage.py'))
        self.manage_module = __import__('manage')

    @patch('django.core.management.execute_from_command_line')
    def test_manage_py_runs(self, mock_execute):
        """Test that manage.py runs without errors."""
        mock_execute.return_value = None
        with patch.object(sys, 'argv', [self.manage_py_path, 'help']):
            try:
                self.manage_module.main()
                mock_execute.assert_called_once_with([self.manage_py_path, 'help'])
            except SystemExit as e:
                self.assertEqual(e.code, 0)

if __name__ == '__main__':
    unittest.main()
