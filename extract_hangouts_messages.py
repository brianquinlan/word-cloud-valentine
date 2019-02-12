#!/usr/bin/env python3

"""
Extract the text message content from a Google Hangouts JSON file.

You can get this type of file using Google Takeout.

e.g.

$ ./extract_hangouts_messages <Hangouts.json
This is the first message in the file.
This is the second message in the file.
This message
spans several
lines.
...
"""

import argparse
import json
import sys


def filter_conversations(conversations, interesting_gaia_ids):
    for conversation in conversations:
        conversation_data = conversation['conversation']['conversation']
        for participant in conversation_data['participant_data']:
            if (not interesting_gaia_ids or
                    participant['id']['gaia_id'] in interesting_gaia_ids):
                yield conversation
                break


def extract_message_text(conversations):
    for conversation in conversations:
        if 'events' in conversation:
            for event in conversation['events']:
                if 'chat_message' in event:
                    chat_message = event['chat_message']
                    if 'message_content' in chat_message:
                        message_content = chat_message['message_content']
                        if 'segment' in message_content:
                            for segment in message_content['segment']:
                                if 'text' in segment:
                                    yield segment['text']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--gaia-id",
        dest='gaia_id',
        default=frozenset(),
        nargs="*",
        help="Restrict the extracted conversations to only ones involving "
             "the people with the given GAIA ids. If blank then include all "
             "conversations.")
    args = parser.parse_args()

    hangouts_data = json.load(sys.stdin)
    conversations = hangouts_data['conversations']
    for message in extract_message_text(
            filter_conversations(conversations, args.gaia_id)):
        print(message)


if __name__ == '__main__':
    main()
