from django.db import models


# Create your models here.
# 抽象表(基表)
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)  # is_delete用来决定数据是否显示(删除后为True)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True  # 声明此字段后数据库不在为此表创建对应的表结构


class Book(BaseModel):
    book_name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")
    author = models.ManyToManyField(to="Author")
    publish = models.ForeignKey(to="Press", on_delete=models.CASCADE)

    class Meta:
        db_table = "t_book"
        verbose_name_plural = "书籍表"

    def __str__(self):
        return self.book_name

    # 在models中定义自定义字段，然后在序列化字段中添加(替换)
    # @property
    # def press_name(self):
    #     return self.publish.press_name
    #
    # @property
    # def author_name(self):
    #     return self.author.values("author_name", "age", "authordetail__mobile")


class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")
    age = models.SmallIntegerField()

    class Meta:
        db_table = "t_author"
        verbose_name_plural = "作者表"

    def __str__(self):
        return self.author_name


class Press(BaseModel):
    press_name = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    pic = models.ImageField(upload_to="img", default="img/1.jpg")

    class Meta:
        db_table = "t_press"
        verbose_name_plural = "出版社表"

    def __str__(self):
        return self.press_name


class AuthorDetail(BaseModel):
    author = models.ForeignKey(to="Author", on_delete=models.CASCADE)
    mobile = models.IntegerField()
    address = models.CharField(max_length=128)

    class Meta:
        db_table = "t_userdetail"
        verbose_name_plural = "作者详情表"

    def __str__(self):
        return "%s的详情" % self.author.author_name
