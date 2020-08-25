from populate import base
from account.models import User


print('Creating admin account ...', end=''
      User.objects.create_superuser(username='admin', password='xxxxxxxx', email=None, fullName='Victoria Wu')
print('done')