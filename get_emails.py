from network.hunter import HunterManager
from repo.company import CompanyRepo


def main():
    for data in CompanyRepo.get_all():
        domains_data = HunterManager.get_domain_data(data['website'])
        for email_data in domains_data['emails']:
            email_data['company_id'] = data['id']


if __name__ == '__main__':
    main()
