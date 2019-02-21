from db import session
from db.models import Location


class LocationRepo:

    @staticmethod
    def get_fields():
        return [key for key in Location.__dict__.keys() if not key.startswith('_') and key != 'id']

    @staticmethod
    def get_all():
        return session.query(Location).all()

    @staticmethod
    def create_or_update(data):
        q = session.query(Location).filter_by(location_id=data['location_id'])
        company = q.first()
        if not company:
            company = Location(**data)
            session.add(company)
            session.commit()
        else:
            q.update(data)
