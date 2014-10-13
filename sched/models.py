from datetime import datetime
from sqlalchemy import Boolean, Column, ForeignKey
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import check_password_hash
from werkzeug import generate_password_hash

Base = declarative_base()


class User(Base):

    """A user login, with credentials and authentication."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    name = Column('name', String(200))
    email = Column(String(100), unique=True, nullable=False)
    active = Column(Boolean, default=True)

    _password = Column('password', String(100))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
        password_descriptor = property(self._get_password, self._set_password)
        password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        if self._password is None:
            return False
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self._password, password)

    @classmethod
    def authenticate(cls, query, email, password):
        email = email.strip().lower()
        user = query(cls).filter(cls.email == email).first()
        if user is None:
            return None, False
        if not user.active:
            return user, False
        return user, user.check_password(password)

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class Appointment(Base):

    """An appointment on the calendar."""
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    modified = Column(DateTime, default=datetime.now,
                      onupdate=datetime.now)

    title = Column(String(255))
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    allday = Column(Boolean, default=False)
    location = Column(String(255))
    description = Column(Text)

    user_id = Column(Integer,
                     ForeignKey('user.id'), nullable=False)
    user = relationship(User, lazy='joined', join_depth=1)

    @property
    def duration(self):
        delta = self.end - self.start
        return delta.days * 24 * 60 * 60 + delta.seconds

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))

if __name__ == "__main__":
    from datetime import timedelta
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_engine('sqlite:///sched.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

#    Add user1
    user = User(name="User1", email="hola@adios.com")
    user._set_password("12345")
    session.add(user)
    session.commit()

    now = datetime.now()
    appt = Appointment(
        title='New appointment', start=now,
        end=now + timedelta(seconds=1800),
        allday=False, location='the office', description='test', user_id=1)

    session.add(appt)
    session.commit()
    
    now = datetime.now()
    appt = Appointment(
        title='New appointment2', start=now,
        end=now + timedelta(seconds=1800),
        allday=False, location='the office', description='test', user_id=1)

    session.add(appt)
    session.commit()
