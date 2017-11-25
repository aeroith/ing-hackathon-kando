import boto3

def index_face(s3_path):
    response = rekognition_client.index_faces(
        CollectionId=face_collection_name,
        Image={
            'S3Object': {
                'Bucket': photo_bucket,
                'Name': s3_path}
        },
        DetectionAttributes=[
            'DEFAULT',
        ]
    )
    print response

access_key = 'AKIAIQXIEYVTPUL5YNNA'
secret_key = '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'
photo_bucket = "ing-hackathon-photo-bucket"
region = "eu-west-1"
face_collection_name = 'kando-team-collection'
rekognition_client = boto3.client('rekognition', aws_access_key_id=access_key,
                                  aws_secret_access_key=secret_key, region_name=region)

faces_to_index = ['berkay1.jpeg',
'berkay2.jpeg',
'berkay3.jpeg',
'denizcan1.jpeg',
'denizcan2.jpeg',
'denizcan3.jpeg',
'olcay1.jpeg',
'olcay2.jpeg',
'olcay3.jpeg',
'olcay4.jpeg',
'olcay5.jpeg',
'sercan1.jpeg',
'sercan2.jpeg']

for face in faces_to_index:
    index_face(face)


