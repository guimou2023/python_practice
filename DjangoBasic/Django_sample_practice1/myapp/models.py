from django.db import models

# Create your models here.


# admin_db
class UserType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Users(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    ut = models.ForeignKey(to='UserType', to_field='id', limit_choices_to={'id__gt': 1})
    # ut = models.ForeignKey(to='UserType', to_field='id', limit_choices_to={'id__gt': 5})

    def __str__(self):
        return self.user


class UserGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)


class UserInfo(models.Model):

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=32, error_messages={'required': "不能为空.", 'invalid': '格式错误'}, null=True)
    user_group = models.ForeignKey(to='UserGroup', to_field='uid', default=1)

    user_type_choices = (
        (1, '超级用户'),
        (2, '普通用户'),
        (3, '垃圾用户')
    )
    user_type_id = models.IntegerField(choices=user_type_choices, default=1)



class UserInfo1(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)


# class Blog(models.Model):
#     blog_name = models.CharField(max_length=32)
#     m = models.ManyToManyField('Tag', through='B2T', through_fields=['b', 't1'])
#
#
# class Tag(models.Model):
#     tag_name = models.CharField(max_length=32)
#
# class B2T(models.Model):
#     b = models.ForeignKey('Blog')
#     t1 = models.ForeignKey('Tag')
#     t2 = models.ForeignKey('Tag')




# mocdelfrom 练习

class FuserType(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class DepartmentGroup(models.Model):
    name = models.CharField(max_length=32, unique=True)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Fstaff(models.Model):
    staff_name = models.CharField(max_length=32)
    gender = models.CharField(max_length=32)
    staff_type = models.ForeignKey(to='FuserType', to_field='id', limit_choices_to={'id__gte': 1})
    u2g = models.ManyToManyField(DepartmentGroup)
    def __str__(self):
        return self.staff_name


