from django.db import models
from ckeditor.fields import RichTextField
## RichTextField   底层是 TextField  只是修改前端的样式，能够将输入的内容以html的格式进行重新排版
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
# 作者
GENDER_STATUS=(
    (0,"女"),
    (1,"男")

)

class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, verbose_name="作者姓名")
    gender = models.CharField(max_length=32, verbose_name="性别")  #男或者女
    gender = models.IntegerField(choices=GENDER_STATUS,verbose_name="性别") #0代表女，1代表男
    age = models.IntegerField(verbose_name="年龄")
    email = models.CharField(max_length=32, verbose_name="邮箱")
    class Meta:
        db_table="author"

    def __str__(self):
        return self.name

# 类型表
class Type(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=32,verbose_name="类型名字")
    description = models.TextField(verbose_name="类型描述")
    class Meta:
        db_table="type"

    def __str__(self):
        return self.name

# 文章
class Article(models.Model):
    # django的orm会自动创建一个id主键
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=32,verbose_name="标题")
    date=models.DateField(verbose_name="创建时间") #auto_now=Ture
    content=RichTextField(verbose_name="文章内容")
    description=RichTextField(verbose_name="文章描述")
    # content=models.TextField(verbose_name="文章内容")
    # description=models.TextField(verbose_name="文章描述")
    # 由方法upload_to决定了图片上传的路径static/images/
    # upload_to 当images目录存在的时候，直接将图片上床到images目录下
    # 当 images目录不存在的时候，会先创建images目录并且完成图片的上传
    picture=models.ImageField(upload_to="images",verbose_name="图片")
    recommend=models.IntegerField(default=0,verbose_name="文章推荐") ##1代表推荐，0代表不推荐
    click=models.IntegerField(default=0,verbose_name="文章点击率")  #按照点击率进行逆序排序

    author=models.ForeignKey(to=Author,to_field="id",on_delete=models.CASCADE)
    type=models.ManyToManyField(to=Type)
    class Meta:
        db_table="article"

    def __str__(self):
        return self.title
