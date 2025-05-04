# Using AI tools
Prompt: Project 8 requirements. Use AI tools to analyze the contents of Project 8 and provide a step-by-step solution to complete the project

# Test Plan

## Overview
This document describes the testing strategy for our CodePromptu integration. We focus on creating, retrieving, updating, and deleting prompts, ensuring both public and private permissions are respected.

## Test Categories

1. **Creation (C in CRUD)**  
   - We test creation of prompts by different users (Adrianna, Bob, and Alice).  
   - We check normal scenarios, as well as boundary scenarios (e.g., empty display name, large content).

2. **Retrieval (R in CRUD)**  
   - We ensure a user can retrieve their own created prompts, either public or private.  
   - We test retrieval of non-existent prompts, expecting errors.

3. **Updating (U in CRUD)**  
   - We verify that users can update their own prompts, such as updating tags.
   - We confirm unauthorized users cannot update others’ prompts.

4. **Deletion (D in CRUD)**  
   - We test unauthorized deletion scenarios to ensure users cannot delete prompts they do not own.

5. **Permission / Access Control**  
   - We test that Alice, who has read-only permission, cannot create prompts.
   - We confirm that Adrianna cannot retrieve Bob’s private prompts.

6. **Boundary / Edge Cases**  
   - Large content  
   - Special characters in prompt content  
   - Empty display name  
   - Non-existent GUID retrieval  


## Failing Tests

### 1. `test_adrianna_create_no_tags`
- **Status**: Currently fails because the system automatically adds the tag `pytest-qiyuan`.  
- **Cause**: Our test expects an empty list, but the API never returns an actually empty `tags` array.  
- **Resolution**: We could adjust the code to remove or ignore `pytest-qiyuan`, or accept that this is intended behavior.

### 2. `test_adrianna_update_prompt_tags`
- **Status**: Fails for the same `pytest-qiyuan` reason. Even after updating tags, the `pytest-qiyuan` tag remains.  
- **Cause**: The test expects the tags to match `[newTag1, newTag2]`, but we get `[newTag1, newTag2, pytest-qiyuan]`.  
- **Resolution**: We could modify our assertion to allow for extra tags or remove them in the server logic.

### 3. `test_bob_create_duplicate_prompt_fails` (Intentionally Failing)
- **Status**: Intentionally fails. We assume the system *disallows* duplicates, but it still returns a valid GUID.  
- **Purpose**: Demonstrates a failing scenario that highlights a possible unimplemented feature (duplicate-checking).

## Conclusion
These tests collectively ensure coverage of:
- Basic CRUD operations
- Permission boundaries
- Handling of edge cases
- Known or intentional failing scenarios (including automatic tags and duplicate display names)

If we want exactly one failing test for demonstration, we will fix or skip the first two. Otherwise, we keep them failing to highlight real or unexpected behaviors in the system.
