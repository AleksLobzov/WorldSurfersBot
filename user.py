class User:

    # user initialization method
    def __init__(self, id):

        # message.from_id
        self.id = id

        # 0 - do nothing;
        # 1 - do speaker evaluation;
        # 2 - choose TT winner;
        # 3 - do meeting evaluation
        self.state = 0

        # dictionary of dictionaries.
        # first level pair: speaker id - feedback form.
        # second level: evaluation criteria - rank
        self.speaker_feedback_forms = {}

        # name of TT winner
        self.table_topics_ballot = ''

        # dictionary: evaluation criteria - rank
        self.meeting_feedback_form = {}

    # check if meeting feedback is completed
    def check_meeting_feedback_completed(self):
        is_completed = True
        for value in self.meeting_feedback_form.values():
            if value is '0':
                is_completed = False
        return is_completed
