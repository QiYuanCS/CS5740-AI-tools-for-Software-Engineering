Here are descriptions of test cases in groups related to the functionality they are testing.
```
{test-cases-description}
```

Let's come up with a list of proposed class names, and then for each test class lets write out the full code. Pause
after each class and wait for my go-ahead to continue. Be as comprehensive with test case generation as you can. Also,
remember to use adrianna not alice to create or update prompts.

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

Using this, let's write some test case classes with Alice, Adrianna and Bob, and see what we can do
to test the API for exhaustive coherent behavior.

