import abc
import time
import loompy

class MethodRunner(abc.ABC):
    """ Interface class encapsulating required methods to run a normalization algorithm. """
    def __init__(self, data, verbose):
        self.data = data
        self.verbose = verbose

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError("Subclasses of MethodRunner are required to override this method.")

    def dump_to_loom(self, filename, latent_matrix, row_attrs, col_attrs):
        filename = filename + "_" + str(int(time.time())) + ".loom"
        loompy.create(filename, latent_matrix, row_attrs, col_attrs)
