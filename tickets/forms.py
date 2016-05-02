from wtforms import Form, StringField, validators

class CategoryForm(Form):
	name = StringField('Category', [
		validators.InputRequired(message='You have to introduce a name'),
		validators.Length(max=25, message='The name cannot be longer than 25 \
			characters')
		])