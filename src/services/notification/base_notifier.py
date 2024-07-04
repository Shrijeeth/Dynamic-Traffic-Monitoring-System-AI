"""
Base Notifier Module
"""

import abc


class BaseNotifier(metaclass=abc.ABCMeta):
     """
     A class that defines the base notification service.
     """

     @abc.abstractmethod
     def send_notification(self, **kwargs):
          """
          A method to send a notification.
          """
          raise NotImplementedError

     @abc.abstractmethod
     def validate_notification(self, data: dict):
          """
          A method to validate the notification data.
          """
          raise NotImplementedError


     @abc.abstractmethod
     def close_connection(self):
          """
          A method to close the connection to notifier.
          """
          raise NotImplementedError
