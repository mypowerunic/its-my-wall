from django.shortcuts import render,get_object_or_404
from testapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.generic import ListView
from testapp.forms import CommentForm
from taggit.models import Tag
# Create your views here.

def myfun(request,tag_slug=None):
    post=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post=post.filter(tags__in=[tag])

    paginator=Paginator(post,3)
    page_number=request.GET.get('page')
    try:
        post=paginator.page(page_number)
    except PageNotAnInteger:
        post=paginator.page(1)
    except EmptyPage:
        post=paginator.page(paginator.num_pages)
    return render(request,'testapp/post_list.html',{'post':post,'tag':tag})
# using class based views to generate pagenation
# class PostListView(ListView):
#     model=Post
#     paginate_by=3

def post_detail_view(request,year,month,day,post):
    user=request.user
    print(user)
    post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'testapp/post_detail.html',{'post':post,'form':form,'csubmit':csubmit,'comments':comments})


from django.core.mail import send_mail
from testapp.forms import Email_SendForm

def mail_send(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=Email_SendForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{}({}) recomends to u read"{}"'.format(cd['name'],cd['email'],post.title)
            message='read post at:\n {}\n\n{}\'s comments:\n{}'.format(post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'kv.prabhakararao99@gmail.com',[cd['to']])
            sent=True
            return render(request,'testapp/thnq.html',{'post':post})
    else:
        form=Email_SendForm()
    return render(request,'testapp/sharebymail.html',{'form':form,'post':post,'sent':sent})
