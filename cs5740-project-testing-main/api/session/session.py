from typing import Optional

from api.client.core_client_interface import CoreClientInterface
from api.client.user import User
from api.client.public_client import PublicClient
from api.client.private_client import PrivatePromptClient


class CoreTestUserSession:
    def __init__(self, display_name: Optional[str]):
        self._name = display_name

    def name(self) -> str:
        return self._name


class PublicUserSession(CoreTestUserSession):
    client_cls = PublicClient

    def __init__(self, user: Optional[User] = None, display_name: Optional[str] = None):
        super().__init__(display_name or "Anonymous Public User")
        self.user = user # None if not logged in as admin
        self.client: CoreClientInterface = self.client_cls(user)

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        return await self.client.add_prompt(prompt_data)

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> list[dict]:
        return await self.client.list_prompts(skip, limit)

    async def delete_prompt(self, guid: str) -> None:
        await self.client.delete_prompt(guid)

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        await self.client.update_prompt(guid, updated_data)

    async def get_prompt(self, guid: str) -> dict[str, any]:
        return await self.client.get_prompt(guid)

    async def add_tag_to_prompt(self, guid: str, tag: str) -> None:
        await self.client.add_tag_to_prompt(guid, tag)

    async def remove_tag_from_prompt(self, guid: str, tag: str) -> None:
        await self.client.remove_tag_from_prompt(guid, tag)

    async def list_prompts_by_tags(self, tags: list[str]) -> list[dict]:
        return await self.client.list_prompts_by_tags(tags)


class PrivateUserSession(PublicUserSession):
    client_cls = PrivatePromptClient

    def __init__(self, user: User, display_name: Optional[str] = None):
        if not user:
            raise ValueError("A valid user object is required for PrivateUserSession.")
        super().__init__(user, display_name)
