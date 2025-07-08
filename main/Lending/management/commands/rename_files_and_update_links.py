import os
import uuid
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from Lending.models import ImageForExampleOfWork, LendingPage


def generate_random_filename(original_filename, upload_dir):
    ext = original_filename.split('.')[-1].lower()
    return os.path.join(upload_dir, f"{uuid.uuid4().hex}.{ext}")


def rename_files_for_model(model_class, upload_dir):
    """ Переименовывает файлы и возвращает соответствие старых и новых URL """
    file_map = {}  # old_url -> new_url
    queryset = model_class.objects.all()

    for obj in queryset:
        old_path = obj.file.path
        old_url = obj.file.url

        new_rel_path = generate_random_filename(os.path.basename(old_path), upload_dir)
        new_abs_path = os.path.join(settings.MEDIA_ROOT, new_rel_path)
        new_url = settings.MEDIA_URL + new_rel_path

        os.makedirs(os.path.dirname(new_abs_path), exist_ok=True)
        os.rename(old_path, new_abs_path)

        obj.file.name = new_rel_path
        obj.save()

        file_map[old_url] = new_url
        print(f"{model_class.__name__}: {old_path} -> {new_abs_path}")

    return file_map


def update_lending_examples(file_map):
    """ Обновляет все ссылки в поле examplesOfWork у всех лендингов """
    pages = LendingPage.objects.all()
    for page in pages:
        changed = False
        examples = page.examplesOfWork

        if not examples:
            continue

        for example in examples:
            images = example.get("images", [])
            for image in images:
                for key in ["url", "mobaleUrl"]:
                    old_val = image.get(key)
                    if old_val in file_map:
                        image[key] = file_map[old_val]
                        changed = True
                        print(f"Updated {key}: {old_val} -> {file_map[old_val]}")

        if changed:
            page.examplesOfWork = examples
            page.save()
            print(f"Updated LendingPage id={page.id}")


class Command(BaseCommand):
    help = 'Переименовывает файлы и обновляет ссылки в examplesOfWork'

    def handle(self, *args, **options):
        self.stdout.write('Начинаем переименование файлов и обновление ссылок...')

        file_map = rename_files_for_model(ImageForExampleOfWork, 'lending/data/examplesOfWork')
        update_lending_examples(file_map)

        self.stdout.write(self.style.SUCCESS('Готово! Файлы переименованы и ссылки обновлены.'))
