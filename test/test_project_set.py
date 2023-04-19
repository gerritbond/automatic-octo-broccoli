import unittest

from src.main import Project, ProjectSet

class TestProjectSet (unittest.TestCase):
    def test_no_duplicates_when_projects_overlap (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/02", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 4)

    def test_overlapping_full_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 4)
        self.assertFalse(days[1].is_travel_day)

    def test_overlapping_travel_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 4)
        self.assertFalse(days[0].is_travel_day)

    def test_overlapping_travel_and_full_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 4)
        self.assertFalse(days[2].is_travel_day)

    def test_days_on_either_side_of_gap_are_travel_days (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/05", end_date="2015/09/09")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 8)

        # These are the two days that are on either side of the gap in the projects above
        self.assertTrue(days[2].is_travel_day)
        self.assertTrue(days[3].is_travel_day)

    def test_overlapping_day_with_different_rates_considered_high (self):
        projects = [
            Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEqual(len(days), 4)
        self.assertTrue(days[0].is_high_cost_city)

if __name__ == '__main__':
    unittest.main()
