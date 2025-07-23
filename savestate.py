import json
import os
import random


CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))


class SaveState:
    def check_save_file(self) -> bool:
        return os.path.exists(os.path.join(CURRENT_FOLDER, 'save.json'))

    def create_save_file(self) -> None:
        if not os.path.exists(os.path.join(CURRENT_FOLDER, 'photos')):
            raise FileNotFoundError('photos folder not found')
        
        photos = os.listdir(os.path.join(CURRENT_FOLDER, 'photos'))
        if 'put_images_here' in photos:
            photos.remove('put_images_here')
        random.shuffle(photos)

        with open(os.path.join(CURRENT_FOLDER, 'save.json'), 'w') as f:
            json.dump({
                idx: {
                    'photo': os.path.join(CURRENT_FOLDER, 'photos', photo),
                    'rating': 0
                } for idx, photo in enumerate(photos)
            }, f, indent=4)

    def load(self) -> dict[int, dict[str, str | int]]:
        if not self.check_save_file():
            self.create_save_file()
        
        with open(os.path.join(CURRENT_FOLDER, 'save.json'), 'r') as f:
            return json.load(f)

    def save(self, data: dict[int, dict[str, str | int]]) -> None:
        with open(os.path.join(CURRENT_FOLDER, 'save.json'), 'w') as f:
            json.dump(data, f, indent=4)
