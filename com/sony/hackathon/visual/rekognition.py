from rekognition_helper import rekognition_helper
import io
import time
import picamera


class visual_cortex(object):
    def __init__(self):
        self.human_like = ['Person', 'Human']
        self.readable = ['Brochure', 'Flyer', 'Newspaper']


    def see_and_tell(self, byte_array):
        re_helper = rekognition_helper()

        re_helper.detect_labels(byte_array)
        re_helper.speak(text=re_helper.detect_text(byte_array))

if __name__ == "__main__":
    my_stream = io.BytesIO()
    with picamera.PiCamera() as camera:
	camera.resolution = (1024, 768)
        camera.start_preview()
    	# Camera warm-up time
    	time.sleep(2)
    	camera.capture("foo.jpg")
	with open("foo.jpg", "rb") as imageFile:
            f = imageFile.read()
	    vc = visual_cortex()
    	    vc.see_and_tell(f)

   
