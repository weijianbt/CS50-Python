from project import validate_bank
import project

def test_validate_bank():
    assert(validate_bank("")) == False
    assert(validate_bank("BankA")) == True

def test_validate_principal_amount():

    #only whole number > 0 without any formatting allowed
    test_case = {
        0           : False,
        -1          : False,
        "0"         : False,
        "10,000"    : False,
        " "         : False,
        ""          : False,
        1000        : 1000
    }

    results = {}
    for input_value, expected_result in test_case.items():
        result = project.validate_principal_amount(input_value)
        results[input_value] = result

    assert results == test_case


def test_validate_interest():

    #only numbers > 0, can be allowed. Decimals are allowed
    test_case = {
        1: True,
        0: False,
        0.1: True,
        "1%" : False,
        "A" : False,
        "" : False,
        " " : False
    }

    results = {}
    for input_value, expected_result in test_case.items():
        result = project.validate_interest(input_value)
        results[input_value] = result

    assert results == test_case

def test_validate_tenure():
    #only whole numbers > 0 can be allowed.
    test_case = {
        1: True,
        0: False,
        0.1: False,
        "A" : False,
        "" : False,
        " " : False
    }

    results = {}
    for input_value, expected_result in test_case.items():
        result = project.validate_tenure(input_value)
        results[input_value] = result

    assert results == test_case


def test_validate_deposit_date():
    test_case = {
        "2023-1-1": True,
        "2023-01-01": True,
        "2023-99-99": False,
        0: False,
        "A" : False,
        "" : False,
        " " : False
    }

    results = {}
    for input_value, expected_result in test_case.items():
        result = project.validate_deposit_date(input_value)
        results[input_value] = result

    assert results == test_case

