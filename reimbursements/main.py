import json
import sys
import datetime

class ProjectDay:
    LOW_COST_CITY_TRAVEL_RATE = 45
    LOW_COST_CITY_FULL_RATE = 75
    HIGH_COST_CITY_TRAVEL_RATE = 55
    HIGH_COST_CITY_FULL_RATE = 85

    def __init__ (self, is_high_cost_city: bool, is_travel_day: bool, date: datetime.date):
        self.is_high_cost_city = is_high_cost_city
        self.is_travel_day = is_travel_day
        self.date = date

    def calculate_reimbursement (self):
        total = 0
        if self.is_high_cost_city:
            total += ProjectDay.HIGH_COST_CITY_TRAVEL_RATE if self.is_travel_day else ProjectDay.HIGH_COST_CITY_FULL_RATE
        else:
            total += ProjectDay.LOW_COST_CITY_TRAVEL_RATE if self.is_travel_day else ProjectDay.LOW_COST_CITY_FULL_RATE
        
        return total


class Project:
    DATE_FORMAT = "%Y/%m/%d"

    def __init__ (self, city_cost, start_date, end_date):
        self.is_high_cost_city = city_cost.lower() == "high"
        self.start_date = datetime.datetime.strptime(start_date, Project.DATE_FORMAT)
        self.end_date = datetime.datetime.strptime(end_date, Project.DATE_FORMAT)

    def convert_to_days (self) -> list[ProjectDay]:
        project_days: list[ProjectDay] = []
        time_delta = self.end_date - self.start_date

        for t in range(time_delta.days + 1):
            project_days.append(
                ProjectDay(
                    is_high_cost_city=self.is_high_cost_city, 
                    is_travel_day=False, 
                    date=self.start_date+datetime.timedelta(days=t)))
        
        # Set the first and last day of a project as travel days
        project_days[0].is_travel_day = True
        project_days[len(project_days) - 1].is_travel_day = True

        return project_days

    def calculate_reimbursement (self):
        days = self.convert_to_days()
        total = 0

        for d in days:
            total += d.calculate_reimbursement()


class ProjectSet:
    def __init__ (self, projects: list[Project] = []):
        self.projects = projects

    # Determines actual project days for the provided project set
    def determine_actual_days (self) -> list[ProjectDay]:
        return []

# Loads project sets from a list of filenames
def load (filenames: list[str]) -> ProjectSet:
    project_sets = []    
    # Read in project sets from command line, passed in as json files.
    for name in filenames:
        project_set = ProjectSet()

        try:
            with open(name, 'r') as f:
                data = f.read()
                projectData = json.loads(data)['projects']
                for d in projectData:
                    project_set.projects.append(Project(d["city_cost"], d["start_date"], d["end_date"]))

            project_sets.append(project_set)
        except:
            print(f"Encountered a problem reading in set file {name}; skipping")

    return project_sets

# Code to execute if this file is being used to actual assess a project and not just under test
if __name__ == '__main__':
    filenames = sys.argv[1:]
    if (len(filenames) == 0):
        print ("Usage: py3 main.py project_set.json [project_set_2.json ..]")
        sys.exit(1)

    project_sets = load(filenames)

