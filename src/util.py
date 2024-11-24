import os

class Util:
  """A utility class containing useful functions"""
  # using __ is convention for "private" vars
  # class variable __instance will keep track of the lone object instance
  __instance = None
  __PROJ_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

  # allows us to do tmp = Util();
  def __new__(cls):
    if cls.__instance is None:
      cls.__instance = super(Util, cls).__new__(cls)
    return cls.__instance

  def get_project_dir(self):
    """Get the path to the project dir"""
    return self.__PROJ_DIR
