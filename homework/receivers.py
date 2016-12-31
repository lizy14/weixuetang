from django.db.models.signals import post_save
from django.dispatch import receiver
from wechat.tasks import send_template, t_send_template
from codex.taskutils import *
from django.utils import timezone
from datetime import datetime, time, timedelta


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
    for k, v in instance.changes().items():
        if k == 'graded':
            graded(v)
        elif k == 'ignored':
            ignored(v)
        else:
            pass
    # if 'ignored' not in instance.changes():
        # ignored((0, 0))
    if getattr(instance, 'force_now', False):
        ignored((0, 0))


from userpage.models import Student


@receiver(post_save, sender=Homework)
def create_hw_status(sender, instance, raw, **kwargs):
    if raw:
        return
    subscribes = CourseStatus.objects.filter(course=instance.course)
    for sub in subscribes:
        stu = sub.student
        try:
            _ = HomeworkStatus.objects.get(student=stu, homework=instance)
        except:
            hws = HomeworkStatus(student=stu, homework=instance)
            if getattr(instance, 'force_now', False):
                hws.force_now = True
            hws.save()
