from django.db.models.signals import post_save
from django.dispatch import receiver
from wechat.tasks import send_template, t_send_template
from codex.taskutils import *
from django.utils import timezone
from datetime import datetime, time, timedelta
from .models import *
import logging
logger = logging.getLogger(name=__name__)

@receiver(post_save, sender=HomeworkStatus)
def update_hw_status(sender, instance, raw, **kwargs):
    if raw:
        return

    def graded(tup):
        nonlocal instance
        send_template(instance.student.open_id, instance)

    def ignored(tup):
        nonlocal instance
        if tup[1]:
            # revoke(t_send_template, args=None)
            pass
        else:
            ahead = instance.student.pref.s_ddl_ahead_time
            eta = timezone.make_aware(datetime.combine(instance.homework.end_time, time(
                23, 59, 59)) - timedelta(minutes=ahead) if not getattr(instance, 'force_now', False) else datetime.now() + timedelta(seconds=10), timezone.get_current_timezone())
            send_template(instance.student.open_id,
                          instance.homework, '', safe_apply_async, eta=eta)
    logger.critical(instance.changes().items())
    # for k, v in instance.changes().items():
    #     if k == 'graded':
    #         graded(v)
    #     elif k == 'ignored':
    #         ignored(v)
    #     else:
    #         pass
    # if 'ignored' not in instance.changes():
        # ignored((0, 0))
    # if getattr(instance, 'force_now', False):
        # ignored((0, 0))


from userpage.models import Student


@receiver(post_save, sender=Homework)
def create_hw_status(sender, instance, raw, **kwargs):
    if raw:
        return
    try:
        status = HomeworkStatus.objects.get(student=instance._status.student, homework__xt_id=instance.xt_id)
    except:
        status = HomeworkStatus(student=instance._status.student, homework=instance)
    status.__dict__.update({
        'submitted': instance._status.submitted,
        'graded': instance._status.graded,
        'grading': instance._status.grading,
        'grading_comment': instance._status.grading_comment,
        'graded_by': instance._status.graded_by,
    })
    status.save()
