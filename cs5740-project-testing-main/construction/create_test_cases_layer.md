You are a QA developer expert in Python, using the pytest framework.

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

You have these session layer classes:
```
{session_layer_classes}
```

We have a User class that holds a username and password.
```
{user_class}
```

Let's have a common class where we can put common fixtures and helper methods.
Let's call it BaseTest.
In there we should read in our test user from a .env file using the python-dotenv library.
Keys are TEST_USERNAME and TEST_PASSWORD.  
We should also have a fixture that returns a public session without a user (called Alice), and a private session with a user (called Bob).
Also we need fixture that runs after each test case to delete all prompts that are tagged as "pytest".

Let's now consider constructing the test case layer.

Every test class should inherit from BaseTest.
We should have one or more test cases per class.
Each test case should be a class named Test{test-group-name}.
Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
Each method must have a docstring that describes the test case.
Any prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  

Let's pause to breath and think of what we can do with this api.
We have prompts we can create publicly or privately.
The content of a prompt can contain variables, tags and one classification.
Variable syntax forms are: {input}, {output}, {input?}, {output!}, {input:mime-type-format}, {output!:mime-type-format}, {input:mime-type-format:description}, {output!:mime-type-format:description}.
Tags are just strings.  A prompt can have multiple tags.
Classifications are just strings.

If Bob creates a private prompt, only Bob can see it, Alice cannot.
If you create a public prompt, everyone can see it including Alice.

We have facilities to create a prompt (getting a guid) with fields content, tags and classification specified,
look at a prompt by guid, delete a prompt by guid, update a prompt by guid with fields content, tags and classification specified,
and list prompts by text search, tags and classification.

Using this, let's write some test cases with Alice and Bob, and see what we can do
to test the API for exhaustive coherent behavior.

