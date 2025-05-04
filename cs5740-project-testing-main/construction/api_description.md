
### `/public/prompt/`

- **POST**
  - **Summary**: Add a new prompt. Requires an admin user.
  - **Parameters**: None
  - **Body**: Required, based on `PromptCreate` schema
  - **Responses**: 201 (Successful Response), 422 (Validation Error)

- **GET**
  - **Summary**: List all prompts.
  - **Parameters**: `skip` (optional, integer, default 0), `limit` (optional, integer, default 10)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/public/prompt/{guid}`

- **DELETE**
  - **Summary**: Delete a prompt by GUID. Requires an admin user.
  - **Parameters**: `guid` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **PUT**
  - **Summary**: Update a prompt by GUID. Requires an admin user.
  - **Parameters**: `guid` (required, string)
  - **Body**: Required, based on `PromptUpdate` schema
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **GET**
  - **Summary**: Retrieve a prompt by GUID.
  - **Parameters**: `guid` (required, string)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/public/prompt/name/{name}`

- **GET**
  - **Summary**: Retrieve a prompt by name.
  - **Parameters**: `name` (required, string)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/public/prompt/tags/`

- **GET**
  - **Summary**: List Public Prompts by Tag.
  - **Parameters**: `tags` (optional, string, comma-separated list of tags)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/public/prompt/{guid}/tag/{tag}`

- **POST**
  - **Summary**: Add a tag to a prompt by GUID. Requires an admin user.
  - **Parameters**: `guid` (required, string), `tag` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **DELETE**
  - **Summary**: Remove a tag from a prompt by GUID. Requires an admin user.
  - **Parameters**: `guid` (required, string), `tag` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

### `/private/prompt/`

- **POST**
  - **Summary**: Add a new private prompt. Requires a logged-in user.
  - **Parameters**: None
  - **Body**: Required, based on `PromptCreate` schema
  - **Responses**: 201 (Successful Response), 422 (Validation Error)

- **GET**
  - **Summary**: List all private prompts of the logged-in user.
  - **Parameters**: `skip` (optional, integer, default 0), `limit` (optional, integer, default 10)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/private/prompt/{guid}`

- **DELETE**
  - **Summary**: Delete a private prompt by GUID. Requires the owner of the prompt.
  - **Parameters**: `guid` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **PUT**
  - **Summary**: Update a private prompt by GUID. Requires the owner of the prompt.
  - **Parameters**: `guid` (required, string)
  - **Body**: Required, based on `PromptUpdate` schema
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **GET**
  - **Summary**: Retrieve a private prompt by GUID.
  - **Parameters**: `guid` (required, string)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/private/prompt/name/{name}`

- **GET**
  - **Summary**: Retrieve a private prompt by name.
  - **Parameters**: `name` (required, string)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/private/prompt/tags/`

- **GET**
  - **Summary**: List Private Prompts by Tag.
  - **Parameters**: `tags` (optional, string, comma-separated list of tags)
  - **Responses**: 200 (Successful Response), 422 (Validation Error)

### `/private/prompt/{guid}/tag/{tag}`

- **POST**
  - **Summary**: Add a tag to a private prompt by GUID. Requires the owner of the prompt.


 - **Parameters**: `guid` (required, string), `tag` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)

- **DELETE**
  - **Summary**: Remove a tag from a private prompt by GUID. Requires the owner of the prompt.
  - **Parameters**: `guid` (required, string), `tag` (required, string)
  - **Responses**: 204 (Successful Response), 422 (Validation Error)
