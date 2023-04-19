import unittest

from src.main import Project, ProjectDay

class TestProject (unittest.TestCase):
    def test_single_project_day_should_be_travel (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/01")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEqual(len(days), 1)
        self.assertTrue(days[0].is_travel_day)

    def test_two_project_days_should_be_travel (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/02")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEqual(len(days), 2)
        self.assertTrue(days[0].is_travel_day)
        self.assertTrue(days[1].is_travel_day)

    def test_internal_project_days_should_be_full (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEqual(len(days), 3)
        self.assertTrue(days[0].is_travel_day)
        self.assertFalse(days[1].is_travel_day)
        self.assertTrue(days[2].is_travel_day)

    def test_project_days_should_have_same_cost_as_project_high (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEqual(len(days), 3)
        for day in days:
            self.assertTrue(day.is_high_cost_city)

    def test_project_days_should_have_same_cost_as_project_low (self):
        project = Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEqual(len(days), 3)
        for day in days:
            self.assertFalse(day.is_high_cost_city)

if __name__ == '__main__':
    unittest.main()
