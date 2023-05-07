from flask import Flask, request, redirect
from flask_kerberos import (
    Kerberos,
    REQUIRED,
    HTTP_ERROR_AUTH_REQUIRED,
    HTTP_ERROR_FORBIDDEN
)

app = Flask(__name__)
kerberos = Kerberos(app)

@app.route('/')
@kerberos.authenticated_or_401()
def index():
    return 'Hello, {}!'.format(request.remote_user)

@app.route('/admin')
@kerberos.authenticated_or_401()
def admin():
    if not kerberos.check_roles('admin'):
        return redirect('/')
    return 'Welcome, {}!'.format(request.remote_user)

@app.route('/logout')
def logout():
    kerberos.logout()
    return redirect('/')

@app.errorhandler(HTTP_ERROR_AUTH_REQUIRED)
def handle_auth_error():
    return redirect('/login')

@app.errorhandler(HTTP_ERROR_FORBIDDEN)
def handle_forbidden_error():
    return 'You do not have permission to access this resource.'

if __name__ == '__main__':
    app.run()
