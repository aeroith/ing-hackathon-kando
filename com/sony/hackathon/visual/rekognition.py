from rekognition_helper import rekognition_helper


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human', 'People']
        self.readable = ['Brochure', 'Flyer', 'Newspaper']

        self.known_faces = {'e7e5b7da-ad8a-4c77-af43-69454c3e0ce9': 'Berkay',
                            'fc8458b5-fffa-4f23-aeb6-980127fdb427': 'Denizcan',
                            'edaa11a6-1937-485b-9065-133ea2a68b8a': 'Sercan',
                            '929c29f9-539c-4b84-aa2e-f7189e1a446e': 'Serhat',
                            'c309eec7-956f-4a3c-9d79-afbf00ab6715': 'Serhat',
                            'e1bdb7d9-9368-4e8d-98c2-fa6ae4a29e9b': 'Serhat',
                            'f460ed5d-ecba-4ca1-967a-1a380862d03f': 'Serhat',
                            '2e50621b-c4cc-4712-9e80-f43f399bd7a0': 'Olcay'}

    def see_and_tell(self, byte_array):
        re_helper = rekognition_helper()
        #re_helper.create_one_time_collection()
        re_helper.search_faces_by_image(byte_array)
        detected_label = re_helper.detect_labels(byte_array)
        re_helper.speak(detected_label)
        if detected_label in self.human_like:
            matched_face_id = re_helper.search_faces_by_image(byte_array)
            matched_name = self.known_faces[matched_face_id]
            re_helper.speak(matched_name, voice='Filiz')

        re_helper.speak(text=re_helper.detect_text(byte_array))


if __name__ == "__main__":
    with open("/Users/trberkad/Downloads/serhat_test1.jpeg", "rb") as imageFile:
        f = imageFile.read()

    vc = visual_cortex()
    vc.see_and_tell(f)
