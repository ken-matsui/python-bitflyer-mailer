# coding: utf-8

# Inside modules
import os
import signal
import operator
from datetime import datetime, timedelta
# Outside modules
import boto3
# Other modules
from mailer import Mailer
from ltp_getter import LtpGetter
import progressbar


def scan_dynamo(table, key):
	dynamodb = boto3.resource('dynamodb')
	table = dynamodb.Table(table)
	keys = table.scan(key)
	return [item[key] for item in keys['Items']]

def judge(op, now, before, sendtime):
	return op(now, before) & (sendtime < datetime.now() - timedelta(minutes=15))

def logging(opname, before, now, sendtime):
	sendtime = datetime.now()
	print("Sent a mail as {opname}({before} => {now}) on {sendtime}".format(**locals()))
	return sendtime, now

def bitflyer_mailer(from_, subject, ltpgetter):
	mailer = Mailer(from_=from_, subject=subject)
	max_before, min_before = ltpgetter.get_max(), ltpgetter.get_min()
	max_sendtime = min_sendtime = datetime.now() - timedelta(minutes=15)
	while True:
		try:
			max_now, min_now = ltpgetter.get_max(), ltpgetter.get_min()
			if judge(operator.gt, max_now, max_before, max_sendtime):
				to = scan_dynamo('contacts', 'address')
				mailer.send(to=to, body="ここ１時間の最大値が更新され，{}円になりました".format(max_now))
				max_sendtime, max_before = logging("MAX", max_before, max_now, max_sendtime)
			if judge(operator.lt, min_now, min_before, min_sendtime):
				to = scan_dynamo('contacts', 'address')
				mailer.send(to=to, body="ここ１時間の最小値が更新され，{}円になりました".format(min_now))
				min_sendtime, min_before = logging("MIN", min_before, min_now, min_sendtime)
			if max_sendtime < datetime.now() - timedelta(hours=1):
				max_before = ltpgetter.get_oldest()
			if min_sendtime < datetime.now() - timedelta(hours=1):
				min_before = ltpgetter.get_oldest()
		except KeyboardInterrupt:
			break
		except Exception as e:
			raise e

def main():
	timerange = {"hours": 1}
	mail_interval = {"minutes": 15}

	ltpgetter = LtpGetter(**timerange)
	ltpgetter.start()
	progressbar.waiting(**timerange)

	print()
	print("Start mailer...")

	from_ = "signal_notification@hoge.com"
	subject = "btc-fx/jpyシグナル"
	bitflyer_mailer(from_, subject, ltpgetter)

	print("End mailer.")
	os.kill(os.getpid(), signal.SIGKILL)

if __name__ == '__main__':
	main()
