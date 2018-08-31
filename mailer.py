# Inside modules
import threading
# Outside modules
import boto3


class Mailer(object):
	"""docstring for Mailer"""
	def __init__(self, **kwargs):
		"""
		from_, to, subject, body
		"""
		self.options = kwargs
		self.client = boto3.client("ses")

	# user+recipient1@example.com
	def send(self, **kwargs):
		def run():
			kwargs.update(self.options)
			response = self.client.send_email(
				Source=kwargs["from_"],
				Destination={
					"ToAddresses": [kwargs["from_"]],
					"BccAddresses": kwargs["to"]
				},
				Message={
					"Subject": { "Data": kwargs["subject"] },
					"Body": { "Text": { "Data": kwargs["body"] } }
				}
			)
		thread = threading.Thread(target=run)
		thread.start()
