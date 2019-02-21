from tqdm import tqdm

from network.angel import AngelManager
from repo.location import LocationRepo


def main():
    bar = tqdm()
    for data in AngelManager.get_locations():
        for location in data:
            bar.update()
            LocationRepo.create_or_update(
                {
                    'location_id': location['tag']['id'],
                    'display_name': location['tag']['display_name']
                 }
            )


if __name__ == '__main__':
    main()
