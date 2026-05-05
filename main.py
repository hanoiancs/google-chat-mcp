
# from google.oauth2.service_account import Credentials
from google.apps import chat_v1 as google_chat
from googleapiclient.discovery import build
from auth import get_client, auth


def main():
    """Shows basic usage of the Google Chat API."""
    try:
        # Create a client
        client = get_client()

        # Initialize request argument(s)
        # request = google_chat.ListSpacesRequest(
        #     # Filter spaces by space type (SPACE or GROUP_CHAT or DIRECT_MESSAGE)
        #     filter='space_type = "SPACE"'
        # )

        # Make the request
        # page_result = client.list_spaces(request)

        # Handle the response. Iterating over page_result will yield results and
        # resolve additional pages automatically.
        # for response in page_result:
        #     print(f"{response.name} - {response.display_name}")

        space_name = "spaces/AAA"

        # List all members of the space
        # request = google_chat.ListMembershipsRequest(parent=space_name, page_size=10)
        # memberships = client.list_memberships(request)
        # for membership in memberships:
        #     print(f"{membership.name} - {membership.member.display_name}")
        # return None

        request = google_chat.ListMessagesRequest(
            parent=space_name, 
            page_size=25, 
            order_by="create_time ASC",
            filter="create_time > \"2026-05-05T00:00:00+00:00\" AND create_time < \"2026-05-06T00:00:00+00:00\""
        )
        messages = client.list_messages(request)
        for message in messages:
            print("------------------------------")
            print(message)
    except Exception as error:
        # TODO(developer) - Handle errors from Chat API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
    # creds = auth()
    # people_service = build("people", "v1", credentials=creds)
    # profile = people_service.people().get(resourceName="people/115014927189572540867", personFields="names,emailAddresses").execute() 
    # print(profile)
