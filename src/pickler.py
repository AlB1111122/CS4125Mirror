import pickle
import util

class Pickler:
    """Loads and saves models to disk"""
    @staticmethod
    def read_dump(path):
        """Dumps teh model to disk"""
        with open(util.Util().get_project_dir() + "/saves/" + path,'rb') as f:
            return pickle.load(f)


    @staticmethod
    def dump(path,dump):
        """Loads a model from disk"""
        with open(util.Util().get_project_dir() + "/saves/" + path,'wb') as f:
            pickle.dump(dump,f)