import boto3
import os


class rekognition_helper(object):
    def __init__(self):
        self.access_key = 'AKIAIQXIEYVTPUL5YNNA'
        self.secret_key = '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'
        self.photo_bucket = "ing-hackathon-photo-bucket"
        self.region = "eu-west-1"

        self.detect_text_threshold = 70
        self.detect_label_threshold = 50

        self.rekognition_client = boto3.client('rekognition', aws_access_key_id=self.access_key,
                                               aws_secret_access_key=self.secret_key, region_name=self.region)
        self.s3_client = boto3.client('s3', region_name=self.region, aws_access_key_id=self.access_key,
                                      aws_secret_access_key=self.secret_key)

        self.polly_client = boto3.client('polly', aws_access_key_id=self.access_key,
                                         aws_secret_access_key=self.secret_key, region_name=self.region)

    def detect_faces(self, bucket, key, region="eu-west-1"):
        rekognition = boto3.client("rekognition", region)
        response = rekognition.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": key,
                }
            },
            Attributes=['ALL'],
        )
        return response['FaceDetails']

    def create_collection(self):
        response = self.rekognition_client.create_collection(
            CollectionId='test-collection'
        )
        print response

    def detect_labels(self, byte_array):
        response = self.rekognition_client.detect_labels(
            Image={
                'Bytes': byte_array
            },
            MaxLabels=2,
            MinConfidence=self.detect_label_threshold
        )
        print response

    def detect_text(self, byte_array):
        response = self.rekognition_client.detect_text(
            Image={
                'Bytes': byte_array
            }
        )
        detected_text_list = list()
        if response:
            for detection in response['TextDetections']:
                detected_text = detection['DetectedText']
                confidence_level = float(detection['Confidence'])
                string_type = detection['Type']
                if confidence_level > self.detect_text_threshold and string_type == 'LINE':
                    detected_text_list.append(detected_text)
        return ' '.join(detected_text_list)

    def index_faces(self):
        response = self.rekognition_client.index_faces(
            CollectionId='test-collection',
            Image={
                'S3Object': {
                    'Bucket': self.photo_bucket,
                    'Name': 'test.jpg'}
            },
            ExternalImageId='string',
            DetectionAttributes=[
                'DEFAULT',
            ]
        )
        print response

    def search_faces_by_image(self):
        with open("/Users/trberkad/Downloads/gozluklu_test.jpg", "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)

        response = self.rekognition_client.search_faces_by_image(
            CollectionId='test-collection',
            Image={
                'Bytes': b
            }
        )
        print response

    def search_faces_by_image_s3(self):
        with open("/Users/trberkad/Downloads/gozluklu_test.jpg", "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)

        response = self.rekognition_client.search_faces_by_image(
            CollectionId='test-collection',
            Image={
                'S3Object': {
                    'Bucket': self.photo_bucket,
                    'Name': 'gozluklu_test.jpg'}
            }
        )
        print response

    def speak(self, text, format='mp3', voice='Brian'):
        resp = self.polly_client.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)
        soundfile = open('/tmp/sound.mp3', 'w')
        soundBytes = resp['AudioStream'].read()
        soundfile.write(soundBytes)
        soundfile.close()
        os.system('afplay /tmp/sound.mp3')  # Works only on Mac OS, sorry
        os.remove('/tmp/sound.mp3')
