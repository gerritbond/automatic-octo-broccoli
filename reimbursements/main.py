import json
import sys

LOW_COST_CITY_TRAVEL_RATE = 45
LOW_COST_CITY_FULL_RATE = 75
HIGH_COST_CITY_TRAVEL_RATE = 55
HIGH_COST_CITY_FULL_RATE = 85

class ProjectDay:
    def __init__ (self, reimbursement_tier, is_travel_day, date):
        self.reimbursement_tier = reimbursement_tier
        self.is_travel_day = is_travel_day
        self.date = date

class ProjectSet:
    def __init__ (self, json_def):
        self.__dict__ = json.loads(json_def)

def assess_reimbursement_costs (project_days):
    return 0

def determine_project_days (project_set):
    return []

def load (filenames):
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


if __name__ == '__main__':
    filenames = sys.argv[1:]
    if (len(filenames) == 0):
        print ("Usage: py3 main.py project_set.json [project_set_2.json ..]")
        sys.exit(1)

    project_sets = load(filenames)


