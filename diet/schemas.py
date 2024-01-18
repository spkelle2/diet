"""
The objects in this file define the schemas for inputs and solutions to the
optimization model solved within the Diet class in this package.
"""

from ticdat import TicDatFactory

# ------------------------ define the input schema --------------------------------
# Declare the tables, fields, and primary keys
input_schema = TicDatFactory(
    categories=[["Name"], ["Min Nutrition", "Max Nutrition"]],
    foods=[["Name"], ["Cost"]],
    nutrition_quantities=[["Food", "Category"], ["Quantity"]]
)

# Define the foreign key relationships
input_schema.add_foreign_key("nutrition_quantities", "foods", ["Food", "Name"])
input_schema.add_foreign_key("nutrition_quantities", "categories",
                            ["Category", "Name"])

# Define the data types
input_schema.set_data_type("categories", "Min Nutrition", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)
input_schema.set_data_type("categories", "Max Nutrition", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=True)
input_schema.set_data_type("foods", "Cost", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)
input_schema.set_data_type("nutrition_quantities", "Quantity", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)

# Define check constraints (ensure Max Nutrition doesn't fall below Min Nutrition)
input_schema.add_data_row_predicate(
    "categories", predicate_name="Max Nutrition must be >= Min Nutrition",
    predicate=lambda row: row["Max Nutrition"] >= row["Min Nutrition"]
)

# Fields by default take a default value of 0. This makes sense everywhere
# except for Max Nutrition
input_schema.set_default_value("categories", "Max Nutrition", float("inf"))


# ------------------------ define the solution schema -----------------------------
# Declare the tables, fields, and primary keys
solution_schema = TicDatFactory(
    parameters=[["Parameter"], ["Value"]],
    buy_food=[["Food"], ["Quantity"]],
    consume_nutrition=[["Category"], ["Quantity"]],
    errors=[[], ["Table", "Primary Key", "Failure Type", "Message"]]
)
