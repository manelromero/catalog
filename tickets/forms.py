from wtforms import Form, StringField, validators

class CategoryForm(Form):
	name = StringField('Category', [validators.Required()])