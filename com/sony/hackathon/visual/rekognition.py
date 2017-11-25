from rekognition_helper import rekognition_helper


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human']
        self.readable = ['Brochure', 'Flyer', 'Newspaper']
        self.known_faces = {'Berkay': 'e7e5b7da-ad8a-4c77-af43-69454c3e0ce9',
                            'Denizcan': 'fc8458b5-fffa-4f23-aeb6-980127fdb427',
                            'Sercan': 'edaa11a6-1937-485b-9065-133ea2a68b8a',
                            'Serhat': '929c29f9-539c-4b84-aa2e-f7189e1a446e',
                            'Olcay': '2e50621b-c4cc-4712-9e80-f43f399bd7a0'}

    def see_and_tell(self, byte_array):
        re_helper = rekognition_helper()
        re_helper.search_faces_by_image(byte_array)
        #re_helper.speak(text=re_helper.detect_labels(byte_array))
        #re_helper.speak(text=re_helper.detect_text(byte_array))


if __name__ == "__main__":
    with open("/Users/trberkad/Downloads/olcay.jpg", "rb") as imageFile:
        f = imageFile.read()

    vc = visual_cortex()
    vc.see_and_tell(f)
