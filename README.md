# diet

This repository demos how to develop data science projects for production
deployments. The concepts on display in this repository are an abridgment of
Pete Cacioppi's [Tidy, Tested, Safe](https://github.com/ticdat/tidy_tested_safe/wiki)
book and a collection of DevOps best practices I've picked up over the years.
Together, they include:
* Enforcing data science model input data integrity
* Writing unit tests
* Writing assert statements
* Using version control
* Automating installation for:
  * Running in development
  * Running as a Conda package
  * Running as a Docker container
For information, see the companion medium article. 

## Running in Development
If Conda is not already installed on your machine, go [here](https://docs.conda.io/projects/miniconda/en/latest/)
to do so. Then, run the following commands from this project's root directory:
```commandline
conda env create -f environment.yml
conda activate diet
```
To confirm that the environment was created correctly, run:
```commandline
coverage run -m unittest discover
```