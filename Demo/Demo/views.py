from django.http import HttpResponse
import datetime
from django.shortcuts import render,render_to_response
from Article.models import *
from django.core.paginator import Paginator
# def index(request):
#     s=datetime.datetime.now()
#     return HttpResponse(str(s))
"""
视图：作用
:param request:  形参 包含请求信息的请求对象
:return:    HttpResponse  响应对象
"""
from django.template.loader import get_template
from django.shortcuts import render_to_response
def index(request):
    ## 返回数据
    ## 1、 返回6条文章数据   排序  按照时间逆序
    article = Article.objects.order_by("-date")[:6]
    ##
    # one = article[0]
    # print(one)
    # print(one.author)
    # print(one.type.first())
    ## 2、 返回图文推荐文章内容  7条
    # ##  图文推荐： 获取到推荐的文章   数据库中应该有推荐的字段 标识
    recommend_article = Article.objects.filter(recommend=1).order_by("-date")[:7]
    # ## 3、 点击排行12条内容
    # ## 有点击率
    # ##  按照点击率进行逆序
    click_article = Article.objects.order_by("-click")[:12]

    return render_to_response("index.html", locals())




def base(request):
    return render_to_response("base.html")
def about(request):
    return render_to_response("about.html")
def listpic(request):
    return render_to_response("listpic.html")
# 文章详情

def articleinfo(request,id):
    # 文章的标识，使用id

    article = Article.objects.get(id=id)
    # 每次触发这个视图点击率+1
    article.click+=1
    article.save()


    return render_to_response("articleinfo.html",locals())


def newslistpic(request,page):
    # 查询文章
    article=Article.objects.all() #返回的是一个queryset
    pagnitor_obj=Paginator(article,6)
    page_obj=pagnitor_obj.page(page)
    # 通过遍历 pagnitor_obj.page_range->range(1,11)
    # 解决 页码数量太多
    # 获取当前页码，然后生成start和end
    page_num=page_obj.number
    # start
    start=page_num-2
    if start<=2:
        start=1
        end=start+5
    # end
    else:
        end=page_num+3
        if end>=pagnitor_obj.num_pages:
            end=pagnitor_obj.num_pages+1
            start=end-5
    page_range=range(start,end)
    # 根据类型对数据进行查询
    # 获取类型
    article_type=request.GET.get("type")
    print(article_type)
    # 根据类型查询到该类型下的文章，将文章返回

    return render_to_response("newslistpic.html",locals())

# 增加多条数据
def add_article(request):
    for i in range(100):
        article=Article()
        article.title="title_%s"%i
        article.content="content_%s"%i
        article.date="2020-02-18"
        article.description="description_%s"%i
        article.author=Author.objects.get(id=1)
        article.save() #在创建关系之前先保存文章数据
    #    多对多关系中的add方法
        article.type.add(Type.objects.get(id=1))
        article.save()



    return HttpResponse("add_article")

# 分页

def fy_test(request,page):
    ## 查询文章的方法
    article = Article.objects.all().order_by("id")
    # print(article)
    ## Paginator(数据集，每页展示的条数)
    paginator_obj = Paginator(article,10)
    print(paginator_obj)
    # print(paginator_obj.count)    ### 数据的总条数
    # print(paginator_obj.num_pages)   ###  总页数
	    # print(paginator_obj.page_range)   ##  range(1, 4)

    page_obj = paginator_obj.page(page)
   # print(page_obj)   #   <Page 1 of 11>
  ## 循环遍历  得到分页之后的数据
    for one in page_obj:
        print(one)
    # print(page_obj.has_next())    ## 是否有下一页  True  False
    # print(page_obj.has_previous())    ## 是否有上一页  True  False
    # print(page_obj.number)    ## 返回当前所在的页码
    # print(page_obj.previous_page_number())   ## 上一页的页码
    # print(page_obj.next_page_number())     ## 下一页的页码
    # print(page_obj.has_other_pages())   ## 是否有其他的页

    return HttpResponse("fy test")

# 请求方式
def request_demo(request):
    # 学习请求提供的方法
    # print(dir(request))
# ['COOKIES', 'FILES', 'GET', 'META', 'POST', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_current_scheme_host', '_encoding', '_get_full_path', '_get_post', '_get_raw_host', '_get_scheme', '_initialize_handlers', '_load_post_and_files', '_mark_post_parse_error', '_messages', '_read_started', '_set_post', '_stream', '_upload_handlers', 'body', 'build_absolute_uri', 'close', 'content_params', 'content_type', 'csrf_processing_done', 'encoding', 'environ', 'get_full_path', 'get_full_path_info', 'get_host', 'get_port', 'get_raw_uri', 'get_signed_cookie', 'headers', 'is_ajax', 'is_secure', 'method', 'parse_file_upload', 'path', 'path_info', 'read', 'readline', 'readlines', 'resolver_match', 'scheme', 'session', 'upload_handlers', 'user', 'xreadlines']
#     print(request.COOKIES)  ##标识用户的身份
#     print(request.FILES)  ##上传的文件，例如图片文档
    #GET get请求传递的参数
    name=request.GET.get("name")
    age=request.GET.get("age")
    print(name)
    print(age)


    return HttpResponse('request demo')