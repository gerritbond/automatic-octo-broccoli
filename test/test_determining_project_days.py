import unittest
import datetime

from reimbursements.main import ProjectSet, ProjectDay, determine_project_days

class TestDetermineProjectDays (unittest.TestCase):
    def test_reimbursing_with_unrecognized_tier_should_default_to_low (self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
