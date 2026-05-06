from datetime import datetime

from google.apps.chat_v1.types import Membership

from models import MemberModel, MemberModel, MessageModel, MessageQuoteModel, MessageThreadModel, SenderModel


def normalize_person(membership: Membership) -> MemberModel:
    return MemberModel(
        id=membership.name.split("/")[-1],
        name=membership.name,
        member_name=membership.member.name,
        type=membership.member.type_.name,
        role=membership.role.name,
        state=membership.state.name,
    )


def normalize_message(message) -> MessageModel:
    return MessageModel(
        name=message.name,
        text=message.text,
        create_time=datetime.fromtimestamp(message.create_time.timestamp()),
        sender=(
            SenderModel(
                id=message.sender.name.split("/")[-1],
                name=message.sender.name,
                display_name=message.sender.display_name,
            )
            if message.sender
            else None
        ),
        thread=(
            MessageThreadModel(name=message.thread.name) if message.thread else None
        ),
        quote=(
            MessageQuoteModel(
                name=message.quoted_message_metadata.name,
                text=message.quoted_message_metadata.quoted_message_snapshot.text,
                create_time=datetime.fromtimestamp(
                    message.quoted_message_metadata.last_update_time.timestamp()
                ),
                type=message.quoted_message_metadata.quote_type.name,
            )
            if message.quoted_message_metadata
            else None
        ),
    )
