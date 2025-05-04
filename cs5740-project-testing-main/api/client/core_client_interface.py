from typing import List, Optional, Protocol


class CoreClientInterface(Protocol):

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        ...

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> List[dict]:
        ...

    async def delete_prompt(self, guid: str) -> None:
        ...

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        ...

    async def get_prompt(self, guid: str) -> dict[str, any]:
        ...


    async def list_prompts_by_tags(self, tags: List[str]) -> List[dict]:
        ...

    async def add_tag_to_prompt(self, guid: str, tag: str) -> None:
        """Adds a tag to a prompt specified by its GUID.

        Args:
            guid (str): The unique identifier for the prompt.
            tag (str): The tag to add to the prompt.

        Raises:
            Exception: If the operation is unsuccessful.
        """

    async def remove_tag_from_prompt(self, guid: str, tag: str) -> None:
        """Removes a tag from a prompt specified by its GUID.

        Args:
            guid (str): The unique identifier for the prompt.
            tag (str): The tag to remove from the prompt.

        Raises:
            Exception: If the operation is unsuccessful.
        """
