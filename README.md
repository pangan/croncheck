# CronCheck

This application is a CLI for checking a cron config file and
 returns the soonest running time for each command in the config file.
   
By: Amir Mofakhar <amir@mofakhar.info>


# Installing

-  Create a Python 3 virtual environment:
   
  `virtualenv .env`

- Activate the virtual environment:

  `source .env/bin/activate`
  
- Install the requirements:

  `pip install -r requirements.txt`  


# Testing

## Unit test

This application has 100% test coverage.
There are some unit tests and integration tests which can be run by below command:

**Remember to install `test-requirements.txt` before!**

`nosetests tests --verbose --with-coverage --cover-package croncheck`

## PEP8

To check the code style:

`flake8 --max-line-length=100 croncheck` 

# Running

## Method 1

It is possible to run the command by installing it in the virtual environment :

- run below command to install the CLI :
  
  `python setup.py install`

- use below syntax to run the application:

  `croncheck HH:MM<[config_file]`
  
  example: `(.env)$: croncheck 12:25<sample_config`
  
## Method 2

Running the module:

- Go to the root of application and run below command:

  `python -m croncheck.app HH:MM<[config_file]`

