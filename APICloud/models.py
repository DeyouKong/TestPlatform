from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserInfo(AbstractUser):
    __doc__ = "用户表"
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11,null=True,unique=True,verbose_name="手机号")  # 文章标题，verbose_name 设置在admin中的别名)
    # upload_to 前段传送过来的文件都保存在这个文件夹，如果不存在，自动创建
    avatar = models.FileField(upload_to="avatars/",default="avatars/default.png")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.username

    class Meta:
        # 设置在 admin 后台管理中，表的别名
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        # 如果无此设置，当数量为多个时，显示为 "用户s"

class Sign(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "签名"
        verbose_name_plural = verbose_name

class Project(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    sign = models.ForeignKey('Sign', on_delete=models.CASCADE)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目"
        verbose_name_plural = verbose_name

class Environment(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.CharField(max_length=100,null=True)
    url = models.CharField(max_length=100)
    private_key = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试环境"
        verbose_name_plural = verbose_name

class Interface(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=50)
    method = models.CharField(max_length=4)
    data_type = models.CharField(max_length=4)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_sign = models.IntegerField()
    description = models.CharField(max_length=100, null=True)
    request_header_param = models.TextField()
    request_body_param = models.TextField()
    response_header_param = models.TextField()
    response_body_param = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "接口"
        verbose_name_plural = verbose_name

class Case(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用例"
        verbose_name_plural = verbose_name

class Plan(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    environment = models.ForeignKey('Environment', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试计划"
        verbose_name_plural = verbose_name

class Report(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=255)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    content = models.TextField()
    case_num = models.IntegerField(null=True)
    pass_num = models.IntegerField(null=True)
    fail_num = models.IntegerField(null=True)
    error_num = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name