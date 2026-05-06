from mcp.server.fastmcp import FastMCP
from google.apps import chat_v1 as google_chat
from auth import google_chat_client, google_people_client
from db import fetch_people
from helpers import normalize_person
from datetime import datetime

mcp = FastMCP("GoogleChatMCP", stateless_http=False, json_response=True)


@mcp.tool()
async def get_spaces():
    """
    List all chat spaces.

    Returns:
        A list of chat spaces with their names and display names.
        {"spaces": [{"name": "spaces/AAA", "display_name": "Space 1"}, ...]}
    """
    request = google_chat.ListSpacesRequest(filter='space_type = "SPACE"')
    page_result = google_chat_client.list_spaces(request)
    spaces = []
    for response in page_result:
        spaces.append({"name": response.name, "display_name": response.display_name})
    return {"spaces": spaces}


@mcp.tool()
async def get_members(space_name: str):
    """
    List all members of a chat space.

    Args:
        space_name: The name of the chat space.
    Returns:
        A list of members with their names, types, roles, and states.
        {"members": [{"name": "members/AAA", "member_name": "John Doe", "member_type": "HUMAN", "role": "MEMBER", "state": "ACTIVE"}, ...]}
    """
    request = google_chat.ListMembershipsRequest(
        parent=space_name, filter='member.type = "HUMAN"', page_size=25
    )
    memberships = google_chat_client.list_memberships(request)
    members = []
    for membership in memberships:
        members.append(normalize_person(membership))

    member_ids = list(map(lambda m: m["id"], members))
    people_db = fetch_people(member_ids)
    for m in members:
        person = people_db.get(m["id"])
        if person:
            m["member_display_name"] = person["display_name"]

    return {
        "members": members,
    }


@mcp.tool()
async def get_member(member_name: str):
    """
    Get details about a specific member of a chat space.
    """
    request = google_chat.GetMembershipRequest(name=member_name)
    member = google_chat_client.get_membership(request)
    member = normalize_person(member)
    people_db = fetch_people([member["id"]])

    person = people_db.get(member["id"])
    if person:
        member["member_display_name"] = person["display_name"]

    return {"member": member}


@mcp.tool()
async def get_messages(space_name: str, filter: str = ""):
    """
    List messages in a chat space.
    Filter should be in the format: 'create_time > "2026-05-05T00:00:00+00:00" AND create_time < "2026-05-06T00:00:00+00:00"'
    Only use greater than and less than filters on create_time for now to avoid complexity.

    Returns:
        A list of messages with their names, create times, text content, and sender information.
        {"messages": [{"name": "spaces/AAA/messages/BBB", "create_time": "2026-05-05T12:34:56Z", "text": "Hello, world!", "sender": {"name": "users/CCC", "display_name": "John Doe"}}, ...]}
    """
    if not filter:
        # TODO: default filter from date library
        now = datetime.now().isoformat() + "Z"
        first_time_of_day = now.split("T")[0] + "T00:00:00Z"
        last_time_of_day = now.split("T")[0] + "T23:59:59Z"

        filter = f'create_time > "{first_time_of_day}" AND create_time < "{last_time_of_day}"'

    filter = filter.replace(">=", ">").replace("<=", "<")

    request = google_chat.ListMessagesRequest(
        parent=space_name,
        page_size=25,
        order_by="create_time ASC",
        filter=filter,
    )
    messages = google_chat_client.list_messages(request)
    messages_list = []
    for message in messages:
        messages_list.append(
            {
                "name": message.name,
                "create_time": message.create_time,
                "text": message.text,
                "sender": {
                    "id": message.sender.name.split("/")[-1],
                    "name": message.sender.name,
                },
            }
        )

    member_ids = list(set([m["sender"]["id"] for m in messages_list]))
    people_db = fetch_people(member_ids)
    for m in messages_list:
        person = people_db.get(m["sender"]["id"])
        if person:
            m["sender"]["display_name"] = person["display_name"]

    return {"messages": messages_list}


if __name__ == "__main__":
    # mcp.run(transport="streamable-http")
    mcp.run(transport="stdio")
