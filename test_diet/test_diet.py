import os
import unittest

from diet.diet import Diet
from diet.schemas import input_schema, solution_schema


class TestDiet(unittest.TestCase):

    def setUp(self) -> None:
        # keep a copy of the input data handy for each test
        cwd = os.path.dirname(__file__)
        self.dirty_dat = input_schema.csv.create_tic_dat(
            os.path.join(cwd, "../examples/diet_dirty_sample_data")
        )
        self.dat = input_schema.csv.create_tic_dat(
            os.path.join(cwd, "../examples/diet_sample_data")
        )

    def test_init(self):
        # check that init has model and variables if no errors
        diet = Diet(self.dat)
        self.assertTrue(diet.mdl is not None)
        self.assertTrue(diet.nutrition is not None)
        self.assertTrue(diet.buy is not None)

        # check that init has no model or variables if errors
        diet = Diet(self.dirty_dat)
        self.assertTrue(diet.mdl is None)
        self.assertTrue(diet.nutrition is None)
        self.assertTrue(diet.buy is None)

    def test_check_data_integrity(self):
        # for good input dat, check data integrity returns empty solution dat
        sln = Diet._check_data_integrity(self.dat)
        for table in solution_schema.all_tables:
            self.assertFalse(getattr(sln, table))

        # for bad dat check data integrity returns 4 errors
        sln = Diet._check_data_integrity(self.dirty_dat)
        for table in solution_schema.all_tables:
            if table == "errors":
                self.assertTrue(getattr(sln, table))
            else:
                self.assertFalse(getattr(sln, table))
        self.assertTrue(len(sln.errors) == 4)

    def test_create_model(self):
        # check create model gets objective we expect when solved
        mdl, nutrition, buy = Diet._create_model(self.dat)
        mdl.optimize()
        self.assertAlmostEqual(mdl.objVal, 11.829, places=2)

    def test_solve(self):
        # check solve gets the correct optimal solution when we have a model
        diet = Diet(self.dat)
        sln = diet.solve()
        self.assertAlmostEqual(sln.parameters["Total Cost"]["Value"], 11.829, places=2)
        self.assertAlmostEqual(sln.buy_food["hamburger"]["Quantity"], 0.604, places=2)
        self.assertAlmostEqual(sln.buy_food["milk"]["Quantity"], 6.970, places=2)
        self.assertAlmostEqual(sln.buy_food["ice cream"]["Quantity"], 2.591, places=2)

        # check solve does nothing when we have errors
        diet = Diet(self.dirty_dat)
        sln = diet.solve()
        for table in solution_schema.all_tables:
            if table != "errors":
                self.assertFalse(getattr(sln, table))

    def test_static_solve(self):
        # check static solve works
        sln = Diet.static_solve(self.dat)
        self.assertAlmostEqual(sln.parameters["Total Cost"]["Value"], 11.829, places=2)
        self.assertAlmostEqual(sln.buy_food["hamburger"]["Quantity"], 0.604, places=2)
        self.assertAlmostEqual(sln.buy_food["milk"]["Quantity"], 6.970, places=2)
        self.assertAlmostEqual(sln.buy_food["ice cream"]["Quantity"], 2.591, places=2)


if __name__ == '__main__':
    unittest.main()
