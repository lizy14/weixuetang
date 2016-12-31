from django.db import models
from homework.models import *
from django.db.models.signals import post_save
from django.dispatch import receiver


class Notice(models.Model):
    course = models.ForeignKey(Course)
    xt_id = models.CharField(max_length=32, default=None)
    title = models.TextField()
    content = models.TextField()
    publisher = models.CharField(max_length=32)
    publishtime = models.DateField()


class NoticeStatus(models.Model):
    notice = models.ForeignKey(Notice)
    student = models.ForeignKey(Student)
    read = models.BooleanField(default=False)


from wechat.tasks import send_template

ignore_prefix = [
    '文化素质教育讲座',
    '实验室科研探究'
]


@receiver(post_save, sender=Notice)
def create_status(sender, instance, **kwargs):
    try:
        ns, created = NoticeStatus.objects.get_or_create(
            notice=instance,
            student=instance._student,
        )
        for prefix in ignore_prefix:
            if instance.course.name.startswith(prefix):
                return
        if created and instance._student.pref.s_notice and not instance._student.flushing:
            send_template(instance._student.open_id, ns.notice)
    except:
        pass
