from tqdm import tqdm

from network.angel import AngelManager
from repo.company import CompanyRepo


def main():
    bar = tqdm()
    # for data in AngelManager.get_companies_data_by_price():
    #     for company in data:
    #         bar.update()
    #         CompanyRepo.create_or_update(company)

    bar = tqdm()
    for data in AngelManager.get_companies_data_by_location():
        for company in data:
            bar.update()
            CompanyRepo.create_or_update(company)


if __name__ == '__main__':
    main()
