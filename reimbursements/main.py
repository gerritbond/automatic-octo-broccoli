import json
import sys
from datetime import datetime, timedelta, date

class ProjectDay:
    LOW_COST_CITY_TRAVEL_RATE = 45
    LOW_COST_CITY_FULL_RATE = 75
    HIGH_COST_CITY_TRAVEL_RATE = 55
    HIGH_COST_CITY_FULL_RATE = 85

    def __init__ (self, is_high_cost_city: bool, is_travel_day: bool, date: date):
        self.is_high_cost_city = is_high_cost_city
        self.is_travel_day = is_travel_day
        self.date = date

    def calculate_reimbursement (self):
        total = 0
        if self.is_high_cost_city:
            if self.is_travel_day:
                total += ProjectDay.HIGH_COST_CITY_TRAVEL_RATE
            else:
                total += ProjectDay.HIGH_COST_CITY_FULL_RATE
        else:
            if self.is_travel_day:
                total += ProjectDay.LOW_COST_CITY_TRAVEL_RATE
            else:
                total += ProjectDay.LOW_COST_CITY_FULL_RATE

        return total

    def pretty_print (self):
        print (f"{self.date.strftime('%Y/%m/%d')}: {self.calculate_reimbursement()}")

class Project:
    DATE_FORMAT = "%Y/%m/%d"

    def __init__ (self, city_cost, start_date, end_date):
        self.is_high_cost_city = city_cost.lower() == "high"
        self.start_date = datetime.strptime(start_date, Project.DATE_FORMAT)
        self.end_date = datetime.strptime(end_date, Project.DATE_FORMAT)

    def convert_to_days (self) -> list[ProjectDay]:
        project_days: list[ProjectDay] = []
        time_delta = self.end_date - self.start_date

        for t in range(time_delta.days + 1):
            project_days.append(
                ProjectDay(
                    is_high_cost_city=self.is_high_cost_city,
                    is_travel_day=False,
                    date=self.start_date+timedelta(days=t)))

        # Set the first and last day of a project as travel days
        project_days[0].is_travel_day = True
        project_days[len(project_days) - 1].is_travel_day = True

        return project_days

    def calculate_reimbursement (self):
        days = self.convert_to_days()
        total = 0

        for day in days:
            total += day.calculate_reimbursement()


class ProjectSet:
    def __init__ (self, projects: list[Project] = []):
        self.projects = projects

    # Determines actual project days for the provided project set
    def determine_actual_days (self) -> list[ProjectDay]:
        if len(self.projects) == 0:
            return []

        if len(self.projects) == 1:
            return self.projects[0].convert_to_days()

        # Construct a lookup of Date -> Project Days
        initial_project_days = self.projects[0].convert_to_days()
        day_mapping: dict[date, ProjectDay] = {
            k: v for k, v in zip([day.date for day in initial_project_days], initial_project_days)}

        for project in self.projects[1:]:
            new_days = project.convert_to_days()

            for day in new_days:
                # Check for day overlaps, adjusting cost if needed and ensuring they are full days
                if day.date in day_mapping:
                    if day.is_high_cost_city:
                        day_mapping[day.date].is_high_cost_city = True
                    day_mapping[day.date].is_travel_day = False
                else:
                    day_mapping[day.date] = day

        # Pull out the now distinct values, and sort the list by date
        actual_project_days: list[ProjectDay] = list(day_mapping.values())
        actual_project_days.sort(key=lambda d: d.date)

        # Check over the list, ensuring internal days full days
        for idx, day in enumerate(actual_project_days):
            # First and last day cannot be between two days
            if idx in (0, (len(actual_project_days) - 1)):
                continue

            l_date = actual_project_days[idx-1].date
            n_date = actual_project_days[idx+1].date

            # A day is internal if it is border by two other project days
            if day.date - l_date == timedelta(days=1) and n_date - day.date == timedelta(days=1):
                day.is_travel_day = False

        return actual_project_days

# Loads project sets from a list of filenames
def load (files: list[str]) -> ProjectSet:
    sets = []
    # Read in project sets from command line, passed in as json files.
    for name in files:
        project_set = ProjectSet()

        try:
            with open(name, 'r', encoding="UTF-8") as f:
                data = f.read()
                project_data = json.loads(data)['projects']
                for d in project_data:
                    project_set.projects.append(
                        Project(d["city_cost"], d["start_date"], d["end_date"]))

            sets.append(project_set)
        except FileNotFoundError:
            print(f"Encountered a problem reading in set file {name}; skipping")

    return project_sets

# Code to execute if this file is being used to actual assess a project and not just under test
if __name__ == '__main__':
    filenames = sys.argv[1:]
    if len(filenames) == 0:
        print ("Usage: py3 main.py project_set.json [project_set_2.json ..]")
        sys.exit(1)

    project_sets = load(filenames)
