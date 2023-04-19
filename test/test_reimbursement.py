import unittest
import datetime

from reimbursements.main import ProjectDay, assess_reimbursement_costs

class TestReimbursements (unittest.TestCase):
    def test_reimbursing_low_cost_travel_day (self):
        day = ProjectDay(reimbursement_tier="Low", is_travel_day=True, date=datetime.date(2015, 9, 1))
        
        reimbursement = assess_reimbursement_costs (day)
        
        self.assertEquals(reimbursement, 45)

    def test_reimbursing_high_cost_travel_day (self):
        day = ProjectDay(reimbursement_tier="High", is_travel_day=True, date=datetime.date(2015, 9, 1))
        
        reimbursement = assess_reimbursement_costs (day)
        
        self.assertEquals(reimbursement, 55)

    def test_reimbursing_low_cost_full_day (self):
        day = ProjectDay(reimbursement_tier="Low", is_travel_day=False, date=datetime.date(2015, 9, 1))
        
        reimbursement = assess_reimbursement_costs (day)
        
        self.assertEquals(reimbursement, 75)

    def test_reimbursing_high_cost_full_day (self):
        day = ProjectDay(reimbursement_tier="High", is_travel_day=False, date=datetime.date(2015, 9, 1))
        
        reimbursement = assess_reimbursement_costs (day)
        
        self.assertEquals(reimbursement, 85)


if __name__ == '__main__':
    unittest.main()
