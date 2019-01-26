from copy import deepcopy

from db import session
from db.models import Email


class EmailRepo:

    @staticmethod
    def filter_dict(data):
        d = deepcopy(data)
        company_fields = dir(Email)
        delete_keys = [k for k in d if k not in company_fields]
        for key in delete_keys:
            del d[key]
        return d

    @staticmethod
    def create_or_update(data):
        filtered_data = EmailRepo.filter_dict(data)
        q = session.query(Email).filter_by(value=filtered_data['value'])
        email = q.first()
        if not email:
            email = Email(**filtered_data)
            session.add(email)
            session.commit()
        else:
            q.update(filtered_data)
