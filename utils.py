import hashlib
import uuid
import json
from tabulate import tabulate

class Roles:
	class Admin:
		def change_user(login, user_data):
			users = UserWorking.get_users()
			users[login] = user_data
			UserWorking.update_users(users)

		def show_users():
			users = UserWorking.get_users()
			data = [(i, users[i]['password'], users[i]['role']) for i in users]
			headers = ["Login", "Password", "Role"]
			Usefull.show_grid(data, headers)

		def get_changing_data(login):
			user = UserWorking.get_user(login)
			if not user: return
			new_password = input("Новый пароль: ")
			new_role = Usefull.get_integer("Новая роль: ")
			new_password, salt = Usefull.passwd_gen(new_password)
			user = {'salt':salt, 'role':new_role, 'password':new_password}
			Roles.Admin.change_user(login, user)

class Usefull:
	def get_integer(value):
		try:
			return int(input(value))
		except Exception as e:
			print(f"Ошибка ввода: {e}")
			return Usefull.get_integer(value)
	def show_grid(data, headers):
		print(tabulate(data,headers,tablefmt="grid"))

	def passwd_gen(value, salt=None):
		if not salt:
			salt = uuid.uuid4().hex
		result = hashlib.sha256(value.encode() + salt.encode()).hexdigest()
		return (result, salt)
class UserWorking:
	def get_user(login):
		users = UserWorking.get_users()
		if login not in users:
			print("Login doesnt exists")
			return False
		else:
			return users[login]
	def get_users():
		with open('users.json') as f:
			return json.loads(f.read())

	def update_users(data):
		with open('users.json', 'w') as f:
			f.write(json.dumps(data))



class Auth:
	def registration(login, password):
		users = UserWorking.get_users()
		if login in users:
			print("Login already exists")
			return False

		password, salt = Usefull.passwd_gen(password)
		users[login] = {'password':password, 'salt':salt, 'role':0}
		UserWorking.update_users(users)
		return (login, users[login]['role'])

	def login(login, password):
		users = UserWorking.get_users()
		if login not in users:
			print("Login doesnt exists")
			return False
		salt = users[login]['salt']
		hash_passwd, salt = Usefull.passwd_gen(password, salt)
		if users[login]['password'] != hash_passwd:
			print("Invalid password")
			return False
		else:
			return (login, users[login]['role'])

