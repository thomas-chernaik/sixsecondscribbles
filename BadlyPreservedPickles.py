import pickle, threading, time, os

class BadlyPreservedPickles:

    def __init__(self):
        self.fileExpiry = []
        #clean up existing files
        for file in os.listdir(os.path.dirname(__file__)):
            if file.endswith(".pickle"):
                os.remove(os.path.join(os.path.dirname(__file__), file))
        self.cleanUpThread = threading.Thread(target=self.cleanUp)
        self.cleanUpThread.start()

    def cleanUp(self):
        while True:
            for file in self.fileExpiry:
                if file[1] <= time.time():
                    path = os.path.join(os.path.dirname(__file__), file[0])
                    os.remove(path)
                    print("hi")
                    self.fileExpiry.remove(file)
            time.sleep(30)

    def pickle(self, obj, linkName, expiry):
        filename = linkName + ".pickle"
        pickle.dump(obj, open(filename, "wb"))
        #remove old file if it exists
        for file in self.fileExpiry:
            if file[0] == filename:
                self.fileExpiry.remove(file)
        self.fileExpiry.append((filename, time.time() + expiry))
        return filename

    def unpickle(self, filename):
        return pickle.load(open(filename, "rb"))
