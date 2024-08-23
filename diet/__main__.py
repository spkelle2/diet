from ticdat.utils import standard_main

from diet.diet import Diet
from diet.schemas import input_schema, solution_schema


def main() -> None:
    """
    This function serves as the user interface when interacting with the diet package directly
    :return:
    """
    standard_main(input_schema, solution_schema, Diet.static_solve)


if __name__ == '__main__':
    main()
