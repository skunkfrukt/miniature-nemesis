import logging
log = logging.getLogger(__name__)

class Encounter():
    def __init__(self, members=[], origin="LEFT", leader=None, behavior=None):
        self.members = members
        self.origin = origin
        self.leader = leader
        self.common_behavior = behavior

    def add_member(self, placeholder):
        if self.common_behavior is not None:
            pass  ##TODO## Add common behavior or something.
        self.members.append(placeholder)
