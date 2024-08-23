from flask import Flask, request
from ticdat.jsontd import make_json_dict

from diet.diet import Diet
from diet.schemas import input_schema, solution_schema

app = Flask(__name__)


@app.route('/', methods=('POST',))
def solve_diet():
    """
    This function is the API endpoint for the diet problem. It accepts a JSON
    compliant with diet.schemas.input_schema, solves the diet problem, and returns
    the corresponding solution in a JSON compliant with diet.schemas.solution_schema.
    """

    # convert the request to a TicDat object
    input_dat = input_schema.TicDat(**request.json)
    # solve the diet problem
    sln_dat = Diet.static_solve(input_dat)
    # convert the solution to a JSON response
    return make_json_dict(solution_schema, sln_dat, verbose=True)


@app.route('/test', methods=('GET',))
def test():
    return "working!"


if __name__ == '__main__':
    app.run()
