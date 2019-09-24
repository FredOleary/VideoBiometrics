import cv2


class ROISelector:
    def __init__(self, config):
        self.config = config
        self.face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
        self.mouth_cascade = cv2.CascadeClassifier('data/haarcascade_mcs_mouth.xml')

    def select_roi(self, frame):
        found = False
        x = 0
        y = 0
        w = 0
        h = 0
        if self.config['feature_method'] == 'face' or \
            self.config['feature_method'] == 'mouth' or \
            self.config['feature_method'] == 'forehead':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 1:
                for (x, y, w, h) in faces:
                    if self.config['feature_method'] == 'mouth':
                        roi_gray = gray[y:y+h, x:x+w]
                        mouth = self.mouth_cascade.detectMultiScale(roi_gray, 1.3, 5)
                        for( x_mouth, y_mouth, w, h) in mouth:
                            x += x_mouth
                            y += y_mouth
                            found = True
                            break
                    elif self.config['feature_method'] == 'forehead':
                        # For forehead detection, use the top fraction of face and 3/5 width
                        # (These are empirical values)
                        h = int(h/5)
                        x = x + int(w/5)
                        w = int(3*w/5)
                        found = True
                        break
                    else:
                        found = True
                        break

        elif self.config['feature_method'] == 'selectROI':
            r = cv2.selectROI(frame)
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            found = True

        return found, x, y, w, h