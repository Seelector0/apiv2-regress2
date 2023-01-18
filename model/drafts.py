

class Draft:

    def __init__(self, draft_id=None):
        self.draft_id = draft_id

    def __repr__(self):
        return f"{self.draft_id}"

    def __eq__(self, other):
        return self.draft_id or other.draft_id is None or self.draft_id == other.draft_id
