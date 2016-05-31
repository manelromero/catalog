from wtforms import Form, StringField, DateField, PasswordField, SelectField,\
    validators, ValidationError


class LoginForm(Form):
    username = StringField('User', [
        validators.InputRequired(message='You have to introduce an user'),
        validators.Length(
            max=8,
            message='User cannot be longer than 8 characters'
            )
        ])
    password = PasswordField('Password', [
        validators.InputRequired(message='You have to introduce a password'),
        validators.Length(
            min=4,
            max=10,
            message='Password must have between 4 and 10 characters'
            )
        ])


class CategoryForm(Form):
    name = StringField('Category', [
        validators.InputRequired(
            message='You have to introduce a name for the Category'
        ),
        validators.Length(
            max=15,
            message='The name cannot be longer than 15 characters'
            )
        ])


class EventForm(Form):
    category_id = SelectField('Category', [
        validators.InputRequired(
            message='You have to select a Category'
            )],
            coerce=int
            )
    name = StringField('Event', [
        validators.InputRequired(message='You have to introduce a name'),
        validators.Length(
            max=30,
            message='The name cannot be longer than 30 characters'
            )
        ])
    location = StringField('Location', [
        validators.InputRequired(message='You have to introduce a name'),
        validators.Length(
            max=25,
            message='The name cannot be longer than 25 characters'
            )
        ])
    date = DateField('Date', [
        validators.InputRequired(
            message='You have to introduce a date')],
            format='%d/%m/%Y'
            )

    def validate_category_id(form, field):
        if field.data == 0:
            raise ValidationError('You have to select a category')
