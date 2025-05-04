You are a QA developer expert in Python, using the pytest framework.
You're writing tests for an API, described as:
```
{api-description}
```

The architecture of the test cases is three layers:
1. Core client layer (folder=client)
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

Let's use aiohttp for our core client layer.
Let's generate two core client classes, one for private and one for public prompts.
Let's allow these classes to read the .env for TEST_USERNAME.
Every time we make a public or private prompt, we must automatically add a tag "pytest-{TEST_USERNAME}" if it is not present already.
This will let us clean up our database.

Let's use pytest for our test user session layer.
This layer will introduce a class called TestUserSession.
Each session will hold a reference to a core client, and will have a username and password for private, or none for public.
In fact let's make a PrivateTestUserSession and a PublicTestUserSession.


Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  Each test case should be in a file named test_{test-case-name}.py.
Each test case should be a class named Test{test-group-name}.
Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
Each method should have a docstring that describes the test case.
ANy prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

We will also need the following fixtures:
* A fixture that runs after each test case to delete all prompts that are tagged as "pytest-{TEST_USERNAME}".
