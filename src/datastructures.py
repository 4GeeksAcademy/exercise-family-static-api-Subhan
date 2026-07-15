"""
This file contains the FamilyStructure class and its methods.
"""


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": last_name,
                "age": 5,
                "lucky_numbers": [1]
            }
        ]

    # Generates a unique ID whenever a member is added
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        new_member = {
            "id": self._generate_id(),
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }

        self._members.append(new_member)
        return new_member

    def delete_member(self, id):
        member = self.get_member(id)

        if member is None:
            return False

        self._members.remove(member)
        return True

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member

        return None

    def get_all_members(self):
        return self._members