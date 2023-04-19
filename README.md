# ST Technical Interview Solution

This repository contains an implementation of a technical interview question provided by ST.

## Running the code

To run the code, you will need to have at least Python 3. It has been developed with *Python 3.9.5*

We are only using python builtins, no extra packages are required.

The program takes as input any filenames containing a project set to be evaluated.

```bash
python src/main.py data/project_set.json [data/project_set...]
```

To run all original project sets;

```bash
python src/main.py data/project_set_1.json data/project_set_2.json data/project_set_3.json data/project_set_4.json
```

or

```bash
python src/main.py data/project_set_1.json
python src/main.py data/project_set_2.json 
python src/main.py data/project_set_3.json
python src/main.py data/project_set_4.json
```

Each project set will be output a summary of the information passed in, and the ultimate schedule. Along with a total reimbursement. For example; the first project set yields:

```
Submitted Project Days for data/project_set_1.json
2015/09/01: 45
2015/09/02: 75
2015/09/03: 45
-------

Actual Project Days for data/project_set_1.json:
2015/09/01: 45
2015/09/02: 75
2015/09/03: 45
Total Reimbursement Owed: 165
```

If you want to use a project set not included in the initial problem, your format should look like:

The JSON format expected is:
```json
{
    "projects": [
        {
            "city_cost": "Low" | "High",
            "start_date": "2015/09/01",
            "end_date": "2015/09/03"
        }
    ]
}
```

## Running the tests

There are three test files, divided up among the different models in use.

To run these tests, run the following command:

```
python -m unittest test/test_*
```

## Problem Description

### Technical Exercise:
You have a set of projects, and you need to calculate a reimbursement amount for the set. Each project has a start date and an end date. The first day of a project and the last day of a project are always "travel" days. Days in the middle of a project are "full" days. There are also two types of cities a project can be in, high cost cities and low cost cities.

**A few rules:**
- First day and last day of a project, or sequence of projects, is a travel day.
- Any day in the middle of a project, or sequence of projects, is considered a full day.
- If there is a gap between projects, then the days on either side of that gap are travel days.
- If two projects push up against each other, or overlap, then those days are full days as well.
- Any given day is only ever counted once, even if two projects are on the same day.
- A travel day is reimbursed at a rate of 45 dollars per day in a low cost city.
- A travel day is reimbursed at a rate of 55 dollars per day in a high cost city.
- A full day is reimbursed at a rate of 75 dollars per day in a low cost city.
- A full day is reimbursed at a rate of 85 dollars per day in a high cost city.

Given the following sets of projects, provide code that will calculate the reimbursement for each.

```
Set 1:
  Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15

Set 2:
  Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
  Project 2: High Cost City Start Date: 9/2/15 End Date: 9/6/15
  Project 3: Low Cost City Start Date: 9/6/15 End Date: 9/8/15

Set 3:
  Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/3/15
  Project 2: High Cost City Start Date: 9/5/15 End Date: 9/7/15
  Project 3: High Cost City Start Date: 9/8/15 End Date: 9/8/15

Set 4:
  Project 1: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
  Project 2: Low Cost City Start Date: 9/1/15 End Date: 9/1/15
  Project 3: High Cost City Start Date: 9/2/15 End Date: 9/2/15
  Project 4: High Cost City Start Date: 9/2/15 End Date: 9/3/15
```



## Questions and Diagrams

For reference, some diagrams have been included in the diagrams folder. They are built with [Excalidraw](https://excalidraw.com/)

The questions:

**Q**: Are two overlapping full days permitted?

**A**: They can have overlapped full days, but the should only be counted once.

**Q**: Which strategy should we apply when two different rates are available for a single day?

**A**: You can use the highest rate

**Q**: Are travel days inclusive or exclusive of the days listed in a project? 
**A**: Travel days are inclusive!
