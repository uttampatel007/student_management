from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

class CustomUser(AbstractUser):
	user_type_data=((1,"HOD"),(2,"Staffs"),(3,"Student"))
	user_type=models.CharField(default=1,choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
	id = models.AutoField(primary_key=True)
	admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class Staffs(models.Model):
	id = models.AutoField(primary_key=True)
	admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
	gender=models.CharField(max_length=20)
	profile_pic=models.FileField()
	address=models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()


class Courses(models.Model):
	id=models.AutoField(primary_key=True)
	course_name=models.CharField(max_length=20)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class Subjects(models.Model):
	id=models.AutoField(primary_key=True)
	subject_name=models.CharField(max_length=20)
	course_id=models.ForeignKey(Courses, on_delete=models.CASCADE)
	staff_id=models.ForeignKey(Staffs, on_delete=models.CASCADE)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class Students(models.Model):
	id = models.AutoField(primary_key=True)
	admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
	gender=models.CharField(max_length=20)
	profile_pic=models.FileField()
	address=models.TextField()
	course_id=models.ForeignKey(Courses, on_delete=models.CASCADE)
	session_start_year=models.DateField()
	session_end_year=models.DateField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class Attendance(models.Model):
	id = models.AutoField(primary_key=True)
	subject_id=models.ForeignKey(Subjects, on_delete=models.CASCADE)
	attendance_date=models.DateTimeField(auto_now_add=True)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class AttendanceReport(models.Model):
	id = models.AutoField(primary_key=True)
	subject_id=models.ForeignKey(Subjects, on_delete=models.CASCADE)
	attendance_id=models.ForeignKey(Attendance, on_delete=models.CASCADE)
	status=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class LeaveReportStudent(models.Model):
	id=models.AutoField(primary_key=True)
	student_id=models.ForeignKey(Subjects, on_delete=models.CASCADE)
	leave_date=models.CharField(max_length=25)
	leave_message=models.TextField()
	leave_status=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class LeaveReportStaffs(models.Model):
	id=models.AutoField(primary_key=True)
	staff_id=models.ForeignKey(Staffs, on_delete=models.CASCADE)
	leave_date=models.CharField(max_length=25)
	leave_message=models.TextField()
	leave_status=models.BooleanField(default=False)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class FeedbackStudent(models.Model):
	id=models.AutoField(primary_key=True)
	student_id=models.ForeignKey(Subjects, on_delete=models.CASCADE)
	feedback=models.TextField()
	feedback_reply=models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class FeedbackStaffs(models.Model):
	id=models.AutoField(primary_key=True)
	staff_id=models.ForeignKey(Staffs, on_delete=models.CASCADE)
	feedback=models.TextField()
	feedback_reply=models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()


class NotificationStudent(models.Model):
	id=models.AutoField(primary_key=True)
	student_id=models.ForeignKey(Subjects, on_delete=models.CASCADE)
	message=models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()

class NotificationStaffs(models.Model):
	id=models.AutoField(primary_key=True)
	staff_id=models.ForeignKey(Staffs, on_delete=models.CASCADE)
	message=models.TextField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects=models.Manager()


# django signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
	if created:
		if instance.user_type==1:
			AdminHOD.objects.create(admin=instance)
		if instance.user_type==2:
			Staffs.objects.create(admin=instance)
		if instance.user_type==3:
			Students.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance,created,**kwargs):
	if instance.user_type==1:
		instance.adminhod.save()
	if instance.user_type==2:
		instance.staffs.save()
	if instance.user_type==3:
		instance.students.save()
		

		
