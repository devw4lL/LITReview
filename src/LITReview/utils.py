import unicodedata
import string
import os

from PIL import Image

from .constants import image_size

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255


def rename_picture(instance, filename):
    model = str(instance._meta.model).split('.')[-1].lower().replace("'", "").replace(">", "")
    ext = filename.split('.')[-1]
    if model == 'ticket':
        filename = os.path.join(model, (str(instance.user_id) + '_' + clean_filename(instance.title) + '.' + ext))
    elif model == 'customuser':
        model = "users"
        filename = os.path.join(model, (str(instance.first_name) + '_' + (str(instance.last_name) +'_' + clean_filename(instance.nick_name) + '.' + ext)))
    else:
        raise ValueError("Erreur de nom de fichier image")
    return filename


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    for r in replace:
        filename = filename.replace(r, '_')

    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)

    return cleaned_filename[:char_limit]


def resize_image(image, size):
    img = Image.open(image)  # Open image using self
    return img.resize(image_size[size], Image.ANTIALIAS)
