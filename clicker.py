import time


class Clicker(object):
    position = None
    click_time = None

    def click(self, position):
        self.position = position
        self.click_time = time.time()
