from typing import List, Optional

import aiohttp
from dotenv import load_dotenv
import os

from api.client.api_exception import ApiException

load_dotenv()

from api.client.core_client_interface import CoreClientInterface
from api.client.user import User


class PublicClient(CoreClientInterface):
    BASE_URL = os.getenv("BASE_URL")
    TEST_USERNAME = os.getenv('TEST_USERNAME')

    def __init__(self, user: Optional[User] = None):
        self.auth = None
        if user:
            self.auth = user.get_basic_auth()
        self._discriminator_tag = "pytest-" + self.TEST_USERNAME

    async def _ensure_discriminator_tag(self, prompt_data):
        prompt_data["tags"] = list(set(prompt_data.get("tags", []) + [self._discriminator_tag]))  # Ensuring "pytest" tag

    async def _handle_response(self, response, expected_status=None):
        is_error_response: bool = response.status >= 400
        if is_error_response or expected_status and response.status != expected_status:
            error_json = await response.json()
            raise ApiException(response.status, error_json.get('detail'), error_json.get('traceback'))
        return response

    async def add_prompt(self, prompt_data: dict[str, any]) -> str:
        async with aiohttp.ClientSession() as session:
            await self._ensure_discriminator_tag(prompt_data)
            response = await session.post(f'{self.BASE_URL}/public/prompt/', json=prompt_data, auth=self.auth)
            await self._handle_response(response)
            return (await response.text()).strip('"')

    async def list_prompts(self, skip: int = 0, limit: int = 10) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{self.BASE_URL}/public/prompt/?skip={skip}&limit={limit}')
            await self._handle_response(response)
            return await response.json()

    async def delete_prompt(self, guid) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.delete(f'{self.BASE_URL}/public/prompt/{guid}', auth=self.auth)
            await self._handle_response(response, expected_status=204)

    async def update_prompt(self, guid: str, updated_data: dict[str, any]) -> None:
        async with aiohttp.ClientSession() as session:
            await self._ensure_discriminator_tag(updated_data)
            response = await session.put(f'{self.BASE_URL}/public/prompt/{guid}', json=updated_data, auth=self.auth)
            await self._handle_response(response, expected_status=204)

    async def get_prompt(self, guid: str) -> dict[str, any]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{self.BASE_URL}/public/prompt/{guid}')
            await self._handle_response(response)
            return await response.json()

    async def list_prompts_by_tags(self, tags: List[str]) -> List[dict]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(f'{self.BASE_URL}/public/prompt/tags/?tags={",".join(tags)}')
            await self._handle_response(response)
            return await response.json()

    async def add_tag_to_prompt(self, guid: str, tag: str) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.post(f'{self.BASE_URL}/private/prompt/{guid}/tag/{tag}', auth=self.auth)
            await self._handle_response(response, expected_status=204)

    async def remove_tag_from_prompt(self, guid: str, tag: str) -> None:
        async with aiohttp.ClientSession() as session:
            response = await session.delete(f'{self.BASE_URL}/private/prompt/{guid}/tag/{tag}', auth=self.auth)
            await self._handle_response(response, expected_status=204)

