sudo -u postgres dropdb trivia_test
sudo -u postgres createdb trivia_test
sudo -u postgres psql trivia_test < trivia.psql
source env/bin/activate
python test_flaskr.py