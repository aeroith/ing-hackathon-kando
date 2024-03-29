import random

from rekognition_helper import rekognition_helper
import io
import time
import picamera


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human', 'People']
        self.known_faces = {'e7e5b7da-ad8a-4c77-af43-69454c3e0ce9': 'Berkay',
                            '1cff55aa-5406-4644-9fdc-aa5132c51495': 'Berkay',
                            '05ae12a2-8b03-42e2-aef1-875161880c66': 'Berkay',
                            '73184efe-9756-4bfb-aafa-62c09baec97c': 'Berkay',
                            'fc8458b5-fffa-4f23-aeb6-980127fdb427': 'Denizcan',
                            '8d62bd15-4626-4222-9a5d-0f79876b696b': 'Denizcan',
                            '6f37734d-f66f-4969-b632-dde8caebbbc8': 'Denizcan',
                            '66a30047-1035-404e-8022-99c618803dbc': 'Denizcan',
                            'edaa11a6-1937-485b-9065-133ea2a68b8a': 'Sercan',
                            '2a9d8067-43c4-4409-a77e-9ee930bd477f': 'Sercan',
                            'c12dc22d-dea2-403c-a595-d221fb3ce874': 'Sercan',
                            '929c29f9-539c-4b84-aa2e-f7189e1a446e': 'Serhat',
                            'c309eec7-956f-4a3c-9d79-afbf00ab6715': 'Serhat',
                            'e1bdb7d9-9368-4e8d-98c2-fa6ae4a29e9b': 'Serhat',
                            'f460ed5d-ecba-4ca1-967a-1a380862d03f': 'Serhat',
                            '2e50621b-c4cc-4712-9e80-f43f399bd7a0': 'Olcay',
                            '79d65fb4-87c2-457a-ba6e-3029b7d25c83': 'Olcay',
                            'c7a794a4-d564-4592-a242-f47080b51dfe': 'Olcay',
                            'fcb1fc2b-7617-444d-a81a-6d5d1505de7d': 'Olcay',
                            'ece6008e-15e4-4298-a6f5-705f062447ca': 'Olcay',
                            '7261819c-0f5c-49e4-9cf2-549907cb5a0f': 'Olcay',
                            '23c7f00a-8483-4280-a0a1-aaffbe5e1e8c': 'Aysegul',
                            '9a6aa2bf-a0f4-48b9-9d54-00c56028bb88': 'Aysegul',
                            'aa51a0ae-6df5-4642-a7ac-762cce6791e2': 'Aysegul',
                            '0fb8374d-b6a7-448f-a5ef-1f8e3a3cdb99': 'Pinar',
                            '9d9c2cec-81a6-4f73-bd8d-306f0a5412ed': 'Pinar',
                            'acb3f948-4e56-4a03-9ae0-a08dddefe213': 'Pinar',
                            '26673d23-6668-41e7-b2ae-b0e6691b3b02': 'Pinar'}
        self.sentence_prefixes_object = [
            'I see {}.',
            'I think I see {}.',
            'There is {} in front of you.'
        ]

    def __tell_known_names(self, matched_face_ids):
        matched_names = []
        re_helper = rekognition_helper()
        for matched_face_id in matched_face_ids:
            matched_names.append(self.known_faces[matched_face_id])
        matched_names_unique = list(set(matched_names))
        print 'I know these people!'
        print matched_names_unique
        if len(matched_names_unique) > 1:
            matched_names, last = ", ".join(matched_names_unique[:-1]), matched_names_unique[-1]
            re_helper.speak(" ve ".join([matched_names, last]), voice='Filiz')
        elif len(matched_names_unique) == 1:
            re_helper.speak(matched_names_unique[0], voice='Filiz')

    def see_and_tell(self, byte_array, image_path):
        re_helper = rekognition_helper()
        # re_helper.create_one_time_collection()
        # re_helper.search_faces_by_image(byte_array)
        detected_label = re_helper.detect_labels_offline(image_path)
        print 'Detected label: ' + detected_label
        re_helper.speak(random.choice(self.sentence_prefixes_object).format(detected_label))
        if detected_label in self.human_like:
            matched_face_ids = re_helper.search_faces_by_image(byte_array)
            self.__tell_known_names(matched_face_ids)
        else:
            detected_text = re_helper.detect_text(byte_array)
            print 'I detected text!' + detected_text
            re_helper.speak(detected_text)


if __name__ == "__main__":
    my_stream = io.BytesIO()
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.hflip = True
        camera.vflip = True
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        vc = visual_cortex()
        while True:
            camera.capture("foo.jpg")
            with open("foo.jpg", "rw") as imageFile:
                f = imageFile.read()
                vc.see_and_tell(f, "foo.jpg")
