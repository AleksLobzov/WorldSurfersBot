# bot logic implementation

import bot_handler
import user
import config
import collections


ws_bot = bot_handler.BotHandler(config.token)

user_dict = {}


def main():

    new_offset = None

    while True:

        try:

            messages = ws_bot.get_updates(config.timeout, new_offset)

            last_update = ws_bot.last_update()

            last_update_id = last_update['update_id']

            # create unique user dictionary with their last messages
            message_dict = {}
            for item in messages:
                try:
                    message_dict[item['message']['from']['id']] = item
                except KeyError:
                    message_dict[item['edited_message']['from']['id']] = item

            for from_id, message in message_dict.items():

                # get last message
                chat_id = message['message']['chat']['id']
                text = message['message']['text']

                # get last user and remember her
                if from_id not in user_dict:
                    user_dict[from_id] = user.User(from_id)

                # get response text
                response_text = ''
                state = user_dict[from_id].state
                if state == 0:
                    if text == '/reset':
                        user_dict.clear()
                        del config.table_topics_participants[:]
                    elif text == '/addttspkr':
                        user_dict[from_id].state = 4
                        response_text = 'You are going to add TT speaker.\n' \
                                        'Enter his name:'
                    elif text == '/delttspkr':
                        user_dict[from_id].state = 5
                        response_text = 'You are going to delete TT speaker.\n' \
                                        'Choose one by entering her name.\n'
                        response_text += ',\n'.join(str(item) for item in config.table_topics_participants)
                    elif text == '/survey1':
                        user_dict[from_id].state = 1
                        response_text = 'You are going to evaluate a speaker.\n' \
                                        '/continue'
                    elif text == '/survey2':
                        user_dict[from_id].state = 2
                        user_dict[from_id].table_topics_ballot = ''
                        response_text = 'You are going to vote for TT winner.\n' \
                                        'Choose one by entering her name.\n'
                        response_text += ',\n'.join(str(item) for item in config.table_topics_participants)
                    elif text == '/survey3':
                        user_dict[from_id].state = 3
                        for item in config.meeting_evaluation_params:
                            user_dict[from_id].meeting_feedback_form[item] = '0'
                        user_dict[from_id].meeting_feedback_form = collections.OrderedDict(sorted(user_dict[from_id].meeting_feedback_form.items()))
                        response_text = 'You are going to evaluate the meeting.\n' \
                                        'For every parameter choose one of the following grades:\n'
                        response_text += ',\n'.join(str(item) for item in sorted(config.meeting_evaluation_grades, reverse = True))
                        response_text += '\n/continue'
                    elif text == '/result1':
                        response_text = 'Speaker evaluation is not available.\n' \
                                        '/continue'
                    elif text == '/result2':
                        response_text = get_table_topics_result()
                    elif text == '/result3':
                        response_text = get_meeting_evaluation_result()
                    else:
                        response_text = 'Enter /survey1 for speaker evaluation.\n' \
                                        'Enter /survey2 for TT winner voting.\n' \
                                        'Enter /survey3 for meeting evaluation.'
                elif state == 1:
                    user_dict[from_id].state = 0
                    response_text = 'Speaker evaluation is not available.\n' \
                                    '/continue'
                elif state == 2:
                    response_text = fill_table_topics_ballot(user_dict[from_id], text)
                elif state == 3:
                    response_text = fill_meeting_feedback_form(user_dict[from_id], text)
                elif state == 4:
                    response_text = add_table_topics_speaker(user_dict[from_id], text)
                else:
                    response_text = remove_table_topics_speaker(user_dict[from_id], text)

                # send last message
                ws_bot.send_message(chat_id, response_text)

            new_offset = last_update_id + 1

        except IndexError:
            print('There is not new messages in getUpdates()')


# filling table topics ballot
def fill_table_topics_ballot(voter, text):
    if len(config.table_topics_participants) > 0:
        if text in config.table_topics_participants:
            try:
                voter.table_topics_ballot = text
                voter.state = 0
                return 'Congratulations! You voted successfully.\n' \
                       '/continue'
            except TypeError:
                raise AssertionError('Input variable should be User')
        else:
            return 'You have entered the wrong name. Type the correct one'
    else:
        voter.state = 0
        return 'TT participants are not defined\n' \
               '/continue'


# filling meeting feedback form
def fill_meeting_feedback_form(respondent, text):
    if text == '/continue':
        try:
            evaluated_parameter = list(respondent.meeting_feedback_form.keys())[list(respondent.meeting_feedback_form.values()).index('0')]
            return evaluated_parameter + '\n/2 /3 /4 /5'
        except ValueError:
            respondent.state = 0
            return 'Meeting evaluation is over. Thank you!\n' \
                   '/continue'
        except TypeError:
            raise AssertionError('Input variable should be User')
    elif text in ('2', '3', '4', '5', '/2', '/3', '/4', '/5'):
        try:
            evaluated_parameter = list(respondent.meeting_feedback_form.keys())[list(respondent.meeting_feedback_form.values()).index('0')]
            if text[0] == '/':
                text = text[1:]
            respondent.meeting_feedback_form[evaluated_parameter] = text
            evaluated_parameter = list(respondent.meeting_feedback_form.keys())[list(respondent.meeting_feedback_form.values()).index('0')]
            return evaluated_parameter + '\n/2 /3 /4 /5'
        except ValueError:
            respondent.state = 0
            return 'Meeting evaluation is over. Thank you!\n' \
                   '/continue'
        except TypeError:
            raise AssertionError('Input variable should be User')
    else:
        return 'You should complete meeting evaluation. Please, enter /continue'


# add table topics speaker
def add_table_topics_speaker(administrator, text):
    administrator.state = 0
    is_added = False
    for item in config.table_topics_participants:
        if text == item:
            is_added = True
    result = ''
    if is_added:
        result = 'Speaker ' + text + ' is already in the TT participants list\n' \
                 '/continue'
    else:
        config.table_topics_participants.append(text)
        result = 'Speaker ' + text + ' is added\n' \
                 '/continue'
    return result


# remove table topics speaker
def remove_table_topics_speaker(administrator, text):
    administrator.state = 0
    is_added = False
    for item in config.table_topics_participants:
        if text == item:
            is_added = True
    result = ''
    if is_added:
        try:
            config.table_topics_participants.remove(text)
            result = 'Speaker ' + text + ' is deleted\n' \
                     '/continue'
        except ValueError:
            result = 'Speaker ' + text + ' is already deleted by someone else\n' \
                     '/continue'
    else:
        result = 'Speaker ' + text + ' is not in the TT participants list\n' \
                 '/continue'
    return result


# get table topics result
def get_table_topics_result():
    result = {}
    for participant in config.table_topics_participants:
        result[participant] = 0
        for value in user_dict.values():
            if value.table_topics_ballot == participant:
                result[participant] += 1
    print(result)
    result = ',\n'.join(str(key) + ': ' + str(value) for key, value in result.items())
    if result is None:
        result = 'Nobody voted for a TT winner'
    result += '\n/continue'
    return result


# get meeting evaluation result
def get_meeting_evaluation_result():
    result = {}
    participants = {}
    for participant in user_dict.values():
        if participant.check_meeting_feedback_completed():
            participants[participant.id] = participant
    length = len(participants)
    if length > 0:
        try:
            for param in config.meeting_evaluation_params:
                grades = []
                for participant in participants.values():
                    grades.append(int(participant.meeting_feedback_form[param]))
                result[param] = sum(grades) / length
            result = collections.OrderedDict(sorted(result.items()))
            print(result)
            result = ',\n'.join(str(key) + ': ' + str(value) for key, value in result.items())
            result += '\n/continue'
            return result
        except KeyError:
            return 'There is not filled meeting evaluation forms found\n' \
                   '/continue'
    else:
        return 'Nobody provided meeting feedback\n' \
               '/continue'


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
