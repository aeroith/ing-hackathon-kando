import random

from rekognition_helper import rekognition_helper
import io
import time
import picamera


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human', 'People']
        self.known_faces = {'e7e5b7da-ad8a-4c77-af43-69454c3e0ce9': 'Berkay',
                            'fc8458b5-fffa-4f23-aeb6-980127fdb427': 'Denizcan',
                            'edaa11a6-1937-485b-9065-133ea2a68b8a': 'Sercan',
                            '929c29f9-539c-4b84-aa2e-f7189e1a446e': 'Serhat',
                            'c309eec7-956f-4a3c-9d79-afbf00ab6715': 'Serhat',
                            'e1bdb7d9-9368-4e8d-98c2-fa6ae4a29e9b': 'Serhat',
                            'f460ed5d-ecba-4ca1-967a-1a380862d03f': 'Serhat',
                            '2e50621b-c4cc-4712-9e80-f43f399bd7a0': 'Olcay'}
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

    def see_and_tell(self, byte_array):
        re_helper = rekognition_helper()
        # re_helper.create_one_time_collection()
        # re_helper.search_faces_by_image(byte_array)
        detected_label = re_helper.detect_labels(byte_array)
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
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        vc = visual_cortex()
        while True:
            camera.capture("foo.jpg")
            with open("foo.jpg", "rw") as imageFile:
                f = imageFile.read()
                vc.see_and_tell(f)
