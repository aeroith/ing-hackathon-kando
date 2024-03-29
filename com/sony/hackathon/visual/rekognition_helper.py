import boto3
import os
from pygame import mixer  # Load the required library
from botocore.exceptions import ClientError
import keras
import numpy as np
import tensorflow as tf
from keras.applications.inception_v3 import preprocess_input, decode_predictions
from keras.preprocessing import image


class rekognition_helper(object):
    def __init__(self):
        self.access_key = 'AKIAIQXIEYVTPUL5YNNA'
        self.secret_key = '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'
        self.photo_bucket = "ing-hackathon-photo-bucket"
        self.region = "eu-west-1"

        self.detect_text_threshold = 70
        self.detect_label_threshold = 50
        self.face_collection_name = 'kando-team-collection'

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

    def detect_labels(self, byte_array):
        response = self.rekognition_client.detect_labels(
            Image={
                'Bytes': byte_array
            },
            MaxLabels=1,
            MinConfidence=self.detect_label_threshold
        )
        label = ""
        if response and len(response['Labels']) == 1:
            label = response['Labels'][0]['Name']
        return label

    def detect_labels_offline(self, image_path):
        global graph
        model = keras.applications.inception_v3.InceptionV3(include_top=True, weights='imagenet', input_tensor=None,
                                                            input_shape=None, pooling=None, classes=1000)
        graph = tf.get_default_graph()
        with graph.as_default():
            img = image.load_img(image_path, target_size=(299, 299))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = model.predict(x)

            top3 = decode_predictions(preds, top=3)[0]

            predictions = [{'label': label, 'description': description, 'probability': probability * 100.0}
                           for label, description, probability in top3]

            return predictions[0]['label']

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

    def index_faces(self, s3_path):
        response = self.rekognition_client.index_faces(
            CollectionId=self.face_collection_name,
            Image={
                'S3Object': {
                    'Bucket': self.photo_bucket,
                    'Name': s3_path}
            },
            DetectionAttributes=[
                'DEFAULT',
            ]
        )
        print response

    def search_faces_by_image(self, byte_array):
        face_ids = []
        try:
            response = self.rekognition_client.search_faces_by_image(
                CollectionId=self.face_collection_name,
                Image={
                    'Bytes': byte_array
                }
            )
            face_matches = response['FaceMatches']
            if len(face_matches) != 0:
                for face in face_matches:
                    face_ids.append(face['Face']['FaceId'])
        except:
            pass
        return face_ids

    def search_faces_by_image_s3(self):
        with open("/Users/trberkad/Downloads/gozluklu_test.jpg", "rb") as imageFile:
            f = imageFile.read()
            b = bytearray(f)

        response = self.rekognition_client.search_faces_by_image(
            CollectionId=self.face_collection_name,
            Image={
                'S3Object': {
                    'Bucket': self.photo_bucket,
                    'Name': 'gozluklu_test.jpg'}
            }
        )
        print response

    def list_faces(self):
        response = self.rekognition_client.list_faces(
            CollectionId=self.face_collection_name
        )
        print response

    def create_one_time_collection(self):
        try:
            create_collection_response = self.rekognition_client.create_collection(
                CollectionId=self.face_collection_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
                pass

        faces = ['serhat1.jpeg', 'serhat2.jpeg', 'serhat3.jpeg']
        for face in faces:
            self.index_faces(face)

    def delete_collection(self):
        response = self.rekognition_client.delete_collection(
            CollectionId=self.face_collection_name
        )
        return response

    def speak(self, text, format='mp3', voice='Salli'):
        resp = self.polly_client.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)
        soundfile = open('/tmp/sound.mp3', 'w')
        soundBytes = resp['AudioStream'].read()
        soundfile.write(soundBytes)
        soundfile.close()
        mixer.init()
        mixer.music.load('/tmp/sound.mp3')
        mixer.music.play()
        os.remove('/tmp/sound.mp3')
