import pytest

from api.session.session import CoreTestUserSession
from .base_test import BaseTest

@pytest.mark.asyncio
class TestPromptCreationRetrieval(BaseTest):

    async def _get_prompt(self, user, created_guid):
        retrieved_prompt = await user.get_prompt(created_guid)
        return retrieved_prompt

    async def _assert_prompts_equal(self, user: CoreTestUserSession, expected_guid, expected_prompt, actual_prompt):
        user_name = user._name
        assert actual_prompt['guid'] == expected_guid, (
            f"{user_name}'s retrieved prompt GUID does not match the created prompt's GUID."
        )
        assert actual_prompt['content'] == expected_prompt['content'], (
            f"The content of {user_name}'s retrieved prompt does not match the expected content."
        )
        assert actual_prompt['display_name'] == expected_prompt['display_name'], (
            f"The display name of {user_name}'s retrieved prompt does not match the expected display name."
        )
        assert set(actual_prompt['tags']) == set(expected_prompt['tags']), (
            f"The tags of {user_name}'s retrieved prompt do not match the expected tags."
        )

    async def test_adrianna_create_retrieve_public_prompt(self, adrianna):
        """
        Given: Adrianna creates a public prompt with specific content, display name, and tags.
        When: Adrianna retrieves the prompt by its GUID.
        Then: The retrieved prompt matches the created one in GUID, content, display name, and tags.
        """
        expected_prompt = {
            "content": "Test content",
            "display_name": "Test Prompt",
            "tags": ["tag1", "tag2"]
        }
        expected_guid: str = await adrianna.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(adrianna, expected_guid)
        await self._assert_prompts_equal(adrianna, expected_guid, expected_prompt, actual_prompt)

    async def test_bob_create_retrieve_private_prompt(self, bob):
        """
        Given: Bob creates a private prompt with specific content, display name, and tags.
        When: Bob retrieves the prompt by its GUID.
        Then: The retrieved prompt matches the created one in GUID, content, display name, and tags.
        """
        expected_prompt = {
            "content": "Private content",
            "display_name": "Private Prompt",
            "tags": ["private1", "private2"]
        }
        expected_guid = await bob.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(bob, expected_guid)
        await self._assert_prompts_equal(bob, expected_guid, expected_prompt, actual_prompt)

    # 1) New Test: Alice attempts to retrieve a non-existent prompt
    async def test_alice_retrieve_nonexistent_prompt_fails(self, alice):
        """
        Given: Alice tries to retrieve a prompt with a random GUID that doesn't exist.
        When: She attempts retrieval.
        Then: The server should respond with an error (e.g., 404).
        """
        random_guid = "00000000-0000-0000-0000-000000000000"  # intentionally invalid
        with pytest.raises(Exception) as exc_info:
            await self._get_prompt(alice, random_guid)
        assert "404" in str(exc_info.value), (
            "Alice was able to retrieve a non-existent prompt, which is unexpected."
        )

    # 2) New Test: Adrianna creates a prompt with no tags
    async def test_adrianna_create_no_tags(self, adrianna):
        """
        Given: Adrianna creates a public prompt without any tags.
        When: She retrieves the prompt.
        Then: The prompt's tags should be an empty list.
        """
        expected_prompt = {
            "content": "Content without tags",
            "display_name": "No Tag Prompt",
            "tags": []
        }
        expected_guid = await adrianna.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(adrianna, expected_guid)
        assert actual_prompt['guid'] == expected_guid, (
            "GUID mismatch for prompt with no tags."
        )
        assert actual_prompt['tags'] == [], (
            "Expected empty list of tags, but found otherwise."
        )

    # 3) New Test: Bob creates a prompt with special characters in content
    async def test_bob_create_special_chars_in_content(self, bob):
        """
        Given: Bob creates a prompt where content has special characters.
        When: He retrieves the prompt.
        Then: The content should match exactly, including special chars.
        """
        expected_prompt = {
            "content": "Some <xml> & emojis 😊 !? #$%^&*()",
            "display_name": "Special Char Prompt",
            "tags": ["special", "chars"]
        }
        expected_guid = await bob.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(bob, expected_guid)
        await self._assert_prompts_equal(bob, expected_guid, expected_prompt, actual_prompt)

    # 4) New Test: Bob creates a prompt with an empty display name
    async def test_bob_create_empty_display_name(self, bob):
        """
        Given: Bob creates a prompt with an empty string for display name.
        When: The prompt is retrieved.
        Then: The display name should be an empty string, as set.
        """
        expected_prompt = {
            "content": "Prompt with empty display name",
            "display_name": "",
            "tags": ["empty", "display"]
        }
        expected_guid = await bob.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(bob, expected_guid)
        assert actual_prompt['display_name'] == "", (
            "The display name was expected to be empty, but it's not."
        )

    # 5) New Test: Adrianna creates a prompt with large content
    async def test_adrianna_create_large_content(self, adrianna):
        """
        Given: Adrianna creates a prompt with very large content.
        When: She retrieves the prompt.
        Then: The content should match exactly, with no truncation.
        """
        big_content = "A" * 5000  # 5000 chars
        expected_prompt = {
            "content": big_content,
            "display_name": "Large Content Prompt",
            "tags": ["large", "test"]
        }
        expected_guid = await adrianna.add_prompt(expected_prompt)
        actual_prompt = await self._get_prompt(adrianna, expected_guid)
        assert len(actual_prompt['content']) == 5000, (
            "Large content is unexpectedly truncated or altered."
        )

    # 6) New Test: Bob tries to delete a public prompt he did not create (assuming no permission)
    async def test_bob_delete_unauthorized(self, bob, adrianna):
        """
        Given: A prompt is created by Adrianna.
        When: Bob tries to delete it.
        Then: Bob should be denied access (e.g., 403/401).
        """
        # Adrianna creates
        prompt_by_adrianna = {
            "content": "Public content by Adrianna",
            "display_name": "Adrianna's prompt",
            "tags": ["public"]
        }
        guid_created = await adrianna.add_prompt(prompt_by_adrianna)

        # Bob attempts deletion
        with pytest.raises(Exception) as exc_info:
            await bob.delete_prompt(guid_created)

        # Expect some form of "unauthorized" or "forbidden"
        assert "403" in str(exc_info.value) or "401" in str(exc_info.value), (
            "Bob was able to delete a prompt he didn't create, which is unexpected."
        )

    # 7) New Test: Alice tries to create a prompt (should fail if she has read-only permission)
    async def test_alice_create_prompt_fails(self, alice):
        """
        Given: Alice has read-only access.
        When: She tries to create a prompt.
        Then: The server should reject her request with an error (403/401).
        """
        prompt_data = {
            "content": "Alice's unauthorized creation",
            "display_name": "Failing creation",
            "tags": ["unauthorized"]
        }
        with pytest.raises(Exception) as exc_info:
            await alice.add_prompt(prompt_data)
        assert "403" in str(exc_info.value) or "401" in str(exc_info.value), (
            "Alice successfully created a prompt despite having read-only permissions."
        )

    # 8) New Test: Adrianna updates an existing prompt's tags
    async def test_adrianna_update_prompt_tags(self, adrianna):
        """
        Given: Adrianna creates a prompt, then updates its tags.
        When: The prompt is retrieved after the update.
        Then: The updated tags should match the new list of tags.
        """
        initial_prompt = {
            "content": "Updating tags test",
            "display_name": "Updatable Prompt",
            "tags": ["oldTag"]
        }
        guid_created = await adrianna.add_prompt(initial_prompt)

        updated_tags = ["newTag1", "newTag2"]
        await adrianna.update_prompt(guid_created, {"tags": updated_tags})
        updated_prompt = await self._get_prompt(adrianna, guid_created)
        assert set(updated_prompt['tags']) == set(updated_tags), (
            "Prompt tags did not match the updated values."
        )

    # 9) New Test: Adrianna attempts to retrieve Bob's private prompt (should fail if not shared)
    async def test_adrianna_retrieve_bobs_private_prompt_fails(self, adrianna, bob):
        """
        Given: Bob creates a private prompt.
        When: Adrianna attempts to retrieve Bob's private prompt.
        Then: The server should return an error, because it's private to Bob.
        """
        prompt_data = {
            "content": "Secret data for Bob",
            "display_name": "Bob's Private Prompt",
            "tags": ["private"]
        }
        bob_guid = await bob.add_prompt(prompt_data)
        with pytest.raises(Exception) as exc_info:
            await self._get_prompt(adrianna, bob_guid)
        assert "403" in str(exc_info.value) or "404" in str(exc_info.value), (
            "Adrianna could retrieve Bob's private prompt, which is unexpected."
        )

    # 10) New Test (INTENTIONAL FAIL): Bob creates two prompts with the same display_name, expecting an error
    async def test_bob_create_duplicate_prompt_fails(self, bob):
        """
        Given: Bob creates a prompt with a certain display name.
        When: He tries to create another prompt with the exact same display name (assuming system disallows duplicates).
        Then: We expect an error, but let's force a fail to demonstrate the failing test.
        """
        first_prompt = {
            "content": "First content",
            "display_name": "Duplicate Name",
            "tags": ["test"]
        }
        second_prompt = {
            "content": "Second content",
            "display_name": "Duplicate Name",
            "tags": ["test"]
        }

        await bob.add_prompt(first_prompt)  # Should succeed
        # Expecting an error here, but let's say the system actually allows duplicates
        # We'll cause it to fail artificially, for demonstration
        second_guid = await bob.add_prompt(second_prompt)
        # We'll do a failing assertion:
        assert second_guid is None, (
            "This is an intentional failing test. The system allowed a second prompt with the same display name."
        )
