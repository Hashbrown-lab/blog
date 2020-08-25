from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from article.models import Article, Comment
from article.forms import ArticleForm
# Create your views here.
def article(request):
    '''
    Render the article page
    '''
    articles = {article:Comment.objects.filter(article=article) for article in Article.objects.all()}
    context = {'articles':articles}
    return render(request, 'article/article.html', context)

def articleCreate(request):
    '''
    Create a new article instance
        1. If method is GET, render an empty form
        2. If method is POST,
            * validate the form and display error messages if the form is invalid
            * else, save it to the model and redirect to the article page
    '''
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        return render(request, template, {'articleForm':ArticleForm()})
    
    # POST
    articleForm = ArticleForm(request.POST)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})
    
    articleForm.save()
    messages.success(request, 'Added successfully')
    return redirect('article:article')

def articleRead(request, articleId):
    '''
    Read an article
        1. Get the article instance; redirect to the 404 page if not found
        2. Render the articleRead template with the article instance and its associate comments
    '''
    article = get_object_or_404(Article, id=articleId)
    context = {
        'article': article,
        'comments': Comment.objects.filter(article=article)
    }
    return render(request, 'article/articleRead.html', context)

def articleUpdate(request, articleId):
    '''
    Update the article instance:
        1. Get the article to update; redirect to 404 if not found
        2. If method is GET, render a bound form
        3. If method is POST,
            * validate the form and render a bound form if the form is invalid
            * else, save it to the model and redirect to the articleRead page
    '''
    article = get_object_or_404(Article, id=articleId)
    template = 'article/articleCreateUpdate.html'
    if request.method == 'GET':
        articleForm = ArticleForm(instance=article)
        return render(request, template, {'articleForm':articleForm})
    
    #POST
    articleForm = ArticleForm(request.POST, instance=article)
    if not articleForm.is_valid():
        return render(request, template, {'articleForm':articleForm})
    
    articleForm.save()
    messages.success(request, 'Edited Successfully')
    return redirect('article:articleRead', articleId=articleId)

def articleDelete(request, articleId):
    '''
    Delete the article instance:
        1. Render the article page if the method is GET
        2. Get the article to delete; render to 404 if not found 
    '''
    if request.method == 'GET':
        return redirect('article:article')
    
    #POST
    article = get_object_or_404(Article, id=articleId)
    article.delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('article:article')

def articleLike(request, articleId):
    '''
    Add the user to the 'likes' field:
        1. Get the article; redirect to 404 if not found
        2. IF the user does not exist in the "likes" field, add him/her
        3. Finally,call articleRead() function to render the article
    '''
    article = get_object_or_404(Article, id=articleId)
    if request.user not in article.likes.all():
        article.likes.add(request.user)
    else:
        article.likes.remove(request.user)
    return articleRead(request, articleId)

def commentCreate(request, articleId):
    '''
    Create a comment for an article:
        1. Get the "comment" from the HTML form
        2. Store it to database
    '''
    if request.method == 'GET':
        return articleRead(request, articleId)
    
    #POST
    comment = request.POST.get('comment')
    if comment:
        comment = comment.strip()
    if not comment:
        return redirect('article:articleRead', articleId=articleId)
    
    article = get_object_or_404(Article, id=articleId)
    Comment.objects.create(article=article, user=request.user, content=comment)
    return redirect('article:articleRead', articleId=articleId)

def commentUpdate(request, commentId):
    '''
    Update a comment:
        1. Get the comment to update and its article; redirect to 404 if not found
        2. If it is a 'GET' request, return
        3. If the comment's author is not the user. return 
        4. If comment is empty, delete the comment, else update the comment
    '''
    commentToUpdate = get_object_or_404(Comment, id=commentId)
    article = get_object_or_404(Article, id=commentToUpdate.article.id)
    if request.method == 'GET':
        return articleRead(request, article.id)
    
    #POST
    if commentToUpdate.user != request.user:
        messages.error(request, 'Permission denied')
        return redirect('article:articleRead', articleId=article.id)
    
    comment = request.POST.get('comment', '').strip()
    if not comment:
        commentToUpdate.delete()
    else:
        commentToUpdate.content = comment
        commentToUpdate.save()
    return redirect('article:articleRead', articleId=article.id)
    