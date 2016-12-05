# create new user
echo "u='lizy14'; p='i_love_ruangong'; from userpage.models import Student;Student.objects.get_or_create(xt_id=u);import ztylearn; ztylearn.Util.register(u,p)" | python manage.py shell

# run background update task
echo "import WeLearn.tasks as t; t.main()" | python manage.py shell
