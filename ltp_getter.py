# coding: utf-8

# Inside modules
import threading
from datetime import datetime, timedelta
# Outside modules
import numpy as np
# Other modules
from bitflyer_pubnub import BitflyerPubnub


class LtpGetter(threading.Thread):
	"""docstring for Getter
	:param timerange: この時間範囲内での最大値・最小値を取得する．
	"""
	def __init__(self, **timerange):
		super().__init__()
		self.timerange = timerange
		self.channel = "lightning_ticker_FX_BTC_JPY"
		self.key = "ltp"
		with BitflyerPubnub(self.channel) as btp:
			self.queue = np.array([btp.listen(self.key)])
			self.time = np.array([datetime.now()])

	def run(self):
		with BitflyerPubnub(self.channel) as btp:
			while True:
				self.queue = np.append(self.queue, btp.listen(self.key))
				self.time = np.append(self.time, datetime.now())
				timeout = np.where(self.time < datetime.now() - timedelta(**self.timerange))
				self.queue = np.delete(self.queue, timeout)
				self.time = np.delete(self.time, timeout)

	def get_max(self):
		return int(max(self.queue))
	def get_min(self):
		return int(min(self.queue))

	def get_oldest(self):
		return self.queue[0]
