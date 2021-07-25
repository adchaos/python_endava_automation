# python_selenium_endava

# SELENIUM_AUTOMATION

The actual test code is written in Python 3.
Framework: pytest
Tools: allure, xdist and selenium

## Requirements
* Python 3

## For installation
* allure
* pytest
* allure-pytest
* webdriver-manager
* pytest-xdistz

## Running The Tests
Executes 1 instance of webDriver and generate results for allure report.
To execute the available tests from command line use the following command in the root directory of the project:

* pytest  -n 1 test_sample.py --alluredir ./result/

## Allure eport
Start web server with HTML report after the test execution:

* allure serve ./result/ -o ./report/ --clean 
