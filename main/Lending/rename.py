import os
import uuid
from django.conf import settings
from Lending.models import ImagesQuiz, Icons, ImageForExampleOfWork 

def generate_random_filename(original_filename, upload_dir):
    ext = original_filename.split('.')[-1].lower()
    return os.path.join(upload_dir, f"{uuid.uuid4().hex}.{ext}")

def rename_files_for_model(model_class, upload_dir):
    queryset = model_class.objects.all()
    for obj in queryset:
        old_path = obj.file.path 
        new_rel_path = generate_random_filename(os.path.basename(old_path), upload_dir)
        new_abs_path = os.path.join(settings.MEDIA_ROOT, new_rel_path)

        os.makedirs(os.path.dirname(new_abs_path), exist_ok=True)

        os.rename(old_path, new_abs_path)

        obj.file.name = new_rel_path
        obj.save()

        print(f"{model_class.__name__}: {old_path} -> {new_abs_path}")

def main():
    rename_files_for_model(ImagesQuiz, 'lending/data/quizPhotos')
    rename_files_for_model(Icons, 'lending/data/icons')
    rename_files_for_model(ImageForExampleOfWork, 'lending/data/examplesOfWork')

if __name__ == "__main__":
    main()
