from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Book
# from api.serializers import BookModelSerializer, BookDeModelSerializer
from api.serializers import BookModelSerializer2


# Create your views here.
class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        if book_id:  # 如果有则查询单个,否则查询所有
            book = Book.objects.get(pk=book_id, is_delete=False)
            if book:
                # data = BookModelSerializer(book).data
                data = BookModelSerializer2(book).data
                print(book, data)
                return Response({
                    "status": 200,
                    "message": "查询单个书籍成功",
                    "results": data,
                })
            return Response({
                "status": 400,
                "message": "书籍不存在",
            })
        else:
            books = Book.objects.filter(is_delete=False)
            data = BookModelSerializer2(books, many=True).data
            # data = BookModelSerializer(books, many=True).data
            return Response({
                "status": 200,
                "message": "查询所有书籍成功",
                "results": data
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data  # 获取前端提交的数据,然后要通过反序列化器来存储
        # serializer = BookDeModelSerializer(data=request_data)  # 对数据进行反序列化,注意要加data关键字
        serializer = BookModelSerializer2(data=request_data)
        # 有raise_exception属性时，报错则终止程序,返回错误信息，否则继续
        serializer.is_valid(raise_exception=True)  # 对反序列化后的数据进行校验(第二次校验看数据个数是否与反序列字段是否一致)
        book_obj = serializer.save()
        return Response({
            "status": 200,
            "message": "添加书籍成功",
            # "results": BookModelSerializer(book_obj).data,
            "results": BookModelSerializer2(book_obj).data,
        })

    # 更新单个的全部内容
    def put(self, request, *args, **kwargs):
        request_data = request.data  # 接收提交的数据
        print(request_data)
        book_id = kwargs.get("id")
        try:
            book = Book.objects.get(pk=book_id)  # 将前端传的数据反序列化并进行保存(序列化保存的时候DRF会自动根据参数选择是更新还是修改)
        except:
            return Response({
                "status": 400,
                "message": "书籍不存在",
            })
        data = BookModelSerializer2(data=request_data, instance=book)  # 返回的是序列化器
        print(data)
        data.is_valid(raise_exception=True)
        data = data.save()
        print(data)  # 返回的是对象
        return Response({
            "status": 200,
            "message": "书籍修改成功",
            "results": BookModelSerializer2(data).data
        })

    # 更新单个局部内容
    def patch(self, request, *args, **kwargs):
        id = kwargs.get("id")
        request_data = request.data
        try:
            book = Book.objects.get(pk=id)
        except:
            return Response({
                "status": 200,
                "message": "书籍不存在"
            })
        data = BookModelSerializer2(data=request_data, instance=book, partial=True)
        data.is_valid(raise_exception=True)
        data = data.save()
        return Response({
            "status": 200,
            "message": "修改成功",
            "results": BookModelSerializer2(data).data
        })

    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            ids = [id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        print(response)  # response返回的是1或0，影响的数据行数
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })
        return Response({
            "status": 400,
            "message": "书籍不存在",
        })
