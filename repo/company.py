from db import session
from db.models import Company, Email


class CompanyRepo:

    @staticmethod
    def get_fields():
        return [key for key in Company.__dict__.keys() if not key.startswith('_') and key != 'id']

    @staticmethod
    def get_all():
        return session.query(Company).all()

    @staticmethod
    def create_or_update(data):
        q = session.query(Company).filter_by(name=data['name'])
        company = q.first()
        if not company:
            company = Company(**data)
            session.add(company)
            session.commit()
        else:
            q.update(data)
