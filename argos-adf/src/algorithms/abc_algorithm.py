from abc import ABCMeta, abstractmethod


class AbstractAlgorithm(metaclass=ABCMeta):
    @abstractmethod
    def fit(self, datapoints):
        raise NotImplementedError
