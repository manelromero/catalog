from wtforms import Form, StringField, PasswordField, validators


class LoginForm(Form):
    user = StringField('User', [
        validators.InputRequired(message='You have to introduce an user'),
        validators.Length(max=8, message='The user cannot be longer than 8 \
            characters')
        ])
    password = PasswordField('Password', [
        validators.InputRequired(message='You have to introduce a password'),
        validators.Length(min=4, max=8, message='The password must have \
            between 4 and 8 characters')])


class CategoryForm(Form):
    name = StringField('Category', [
        validators.InputRequired(message='You have to introduce a name'),
        validators.Length(max=25, message='The name cannot be longer than 25 \
            characters')])