from django.db import models

class LoginDetail(models.Model):
    username=models.CharField(max_length=260)
    password=models.CharField(max_length=20)
    

class UserDetail(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    birthdate=models.DateField()
    gender=models.CharField(max_length=50)
    user=models.ForeignKey(LoginDetail,on_delete=models.CASCADE)

class ProfilePic(models.Model):
    ProfilePic=models.FileField(upload_to='profilepicture/')
    fk_user=models.ForeignKey(LoginDetail,on_delete=models.CASCADE)

class Friends(models.Model):
    sender_id=models.ForeignKey(LoginDetail, on_delete=models.CASCADE,related_name='sender')
    reciever_id=models.ForeignKey(LoginDetail, on_delete=models.CASCADE,related_name='reciever')
    status=models.BooleanField(default=False)
