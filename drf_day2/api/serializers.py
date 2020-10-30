from rest_framework import serializers
from api.models import Book, Author, AuthorDetail, Press


# 自定义字段可以通过models来实现，也可以通过嵌套类
class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "address")


class AuthorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("author_name", "age")


# 整合序列化和反序列化
class BookModelSerializer2(serializers.ModelSerializer):
    # publish = PressModelSerializer() # 会报错

    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "author", "publish", "re_book_name")

        extra_kwargs = {
            "book_name": {
                "required": True,  # 必填字段
                "min_length": 2,  # 书名的最小长度
                "error_messages": {
                    "required": "图书名必须提供",
                    "min_length": "书名长度必须大于2个字符"
                }
            },
            # 指定某个字段只能参与序列化(read_only)或者只能参与反序列化(write_only)
            "pic": {
                "read_only": True  # 设置pic只能序列化
            },
            "re_book_name": {
                "write_only": True  # 设置二次书名只能反序列化
            }
        }

    # 下面时序列化和反序列化分开定义
    # class BookModelSerializer(serializers.ModelSerializer):
    #     publish = PressModelSerializer()  # 使用嵌套类来自定义字段,注意要使用外键名来做变量名
    #
    #     class Meta:
    #         # 指定当前序列化类针对哪个模型
    #         model = Book
    #         # 指定序列化字段
    #         # fields = ("book_name", "price", "pic", "author_name", "press_name") # 这种方法接收models的自定义字段
    #         fields = ("book_name", "price", "pic", "author", "publish")
    #         # 指定不展示的字段
    #         # exclude = ("is_delete","status","create_time")
    #         # 显示所有字段
    #         # fields = "__all__"
    #         # 指定查询深度
    #         # depth = 1
    #
    #
    # # 定义book类的反序列化
    # class BookDeModelSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Book
    #         # 需要反序列化的字段
    #         fields = ("book_name", "price", "publish", "author")
    #         # 添加DRF提供的默认校验规则,为每个字段单独校验
    #         extra_kwargs = {
    #             "book_name": {
    #                 "required": True,  # 必填字段
    #                 "min_length": 2,  # 书名的最小长度
    #                 "error_messages": {
    #                     "required": "图书名必须提供",
    #                     "min_length": "书名长度必须大于2个字符"
    #                 }
    #             },
    #             "price": {},
    #             "publish": {},
    #             "author": {},
    #         }

    # 使用钩子进行验证
    # 全局钩子，获取所有需要序列化的字段
    # 例用全局钩子，进行两次密码比较验证
    def validate(self, attrs):
        print(attrs)
        return attrs

    def validated_username(self, value):
        print(self, value)
        return value
