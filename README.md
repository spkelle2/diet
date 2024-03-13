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
  * Running behind a web service in a Docker container

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

## Running as a Conda Package
To run as a package, download and install Conda as instructed above if you haven't
already. Then, run the following command to download and install the package:
```commandline
conda install spkelle2::diet
```
To confirm that the package installed correctly, run:
```commandline
python -m diet -i /path/to/diet_sample_data -o /path/to/diet_sample_solution
```