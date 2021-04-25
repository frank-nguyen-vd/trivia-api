export FLASK_APP=flaskr
export FLASK_ENV=development
waitress-serve --cal --listen=*:5000 'flaskr:create_app'