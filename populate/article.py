from populate import base
from account.models import User
from article.models import Article, Comment

titles = ['How to think like a Computer Scientist', 'Learn Python in 10 minutes', 'Django easy learning']
comments = ['Great article', 'Disagree', 'Share', 'It is not easy to learn a programming language']

def populate():
    print('Populating articles and comments...', end='')
    Article.objects.all() .delete()
    Comment.objects.all() .delete()
    admin = User.objects.get(is_superuser=True)
    for title in titles:
        article = Article()
        article.title = title
        for j in range(20):
            article.content += title + '\n'
        article.save()
        for comment in comments:
            Comment.objects.create(article=article, user=admin, content=comment)
    print('done')
    
if __name__ == '__main__':
    populate()