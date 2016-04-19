from app import Content
from app import db
from sqlalchemy.exc import IntegrityError

def generate_fake(count=100):
    from random import seed
    import forgery_py
    seed()
    for i in range(count):
        u =Content(id=i+1,
        title=forgery_py.internet.user_name(True),\
        body_html=forgery_py.name.full_name(),\
        body=forgery_py.lorem_ipsum.sentence(),\
        abstract=forgery_py.lorem_ipsum.sentence(),\
        pub_time=forgery_py.date.date(True),\
        category=forgery_py.lorem_ipsum.sentence(),\
        )

        db.session.add(u)
    try:
        db.session.commit()
        print "ok"
    except IntegrityError:
        db.session.rollback()

generate_fake(count=100)
