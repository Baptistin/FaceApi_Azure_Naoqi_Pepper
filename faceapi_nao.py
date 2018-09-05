# vim: set fileencoding=utf-8 :
import sys
import numpy as np
import cv2
from naoqi import ALProxy

faceapi_headers = {
	'Content-type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '<key>',
}

faceapi_params = urllib.urlencode({
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,glasses',
})

conn = httplib.HTTPSConnection('westeurope.api.cognitive.microsoft.com')

if(len(sys.argv) <= 2):
    print "err"
    sys.exit()

ip_addr = sys.argv[1]
port_num = int(sys.argv[2])


videoDevice = ALProxy('ALVideoDevice', ip_addr, port_num)
tts = ALProxy("ALTextToSpeech", IP, PORT)

AL_kTopCamera = 0
AL_kQVGA = 1            # 320x240
AL_kBGRColorSpace = 13
captureDevice = videoDevice.subscribeCamera(
    "test", AL_kTopCamera, AL_kQVGA, AL_kBGRColorSpace, 10)

width = 320
height = 240
image = np.zeros((height, width, 3), np.uint8)

while True:

    result = videoDevice.getImageRemote(captureDevice);

    if result == None:
        print 'cannot capture.'
    elif result[6] == None:
        print 'no image data string.'
    else:

        values = map(ord, list(result[6]))
        i = 0
        for y in range(0, height):
            for x in range(0, width):
                image.itemset((y, x, 0), values[i + 0])
                image.itemset((y, x, 1), values[i + 1])
                image.itemset((y, x, 2), values[i + 2])
                i += 3

        cv2.imshow("pepper-top-camera-320x240", image)
        f = open(image, "rb")
        faceapi_body = f.read()
        f.close()
        conn.request("POST", "/face/v1.0/detect?%s" % faceapi_params, faceapi_body, faceapi_headers)
        response = conn.getresponse()
        data = response.read()                
        decoded = json.loads(data)
        tts.loadVoicePreference("NaoOfficialVoiceEnglish")
        nombrepersonne = len(decoded)
                # print(nombrepersonne)
                json_object["nb_personne"] = str(nombrepersonne)
                for i in range(len(decoded)):
                    sexe = decoded[i]["faceAttributes"]["gender"]
                    age = int(decoded[i]["faceAttributes"]["age"])
                    glasses = decoded[i]["faceAttributes"]["glasses"]
                    tts.say("You are a " % sexe )
                    tts.say("You are " % age )

    if cv2.waitKey(33) == 27:
        break