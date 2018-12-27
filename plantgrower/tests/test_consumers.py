# https://channels.readthedocs.io/en/latest/testing.html

# from channels import Channel
# from channels import Group
# from channels.test import ChannelTestCase

# # Example testing a consumer thats supposed to take a value and post the
# # square of it to the result channel
# class MyTests(ChannelTestCase):
#     def test_a_thing(self):
#         # Inject a message onto the channel to use in a consumer
#         Channel("input").send({"value": 33})
#         # Run the consumer with the new Message object
#         my_consumer(self.get_next_message("input", require=True))
#         # Verify there's a result and that it's accurate
#         result = self.get_next_message("result", require=True)
#         self.assertEqual(result['value'], 1089)

# # Example adding channel to a group, sending a message to group,
# # and verifying the message was received.
# class MyTests(ChannelTestCase):
#     def test_a_thing(self):
#         # Add a test channel to a test group
#         Group("test-group").add("test-channel")
#         # Send to the group
#         Group("test-group").send({"value": 42})
#         # Verify the message got into the destination channel
#         result = self.get_next_message("test-channel", require=True)
#         self.assertEqual(result['value'], 42)
