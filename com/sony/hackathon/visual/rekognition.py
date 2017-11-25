from rekognition_helper import rekognition_helper


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human']
        self.readable = ['Brochure', 'Flyer', 'Newspaper']


    def see_and_tell(self, byte_array):
        re_helper = rekognition_helper()

        re_helper.detect_labels(byte_array)
        re_helper.speak(text=re_helper.detect_text(byte_array))


if __name__ == "__main__":
    with open("/Users/trberkad/Downloads/gozluklu_test.jpg", "rb") as imageFile:
        f = imageFile.read()

    vc = visual_cortex()
    vc.see_and_tell(f)
