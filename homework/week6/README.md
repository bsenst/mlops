# week 6 best practices

## Q1. Refactoring
Before we can start converting our code with tests, we need to refactor it. How does the if statement that we use for this looks like?

```
if __name__ == '__main__':

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    main(year, month)
```

`@bsenst ➜ /workspaces/mlops (main) $ cd homework/week6`

`@bsenst ➜ /workspaces/mlops/homework/week6 (main) $ python -m venv venv && source ./venv/bin/activate`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ pipenv install`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ python batch.py 2022 02`

`predicted mean duration: 12.513422116701408`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ mkdir output`

## Q2. Installing pytest

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ pipenv install --dev pytest`

`(venv) @bsenst ➜ /workspaces/mlops/homework/week6 (main) $ cd test`

`(venv) @bsenst ➜ .../mlops/homework/week6/test (main) $ pytest`

```
=============================================================================== test session starts ===============================================================================
platform linux -- Python 3.10.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /workspaces/mlops/homework/week6/test
collected 1 item                                                                                                                                                                  

test_sample.py F                                                                                                                                                            [100%]

==================================================================================== FAILURES =====================================================================================
___________________________________________________________________________________ test_answer ___________________________________________________________________________________

    def test_answer():
>       assert func(3) == 5
E       assert 4 == 5
E        +  where 4 = func(3)

test_sample.py:9: AssertionError
============================================================================= short test summary info =============================================================================
FAILED test_sample.py::test_answer - assert 4 == 5
================================================================================ 1 failed in 0.04s ================================================================================
```