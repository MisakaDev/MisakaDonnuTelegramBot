import datetime

from gino import Gino

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
        return await Schedule.query.where(
            Schedule.group_id == self.group_id
        ).where(
            Schedule.date == date.date()
        ).order_by(
            Schedule.pair_number
        ).gino.all()


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode())
    course = db.Column(db.Unicode())

    @classmethod
    async def get_or_create(cls, name, course):
        instance = await cls.query.where(cls.name == name).where(cls.course == course).gino.first()
        if not instance:
            instance = await cls.create(name=name, course=course)
        return instance

    @classmethod
    async def get_all(cls):
        return await cls.query.gino.all()

    @classmethod
    async def get(cls, name, course):
        return await cls.query.where(cls.name == name).where(cls.course == course).gino.first()

    @classmethod
    async def get_by_id(cls, uid):
        return await cls.query.where(cls.id == uid).gino.first()

    @classmethod
    async def get_by_course(cls, course):
        return await cls.query.where(cls.course == course).gino.all()

    @classmethod
    async def get_course_list(cls):
        return await db.select([
            cls.course,
        ]).select_from(
            cls
        ).group_by(
            cls.course,
        ).order_by(
            cls.course.desc()
        ).gino.all()


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer(), primary_key=True)
    pair_number = db.Column(db.Integer(),)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    information = db.Column(db.Unicode())
    date = db.Column(db.Date(), default=datetime.datetime.now)

    @classmethod
    async def create(cls, group_id, date, pair_number, information):
        return await super().create(group_id=group_id, pair_number=pair_number, information=information, date=date)


class Statistic(db.Model):
    __tablename__ = 'statistics'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.Unicode())
    date = db.Column(db.DateTime(), default=datetime.datetime.now)

    @classmethod
    async def create(cls, user_id, message):
        return await super().create(user_id=user_id, message=message)

    @classmethod
    async def message_rating(cls):
        count = db.func.count(cls.id)
        return await db.select([
            cls.message,
            count,
        ]).select_from(
            cls
        ).group_by(
            cls.message,
        ).order_by(
            count.desc()
        ).gino.all()

    @classmethod
    async def count_by_date_interval(cls, start, end):
        count = db.func.count(cls.id)
        return await db.select(
            [count]
        ).select_from(
            cls
        ).where(
            cls.date > start
        ).where(
            cls.date < end
        ).gino.scalar()

    @classmethod
    async def active_users_by_date_interval(cls, start, end):
        return len(await db.select(
            [cls.user_id]
        ).select_from(
            cls
        ).where(
            cls.date > start
        ).where(
            cls.date < end
        ).group_by(
            cls.user_id
        ).gino.all())
