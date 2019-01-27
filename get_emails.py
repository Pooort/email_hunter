from tqdm import tqdm

from network.hunter import HunterManager
from repo.company import CompanyRepo
from repo.email import EmailRepo


def main():
    bar = tqdm()
    for company in CompanyRepo.get_all():
        if len(company.emails) != 0:
            continue
        domains_data = HunterManager.get_domain_data(company.website)
        bar.update()
        if domains_data.get('data') is None:
            print(domains_data['errors'][0]['details'])
            break
        for email_data in domains_data['data']['emails']:
            email_data['company_id'] = company.id
            EmailRepo.create_or_update(email_data)


if __name__ == '__main__':
    main()
