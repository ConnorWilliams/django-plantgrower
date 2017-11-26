# For use with channels which is being used for realtime data
from channels import Group


def ws_connect(message):
    print("Adding new user to stage group.")
    Group('stage').add(message.reply_channel)


def ws_disconnect(message):
    print("Someone left.")
    Group('stage').discard(message.reply_channel)
