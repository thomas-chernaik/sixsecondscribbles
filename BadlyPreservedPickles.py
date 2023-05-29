import pickle, threading

class BadlyPreservedPickles:

    def __init__(self):
        self.fileExpiry = []
        self.cleanUpThread = threading.Thread(target=self.cleanUp)
        self.cleanUpThread.start()

    def cleanUp(self):
        while True:
            for file in self.fileExpiry:
                if file[1] <= time.time():
                    os.remove(file[0])
                    self.fileExpiry.remove(file)
            time.sleep(1)

    def pickle(self, obj, expiry):
        filename = str(time.time()) + ".pickle"
        pickle.dump(obj, open(filename, "wb"))
        self.fileExpiry.append((filename, time.time() + expiry))
        return filename

    def unpickle(self, filename):
        return pickle.load(open(filename, "rb"))
