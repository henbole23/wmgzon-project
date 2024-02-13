import flask_bcrypt

p = flask_bcrypt.generate_password_hash('admin')
print(p)