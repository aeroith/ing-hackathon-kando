import boto3


class rekognition_helper(object):
    def __init__(self):
        self.access_key = 'AKIAIKWK6O7TSDSI7DCA'
        self.secret_key = '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'
        self.rekognition_client = boto3.client('rekognition', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
        self.s3_client = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)
