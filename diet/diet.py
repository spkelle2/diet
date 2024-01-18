import gurobipy as gp
from typing import Dict, Tuple

from diet.schemas import input_schema, solution_schema


class Diet:
    """
    This class defines and solves the optimization model for the diet problem
    (https://en.wikipedia.org/wiki/Stigler_diet).
    """

    @staticmethod
    def static_solve(dat: input_schema.TicDat) -> solution_schema.TicDat:
        """
        A single function that solves the diet problem. Streamlines the user
        interface.

        :param dat: A TicDat object with the input data for the diet problem.
        :return: A TicDat object with the corresponding solution data for the diet problem.
        """
        diet = Diet(dat)
        return diet.solve()

    def __init__(self, dat: input_schema.TicDat) -> None:

        # record our inputs
        self.input_dat = dat

        # check our inputs and record any errors in the solution
        self.solution_dat = self._check_data_integrity(dat)

        # create placeholder for our model and variables
        self.mdl, self.nutrition, self.buy = None, None, None

        # if no errors, create our model
        if not self.solution_dat.errors:
            self.mdl, self.nutrition, self.buy = self._create_model(dat)

    @staticmethod
    def _check_data_integrity(dat: input_schema.TicDat) -> solution_schema.TicDat:
        """
        Check the validity of the input data against the input schema.

        :param dat: A TicDat object with the input data for the diet problem
        :return: A dictionary of where dat fails to conform to the input schema
        """

        # assert table and field adherence
        assert input_schema.good_tic_dat_object(dat), "tables and fields must match input schema"

        data_errors = []

        # collect data type failures
        for (table, field), (bad_values, primary_keys) in \
                input_schema.find_data_type_failures(dat).items():
            for bad_value, primary_key in zip(bad_values, primary_keys):
                data_errors.append((
                    table, primary_key, 'Data Type Failure',
                    f"{bad_value} violates data type for column '{field}'"
                ))

        # collect foreign key failures
        for (child_table, parent_table, (child_column, parent_column)), primary_keys in \
                input_schema.find_foreign_key_failures(dat, verbosity="Low").items():
            for primary_key in primary_keys:
                data_errors.append((
                    child_table, primary_key, 'Foreign Key Failure',
                    f"The entry in '{child_column}' must exist in column "
                    f"'{parent_column}' of table '{parent_table}'"
                ))

        # collect data row (i.e. check constraint) failures
        for (table, predicate_name), primary_keys in input_schema.find_data_row_failures(dat).items():
            for primary_key in primary_keys:
                data_errors.append((
                    table, primary_key, 'Data Row Failure', predicate_name
                ))

        return solution_schema.TicDat(errors=data_errors)

    @staticmethod
    def _create_model(dat: input_schema.TicDat) -> Tuple[gp.Model, Dict[str, gp.Var], Dict[str, gp.Var]]:
        """
        Create the optimization model for the diet problem.

        :param dat: A TicDat object with the input data for the diet problem
        :return: the model and decision variables
        """

        mdl = gp.Model("diet")

        # Create decision variables for the nutrition consumed for each category
        nutrition = {
            category: mdl.addVar(lb=row["Min Nutrition"], ub=row["Max Nutrition"], name=category)
            for category, row in dat.categories.items()
        }

        # Create decision variables for how much of each food to buy
        buy = {food: mdl.addVar(name=food) for food in dat.foods}

        # Minimize the cost of the foods chosen
        mdl.setObjective(sum(buy[food] * row["Cost"] for food, row in dat.foods.items()),
                         sense=gp.GRB.MINIMIZE)

        # Each category of nutrition must be satisfied by the foods chosen
        for category in dat.categories:
            mdl.addConstr(sum(dat.nutrition_quantities[food, category]["Quantity"] * buy[food]
                              for food in dat.foods) == nutrition[category], name=category)

        # udpate the model so we can inspect
        mdl.update()

        return mdl, nutrition, buy

    def solve(self) -> solution_schema.TicDat:
        """
        If we successfully created a model, solve it and save the solution.

        :return: A TicDat object with solution data for the diet problem
        """

        # if i have this hiding behind a web API, no client could ever trigger this
        # however, a future developer may alter this code, in which case it could happen!
        # same with above assert - in general guardrails for devs beyond what we'd expect a user to hit
        assert bool(self.solution_dat.errors) != bool(self.mdl), "Solve expects exactly " \
            "one of the following: the model exists or errors found in the inputs."

        # if we have no errors
        if not self.solution_dat.errors:

            # solve the model
            self.mdl.optimize()
            assert self.mdl.status == gp.GRB.OPTIMAL, \
                "solve expects the model to have been solved to optimality"

            # and save the solution
            for f, x in self.buy.items():
                if x.x > 0:
                    self.solution_dat.buy_food[f] = x.x
            for c, x in self.nutrition.items():
                self.solution_dat.consume_nutrition[c] = x.x
            self.solution_dat.parameters['Total Cost'] = self.mdl.ObjVal

        return self.solution_dat
