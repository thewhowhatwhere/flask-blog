from wtforms import form, fields, validators
from werkzeug.security import check_password_hash

from mamba import db
from mamba.auth.models import User


class LoginForm(form.Form):
    email = fields.StringField(
        validators=[validators.required(), validators.length(max=120)])
    password = fields.PasswordField(
        validators=[validators.required(), validators.length(max=255)])

    def validate_login(self):
        user = self.get_user_by_email()

        if user is None:
            self.errors[0] = 'Invalid user'
            return False

        if not user.is_active():
            self.errors[0] = 'Invalid user'
            return False

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
            self.errors[0] = 'Invalid user'
            return False

        return user

    def get_user_by_email(self):
        return db.session.query(User).filter(
            User.email == self.email.data).first()


class RegistrationForm(form.Form):
    email = fields.StringField(
        validators=[validators.required(), validators.length(max=120)])
    password = fields.PasswordField(
        validators=[validators.required(), validators.length(max=255)])

    def validate_registration(self):
        if db.session.query(User).filter_by(email=self.email.data).count() > 0:
            self.errors[0] = 'Invalid user'
            return False
        return True
