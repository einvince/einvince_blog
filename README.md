This a personal blog power by Flask.

[einvince](http://www.einvince.link/)

###Backend:  
  1. [Flask](http://flask.pocoo.org/)
  2. [Flask-SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/) ORM for MySQL
  3. [Flask-WTF](https://flask-wtf.readthedocs.org/en/latest/)
  4. [Flask-Login](https://flask-login.readthedocs.org/en/latest/)  
  5. [Flask-Admin](http://flask-admin.readthedocs.org/en/latest/)  
  6. [Flask-Script](http://flask-script.readthedocs.org/en/latest/)  

---
###Installation

1. Git clone the repostory.
2.  `pip install -r requirement.txt` command .
3. Change the database settings inside `app/__init__.py` file.
4. Run the migration by this command

        $ python manage.py db init
        $ python manage.py db migrate
        $ python manage.py db upgrade
5. Run the server by this command
        
        $ python manage.py runserver

