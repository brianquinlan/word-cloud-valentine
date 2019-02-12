#!/usr/bin/env python3

"""Extract the GAIA ids found in a Hangouts.json file.

You can get this type of file using Google Takeout.

Useful in providing the --gaia_ids argument to extract_hangouts_messages.py.

e.g.

$ ./extract_gaia_ids.py <Hangouts.json
Jane Doe                                 291251231251231231231
John Smiley                              235982369582309481312
John Smith                               123123124123123123123
...

"""

import json
import sys


def extract_participants(conversations):
    for conversation in conversations:
        conversation_data = conversation['conversation']['conversation']
        for participant in conversation_data['participant_data']:
            yield participant


def main():
    hangouts_data = json.load(sys.stdin)
    conversations = hangouts_data['conversations']
    name_and_gaia_id = set()
    for participant in extract_participants(conversations):
        name = participant.get('fallback_name', 'Unknown')
        if 'id' in participant and 'gaia_id' in participant['id']:
            name_and_gaia_id.add((name, participant['id']['gaia_id']))

    for name, gaia_id in sorted(name_and_gaia_id):
        print(name.ljust(40), gaia_id)

if __name__ == '__main__':
    main()
