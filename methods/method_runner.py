import abc

class MethodRunner(abc.ABC):
    """ Interface class encapsulating required methods to run a normalization algorithm. """
    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses of MethodRunner are required to override this method.")