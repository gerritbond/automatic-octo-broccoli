import unittest
import datetime

from reimbursements.main import ProjectDay, assess_reimbursement_costs

class TestReimbursements (unittest.TestCase):
    def test_reimbursing_low_cost_travel_day (self):
        day = ProjectDay(is_high_cost_city=False, is_travel_day=True, date=datetime.date(2015, 9, 1))
        reimbursement = assess_reimbursement_costs ([day])
        
        self.assertEquals(reimbursement, 45)

    def test_reimbursing_high_cost_travel_day (self):
        day = ProjectDay(is_high_cost_city=True, is_travel_day=True, date=datetime.date(2015, 9, 1))
        reimbursement = assess_reimbursement_costs ([day])
        
        self.assertEquals(reimbursement, 55)

    def test_reimbursing_low_cost_full_day (self):
        day = ProjectDay(is_high_cost_city=False, is_travel_day=False, date=datetime.date(2015, 9, 1))
        reimbursement = assess_reimbursement_costs ([day])
        
        self.assertEquals(reimbursement, 75)

    def test_reimbursing_high_cost_full_day (self):
        day = ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 1))
        reimbursement = assess_reimbursement_costs ([day])
        
        self.assertEquals(reimbursement, 85)

    def test_reimbursing_multiple_days (self):
        days = [
            ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 1)),
            ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 2))
        ]
        reimbursement = assess_reimbursement_costs(days)

        self.assertEquals(reimbursement, 170)

    def test_reimbursing_multiple_days_with_different_rates (self):
        days = [
            ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 1)),
            ProjectDay(is_high_cost_city=False, is_travel_day=False, date=datetime.date(2015, 9, 2))
        ]
        reimbursement = assess_reimbursement_costs(days)

        self.assertEquals(reimbursement, 160)

        
    def test_reimbursing_multiple_days_with_partial_travel (self):
        days = [
            ProjectDay(is_high_cost_city=True, is_travel_day=True, date=datetime.date(2015, 9, 1)),
            ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 2))
        ]
        reimbursement = assess_reimbursement_costs(days)

        self.assertEquals(reimbursement, 140)

        
    def test_reimbursing_multiple_days_with_different_rates_and_partial_travel (self):
        days = [
            ProjectDay(is_high_cost_city=True, is_travel_day=False, date=datetime.date(2015, 9, 1)),
            ProjectDay(is_high_cost_city=False, is_travel_day=True, date=datetime.date(2015, 9, 2))
        ]
        reimbursement = assess_reimbursement_costs(days)

        self.assertEquals(reimbursement, 130)
    
    
    def test_reimbursing_no_days (self):
        days = []
        reimbursement = assess_reimbursement_costs(days)

        self.assertEquals(reimbursement, 0)


if __name__ == '__main__':
    unittest.main()
