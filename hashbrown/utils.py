from django.conf import settings
from .models import Switch


def is_active(label, user=None):
    defaults = getattr(settings, 'HASHBROWN_SWITCH_DEFAULTS', {})

    globally_active = defaults[label].get( 'globally_active', False)

    description = defaults[label].get(
        'description',
        '') if label in defaults else ''

    switch, created = Switch.objects.get_or_create(
        label=label, defaults={
            'globally_active': globally_active,
            'description': description,
        })

    if created:
        return switch.globally_active

    if switch.globally_active or (
        user and user.available_switches.filter(pk=switch.pk).exists()
    ):
        return True
    return False
