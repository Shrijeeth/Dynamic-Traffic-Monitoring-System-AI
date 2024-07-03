# pylint: disable=bad-mcs-method-argument,too-few-public-methods

"""
Module that defines the base model registry for AI models.
"""

import abc


class BaseModelRegistry(metaclass=abc.ABCMeta):
    """
    A class that defines the base ai model registry.
    """

    @abc.abstractmethod
    def load_model(self):
        """
        A method to load a model.
        """
        raise NotImplementedError
