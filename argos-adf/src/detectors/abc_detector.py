from abc import ABCMeta, abstractmethod


class AbstractDetector(metaclass=ABCMeta):
    @abstractmethod
    def fit(self):
        raise NotImplementedError
