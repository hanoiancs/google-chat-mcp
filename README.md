### How to install:
#### 0. Clone code:
Clone this repository to a folder in your computer. Example:
```
/Users/hanoiancs/code/google-chat-mcp
```

#### 1. Install `uv` tool:

```bash
# https://docs.astral.sh/uv/getting-started/installation/

# Install for Mac and Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 2. Create Google Cloud Project and OAuth credentials:

Go to [Google Cloud Console](https://console.cloud.google.com/) and create new project or use an existing one.

Go to `API & Services` -> `Credentials` -> `Create credentials` -> `OAuth client ID`.

Download and save the credentials to `credentials.json` file.

Enable `Google Chat API` with the following scopes:
```
https://www.googleapis.com/auth/contacts.readonly,
https://www.googleapis.com/auth/contacts.other.readonly,
https://www.googleapis.com/auth/chat.spaces.readonly,
https://www.googleapis.com/auth/chat.memberships.readonly,
https://www.googleapis.com/auth/chat.messages.readonly,
https://www.googleapis.com/auth/chat.users.readstate.readonly,
https://www.googleapis.com/auth/chat.users.sections.readonly
```

Go to `Google Chat API` [configuration page](https://console.cloud.google.com/apis/api/chat.googleapis.com/hangouts-chat) and config your app.

- Application Info: Random info.
- Avatar URL: You can use `https://developers.google.com/chat/images/quickstart-app-avatar.png` or your avatar image.
- Description: Random description.


#### 3. Generate access token file:
Run following script to generate `token.json` file.
```bash
uv run auth.py
```

#### 4. Config MCP server in supported tools:

```json
{
  "mcpServers": {
    "GoogleChatMCP": {
      "command": "/Users/hanoiancs/.local/bin/uv",
      "args": [
        "run",
        "--directory",
        "/Users/hanoiancs/code/google-chat-mcp",
        "--frozen",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/Users/hanoiancs/code/google-chat-mcp/server.py"
      ]
    }
  }
}
```