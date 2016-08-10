import cv2

class InputVideoStream:

  def __init__(self, src):
    # initilize the sream and read the first frame
    self.stream = cv2.VideoCapture(src)
    (self.grabbed, self.frame) = self.stream.read()
    self.stopped= False

  def start(self):
    Process(target=self.update, args=()).start()
    return self

  def update(self):
    while True:
      if self.stopped:
        return
      (self.grabbed, self.frame) = self.stream.read()

  def read(self):
    return self.frame

  def stop(self):
    self.stream.release()
    self.stopped
