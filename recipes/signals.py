from django.dispatch import receiver
from django.db.models import signals
from django.utils.crypto import get_random_string
from django.utils.text import slugify

from transliterate import translit

from recipes.models import Recipe

@receiver(signals.pre_save, sender=Recipe)
def create_slug(sender, instance, **kwargs):

    slug_str = "%s %s" % (translit(instance.title, "ru", reversed=True), get_random_string(length=4))
    instance.slug = slugify(slug_str)