import numpy
from os import environ
import qrcode
from PIL import Image
import cv2 as cv
import webbrowser

###########################################################################


def generateQR(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black",back_color="white").convert("RGB")
    img.save("sample.png")
    return img

def decodeQR(image):
    im = cv.cvtColor(numpy.array(image),cv.COLOR_RGB2BGR)
    det = cv.QRCodeDetector()
    retval, points, straight_qrcode = det.detectAndDecode(im)
    # print(retval)
    return retval

def scanQR():
    cap = cv.VideoCapture(0)
    detector = cv.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            a = data
            break
        cv.imshow("QRCODEscanner", img)    
        if cv.waitKey(1) == ord("q"):
            break
    print(a)
    #Change link to localhost to show voucher redeemed
    b=webbrowser.open(str(a))
    cap.release()
    cv.destroyAllWindows()

# text = 'test'
# image2 = generateQR(text)
# decodeQR(image2)
# scanQR()