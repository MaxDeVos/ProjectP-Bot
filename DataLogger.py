import discord
import re
import csv
import time
import datetime


csv_path = "stats/vc_log.csv"


def get_name_from_channel_data(data):
    data = str(data)

    parsed_data = re.search("(?<= channel=).*(?=>)", data)
    parsed_data.group(0)

    if parsed_data[0] == 'None':
        return None

    channel = re.search("(?<= name\=').*(?=\' )", parsed_data[0])
    return channel[0]


def handle_voice_state_change(user, old, new):

    user = str(user)
    old_channel = get_name_from_channel_data(old)
    new_channel = get_name_from_channel_data(new)

    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)

        if old_channel is None:
            # print(user, "Initially joining", new_channel)
            writer.writerow([user, "join", new_channel, str(time.time()), datetime.datetime.now().isoformat()])
        elif new_channel is None:
            # print(user, "Disconnect from", old_channel)
            writer.writerow(
                [user, "leave", old_channel, str(time.time()), datetime.datetime.now().isoformat()])
        elif new_channel != old_channel:
            # print(user, "Transfer from", old_channel, "to", new_channel)
            writer.writerow(
                [user, "leave", old_channel, str(time.time()), datetime.datetime.now().isoformat()])
            writer.writerow([user, "join", new_channel, str(time.time()), datetime.datetime.now().isoformat()])
