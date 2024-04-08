from allauth.account.adapter import DefaultAccountAdapter
from django.contrib import messages

class NoMessagesAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template,
                    message_context={}, extra_tags=''):
        """
        Override the default method to prevent messages from being added
        """
        pass