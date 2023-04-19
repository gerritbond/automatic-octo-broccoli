import unittest

from reimbursements.main import Project, ProjectSet, ProjectDay

class TestProject (unittest.TestCase):
    def test_single_project_day_should_be_travel (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/01")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEquals(len(days), 1)
        self.assertTrue(days[0].is_travel_day)

    def test_two_project_days_should_be_travel (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/02")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEquals(len(days), 2)
        self.assertTrue(days[0].is_travel_day)
        self.assertTrue(days[1].is_travel_day)

    def test_internal_project_days_should_be_full (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEquals(len(days), 3)
        self.assertTrue(days[0].is_travel_day)
        self.assertFalse(days[1].is_travel_day)
        self.assertTrue(days[2].is_travel_day)

    def test_project_days_should_have_same_cost_as_project_high (self):
        project = Project(city_cost="High", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEquals(len(days), 3)
        for day in days:
            self.assertTrue(day.is_high_cost_city)

    def test_project_days_should_have_same_cost_as_project_low (self):
        project = Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03")
        days: list[ProjectDay] = project.convert_to_days()

        self.assertEquals(len(days), 3)
        for day in days:
            self.assertFalse(day.is_high_cost_city)

class TestProjectSet (unittest.TestCase):
    def test_no_duplicates_when_projects_overlap (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/02", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEquals(len(days), 4)

    def test_overlapping_full_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEquals(len(days), 4)
        self.assertFalse(days[1].is_travel_day)

    def test_overlapping_travel_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEquals(len(days), 4)
        self.assertFalse(days[0].is_travel_day)

    def test_overlapping_travel_and_full_days_treated_as_full (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/04")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEquals(len(days), 4)
        self.assertFalse(days[2].is_travel_day)

    def test_days_on_either_side_of_gap_are_travel_days (self):
        projects = [
            Project(city_cost="Low", start_date="2015/09/01", end_date="2015/09/03"),
            Project(city_cost="Low", start_date="2015/09/05", end_date="2015/09/09")
        ]
        project_set = ProjectSet(projects=projects)

        days = project_set.determine_actual_days()

        self.assertEquals(len(days), 8)
        
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

        self.assertEquals(len(days), 4)
        self.assertTrue(days[0].is_high_cost_city)


if __name__ == '__main__':
    unittest.main()
