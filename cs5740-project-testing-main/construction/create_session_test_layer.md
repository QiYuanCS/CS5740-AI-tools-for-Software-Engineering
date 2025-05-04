You are a QA developer expert in Python, using the pytest framework.

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

You have core layer classes:
```
{core_layer_classes}
```


Let's use pytest for our test user session layer.
This layer will introduce a class called UserSession.
Each session will hold a reference to a public and a private core layer client.
The session should take a User object as a parameter.


Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  Each test case should be in a file named test_{test-case-name}.py.
Each test case should be a class named Test{test-case-name}.
Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
Each method should have a docstring that describes the test case.
ANy prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

We will also need the following fixtures:
* A fixture that runs after each test case to delete all prompts that are tagged as "pytest".
