import json
import sys
import datetime

LOW_COST_CITY_TRAVEL_RATE = 45
LOW_COST_CITY_FULL_RATE = 75
HIGH_COST_CITY_TRAVEL_RATE = 55
HIGH_COST_CITY_FULL_RATE = 85

class ProjectDay:
    def __init__ (self, is_high_cost_city: bool, is_travel_day: bool, date: datetime.date):
        self.is_high_cost_city = is_high_cost_city
        self.is_travel_day = is_travel_day
        self.date = date

class Project:
    def __init__ (self, city_cost, start_date, end_date):
        self.is_high_cost_city = city_cost.lower() == "high"
        self.start_date = start_date
        self.end_date = end_date

    def convert_to_days (self) -> list[ProjectDay]:
        return []

class ProjectSet:
    def __init__ (self, json_def: str):
        self.projects: list[Project] = []

        # Process each of the projects into a model 
        projectData = json.loads(json_def)['projects']
        for d in projectData:
            self.projects.append(Project(d))


# Assess the total amount to reimburse for a provided set of project days
def assess_reimbursement_costs (project_days: list[ProjectDay]) -> int:
    total = 0

    for day in project_days:
        if day.is_high_cost_city:
            total += HIGH_COST_CITY_TRAVEL_RATE if day.is_travel_day else HIGH_COST_CITY_FULL_RATE
        else:
            total += LOW_COST_CITY_TRAVEL_RATE if day.is_travel_day else LOW_COST_CITY_FULL_RATE
    
    return total

# Determines actual project days for the provided project set
def determine_project_days (project_set: ProjectSet) -> list[ProjectDay]:
    return []

# Loads project sets from a list of filenames
def load (filenames: list[str]) -> ProjectSet:
    project_sets = []    
    # Read in project sets from command line, passed in as json files.
    for name in filenames:
        try:
            with open(name, 'r') as f:
                data = f.read()
                project_sets.append(ProjectSet(data))
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


