class User:

    # user initialization method
    def __init__(self, id):

        # message.from_id
        self.id = id

        # 0 - do nothing;
        # 1 - do speaker evaluation;
        # 2 - choose TT winner;
        # 3 - do meeting evaluation;
        # 4 - add TT speaker;
        # 5 - remove TT speaker
        # 6 - set language
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
        is_completed = False
        length = len(self.meeting_feedback_form)
        if length > 0:
            try:
                a = [list(self.meeting_feedback_form.values()).index('0')]
                return is_completed
            except ValueError:
                is_completed = True
                return is_completed
        else:
            return is_completed
