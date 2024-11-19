import pickle
import util

class Pickler:
    @staticmethod
    def read_dump(path):
        with open(util.Util.PROJ_DIR + "/saves/" + path,'rb') as f:
            return pickle.load(f)


    @staticmethod
    def dump(path,dump):
        with open(util.Util.PROJ_DIR + "/saves/" + path,'wb') as f:
            pickle.dump(dump,f)