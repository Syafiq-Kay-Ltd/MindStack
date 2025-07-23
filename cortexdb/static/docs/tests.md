# Guide to Testing in CortexDB

- based on `pytest` and Test-Driven Development framework

## Anatomy of a test

Source: <https://docs.pytest.org/en/stable/explanation/anatomy.html>

- the purpose of a test is to examine the result of a particular behaviour to ensure that the result aligns with expectation
- behaviour: "the way in which some system acts in response to a particular situaton and/or stimuli"
- tests can be broken down into four steps:
    1. Arrange - prepare everything for the test
    2. Act - the singular state changing action that triggers the behaviour we want to test - function or method call
    3. Assert - look for the resulting state and check if it looks how we expect
    4. Cleanup - tidy up so that it does not accidentally influence other test

