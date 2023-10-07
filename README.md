# Inforce_test_task
Test task for Inforce company.

To deploy project run:
sudo docker-compose up -d --build
sudo docker-compose exec api python manage.py makemigrations
sudo docker-compose exec api python manage.py migrate

Description:

USER_RELATED_ROUTES
Superuser must create few admins using /register
Superuser and admins can register employees using /register (to restrict self-registration of unwanted people, because it can become uncontrollable mess)
Superuser can manage restaurants & accounts of everyone(cmon, dj-admin is cool)
User (+ admins & su) can login,logout using /login & /logout
There are also can find info about themselves on / (null route) , and there also user can check related to him restaurant(if it exist)

MENU_RELATED_ROUTES /lunch
Admins with related restaurants can publish menus on /lunch/upload 
And also can see the history of menus, related to them
Admins with related restaurants can see total amount of orders & personal data of employees on /lunch/total

Employees can look on current menus list on /lunch/menus (GET) and order them by id (POST)
