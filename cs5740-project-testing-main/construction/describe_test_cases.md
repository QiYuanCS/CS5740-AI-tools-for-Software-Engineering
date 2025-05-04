You are a QA developer expert in Python, using the pytest framework.

The architecture of the test cases is three layers:
1. Core client layer (folder=client) 
2. Test user session layer (folder=session)
3. Test Case layer (folder=test)

You have this test case layer base class:
```
{base_test_class}
```

You have these session layer classes:
```
{session_layer_classes}
```

We have a User class that holds a username and password.
```
{user_class}
```

Let's now consider constructing the test case layer.

* Every test class should inherit from BaseTest.
* They should all be marked with `@pytest.mark.asyncio` to indicate they are async.
* We should have one or more test cases per class.
* Each test case should be a class named Test{test-group-name}.
* Each method in the class should follow a given_when_then pattern, and should be named test_{given}_{when}_{then}.
* Each test method must have a docstring that describes the test case in a given_when_then manner
* Any prompts, tags and classification data to support the test case should be generated in the test case class's setup method, as a fixture.

Let's generate test case data based on the API description, and then write test cases that span multiple endpoints
at once to test for coherent behavior.  

Let's pause to breath and think of what we can do with this api.
We have prompts we can create publicly or privately.
The content of a prompt can contain a display_name, text content, and a list of tags.
Tags are just strings.  A prompt can have multiple tags.

If Bob creates a private prompt, only Bob can see it, Alice cannot.
If Alice creates a public prompt, everyone can see it including Alice but only if they use the /public endpoint.

We have facilities to create a prompt (getting a guid) with fields content, tags and display_name specified,
look at a prompt by guid, delete a prompt by guid, update a prompt by guid with fields content, tags, display_name specified,
list prompts by tag names, add and remove tags from a prompt.

Using this, let's come up with English description of test cases in groups related to the functionality they are testing.  
Make sure the English will be understood to generate code in a later step.
Let's now consider constructing the test case layer.


