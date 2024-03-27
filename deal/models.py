from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class Deal(models.Model):
    name = models.CharField(max_length=100)
    item_count = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    item_sold = models.IntegerField(default=0, validators=[MinValueValidator(1)])
    deal_price = models.DecimalField(default=0, decimal_places=2, max_digits=99999)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.user', on_delete=models.CASCADE)

    def is_active(self):
        return self.active and self.start_time <= timezone.now() <= self.end_time and self.item_sold < self.item_count


class Claim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'deal')

# one to one
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# one to many
# @receiver(post_save, sender=Book)
# def update_author_metadata(sender, instance, created, **kwargs):
#     if created:
#         author = instance.author
#         author.total_books += 1
#         author.save()

# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver

# many to many
# @receiver(m2m_changed, sender=Student.courses.through)
# def update_enrollment_counts(sender, instance, action, reverse, pk_set, **kwargs):
#     if action == 'post_add':
#         if not reverse:
#             # Adding courses to a student
#             instance.courses_count += len(pk_set)
#             instance.save()
#             Course.objects.filter(pk__in=pk_set).update(enrollment_count=models.F('enrollment_count') + 1)
#         else:
#             # Adding students to a course
#             instance.enrollment_count += len(pk_set)
#             instance.save()
#             Student.objects.filter(pk__in=pk_set).update(courses_count=models.F('courses_count') + 1)
#
#     elif action == 'post_remove':
#         if not reverse:
#             # Removing courses from a student
#             instance.courses_count -= len(pk_set)
#             instance.save()
#             Course.objects.filter(pk__in=pk_set).update(enrollment_count=models.F('enrollment_count') - 1)
#         else:
#             # Removing students from a course
#             instance.enrollment_count -= len(pk_set)
#             instance.save()
#             Student.objects.filter(pk__in=pk_set).update(courses_count=models.F('courses_count') - 1)

# reverse indicates the direction of the change.
# If True, it means the operation was performed from the Course side (e.g., adding students to a course).
# If False, the operation was performed from the Student side (e.g., a student enrolling in courses).
# pk_set contains the primary key(s) of the related objects being added or removed.
