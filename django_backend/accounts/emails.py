from django.contrib.auth.tokens import default_token_generator
from djoser import email, utils
from djoser.conf import settings

from django.template.loader import render_to_string, get_template

import os


class ActivationEmail(email.ActivationEmail):
    
    template_name = '../templates/activation.html'
    

    def get_context_data(self):
        context = super().get_context_data()


        try:
            user = context.get("user")
            context["first_name"] = user.first_name
            context["uid"] = utils.encode_uid(user.pk)
            context["token"] = default_token_generator.make_token(user)
            context["url"] = settings.ACTIVATION_URL.format(**context)

            return context
        except Exception as e:
            print(e)
            return context


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "../templates/confirmation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()
        user = context.get("user")
        context["first_name"] = user.first_name

        return context

class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "../templates/password_reset.html"

    def get_context_data(self):
        # PasswordResetEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.PASSWORD_RESET_CONFIRM_URL.format(**context)
        context["first_name"] = user.first_name

        
        return context


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "../templates/password_changed_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["first_name"] = user.first_name

        return context