from network.angel import AngelManager
from repo.company import CompanyRepo


def main():
    for data in AngelManager.get_companies_data():
        for company in data:
            CompanyRepo.create_or_update(company)

if __name__ == '__main__':
    main()
