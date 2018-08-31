# Outside modules
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener


class BitflyerPubnub(object):
	"""docstring for BitflyerPubnub"""
	def __init__(self, channel):
		pnconfig = PNConfiguration()
		pnconfig.subscribe_key = "sub-c-52a9ab50-291b-11e5-baaa-0619f8945a4f"
		self.pubnub = PubNub(pnconfig)
		self.listener = SubscribeListener()
		self.channel = channel

	def __enter__(self):
		self.pubnub.add_listener(self.listener)
		self.pubnub.subscribe().channels([self.channel]).execute()
		self.listener.wait_for_connect()
		return self

	def listen(self, key):
		return self.listener.wait_for_message_on(self.channel).message[key]

	def __exit__(self, type, value, traceback):
		self.pubnub.unsubscribe().channels([self.channel]).execute()
		self.listener.wait_for_disconnect()
