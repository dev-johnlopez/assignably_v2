from app import db
from flask_security import current_user
from app.search import add_to_index, remove_from_index, query_index
from transitions import Machine
from sqlalchemy.ext.declarative import declared_attr
import datetime


class AuditMixin(object):
    #AuditMixin
    #Mixin for models, adds 4 columns to stamp, time and user on creation and modification
    #will create the following columns:

    #:created on:
    #:changed on:
    #:created by:
    #:changed by:
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    changed_on = db.Column(db.DateTime, default=datetime.datetime.now,
                        onupdate=datetime.datetime.now, nullable=False)

    @declared_attr
    def created_by_fk(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'),
                      default=cls.get_user_id, nullable=False)

    @declared_attr
    def created_by(cls):
        return db.relationship("User", primaryjoin='%s.created_by_fk == user.id' % cls.__name__, enable_typechecks=False)

    @declared_attr
    def changed_by_fk(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'),
                      default=cls.get_user_id, onupdate=cls.get_user_id, nullable=False)

    @declared_attr
    def changed_by(cls):
        return db.relationship("User", primaryjoin='%s.changed_by_fk == user.id' % cls.__name__, enable_typechecks=False)

    @classmethod
    def get_user_id(cls):
        try:
            return current_user.id
        except Exception as e:
            # log.warning("AuditMixin Get User ID {0}".format(str(e)))
            return None


class StateMixin(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def status(cls):
        return db.Column(db.String())

    @property
    def state(self):
        return self.status

    @state.setter
    def state(self, value):
        if self.status != value:
            self.status = value

    def after_state_change(self):
        self._session.add(self)
        self._session.commit()

    @classmethod
    def init_state_machine(cls, obj, *args, **kwargs):
        # when we load data from the DB(via query) we need to set the proper initial state
        initial = obj.status or 'new'
        states = ['new', 'active', 'closed']
        transitions = [
            ['activate', 'new', 'active'],
            ['close', 'active', 'closed']
        ]

        machine = Machine(model=obj, states=states, transitions=transitions, initial=initial,
                          after_state_change='after_state_change')

        # in case that we need to have machine obj in model obj
        setattr(obj, 'machine', machine)

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
