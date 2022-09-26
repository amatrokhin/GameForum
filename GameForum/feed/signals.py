from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Reply
from .tasks import notify_receiver, notify_creator


# send mail to post creator when it get a reply or notify reply creator when reply is accepted
@receiver(post_save, sender=Reply,)
def notify_new_reply(sender, instance, created, **kwargs):
    if created:
        notify_receiver.delay(instance.pk)              # transfer key instead of object for less ram usage

    else:
        notify_creator.delay(instance.pk)
