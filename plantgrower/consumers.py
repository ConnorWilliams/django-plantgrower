# For use with channels which is being used for realtime data

from channels import Group


def ws_connect(message):
    print("Someone connected.")
    path = message['path']  # i.e. /sensor/

    if path == '/plantgrower/':
        print("Adding new user to sensor group")
        # Add user to group for broadcast
        Group('sensor').add(message.reply_channel)
        message.reply_channel.send({  # Reply to individual directly
           "text": "You're connected to sensor group :) ",
        })
    else:
        print("Strange connector!")


def ws_disconnect(message):
    print("Someone left us...")
    Group('sensor').discard(message.reply_channel)
