# pytest options

import os
import sys
absolutePathOfCurrentFile = os.path.dirname(os.path.abspath(__file__))
testRootDirectory = os.path.dirname(absolutePathOfCurrentFile)
sys.path.append(testRootDirectory)
from TestUtilities import *

def pytest_addoption(parser):
    parser.addoption("--deploymentType", action="store", default="local")

def pytest_generate_tests(metafunc):
    option_value = metafunc.config.option.deploymentType

    print("opt val: " + option_value)

    if option_value is not None:
        if option_value == "prod":
            backendUrl = TestUtilities.PROD_DEPLOYMENT_URL
        else:
            backendUrl = TestUtilities.LOCAL_DEPLOYMENT_URL

        metafunc.parametrize("backendUrl", [backendUrl])
