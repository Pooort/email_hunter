from db import session
from db.models import Company, Email


class CompanyRepo:

    @staticmethod
    def get_ids():
        return session.query(Company.id).all()

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
