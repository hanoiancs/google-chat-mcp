def normalize_person(membership):
    return {
        "id": membership.name.split("/")[-1],
        "name": membership.name,
        "member_name": membership.member.name,
        "member_type": membership.member.type_,
        "role": membership.role,
        "state": membership.state,
    }
