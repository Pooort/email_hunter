import csv

from repo.company import CompanyRepo
from repo.email import EmailRepo
from settings import CSVDELIMITER

fields = CompanyRepo.get_fields()
fields.extend(EmailRepo.get_fields())

fields.remove('emails')

with open('emails.csv', 'w', newline='') as csvfile:
    fieldnames = fields
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=CSVDELIMITER, extrasaction='ignore')
    writer.writeheader()
    for company in CompanyRepo.get_all():
        for email in company.emails:
            data = company.__dict__
            data.update(email.__dict__)
            writer.writerow(data)
