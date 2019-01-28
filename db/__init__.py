from gino import Gino
import datetime
import config

db = Gino()


async def prepare_db():
    try:
        await db.set_bind('postgresql://{}:{}@{}/{}'.format(config.DB_USER_LOGIN,
                                                            config.DB_USER_PASSWORD,
                                                            config.DB_HOST,
                                                            config.DB_NAME)
                          )
        await db.gino.create_all()
    except Exception as error:
        print(f"Error on prepare database: {error}")
        exit()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    telegram_id = db.Column(db.Integer(), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))

    @classmethod
    async def get_or_create(cls, telegram_id):
        instance = await cls.query.where(cls.telegram_id == telegram_id).gino.first()
        if not instance:
            instance = await cls.create(telegram_id=telegram_id)
        return instance

    async def set_group(self, group_id):
        await self.update(group_id=group_id).apply()

    async def get_schedule_by_day(self, date):
        return []


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(), unique=True)

    @classmethod
    async def get_or_create(cls, name):
        instance = await cls.query.where(cls.name == name).gino.first()
        if not instance:
            instance = await cls.create(name=name)
        return instance

    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def get(cls, name):
        return await cls.query.where(cls.name == name).gino.first()

    @classmethod
    async def get_by_id(cls, uid):
        return await cls.query.where(cls.id == uid).gino.first()


class Statistic(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Unicode())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)

    @classmethod
    async def create(cls, user_id, message):
        return await super().create(user_id=user_id, message=message)
