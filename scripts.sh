alias pm='python manage.py'
# winows 用户：在 cmd 下
# doskey pm=python manage.py $*



# 向 CamusAPI 注册学生
echo "u='lizy14'; p='575520E7BC76'; import ztylearn; ztylearn.Util.register(u,p)" | pm shell

# 向数据库插入学生
echo "u='lizy14'; from userpage.models import *;Student.objects.get_or_create(xt_id=u);" | pm shell

# 运行爬虫
echo "import WeLearn.tasks as t; t.main()" | pm shell
# 通过 celery 运行：
# pm celery worker -B -l debug

# 重置数据库
echo yes | pm reset_db

# 重新 makemigrations
rm userpage/migrations/ -rf
rm homework/migrations/ -rf
rm wechat/migrations/ -rf
rm notice/migrations/ -rf
rm calendar_/migrations/ -rf
pm makemigrations userpage homework wechat notice calendar_
pm migrate
