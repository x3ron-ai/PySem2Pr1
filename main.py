from utils import Auth, Usefull, Roles

auth_method = Usefull.get_integer("Выбор действия:\n1. Авторизация\n2. Регистрация\n: ")

if auth_method == 1:
	login = input("Логин: ")
	passwd = input("Пароль: ")
	user = Auth.login(login, passwd)
	if not user:
		exit()
else:
	login = input("Логин: ")
	passwd = input("Пароль: ")
	r_passwd = input("Повтор пароля: ")
	if passwd != r_passwd:
		print("Пароли не совпадают")
		exit()
	user = Auth.registration(login, passwd)
	if not user:
		exit()

login, role = user
if role == 0:
	print("Вы вошли в личный кабинет покупателя. Скоро здесь появится функционал для данной роли пользователя")
	exit()
elif role == 1:
	print("Вы вошли в личный кабинет продавца. Скоро здесь появится функционал для данной роли пользователя")
	exit()
else:
	role_funcs = Roles.Admin
	while True:
		role_funcs.show_users()
		edit_login = input("Редактируемый логин: ")
		role_funcs.get_changing_data(login)