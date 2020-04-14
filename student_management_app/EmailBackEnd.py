from django.contrib.auth import get_user_model

from django.contrib.auth.backends import ModelBackend


class EmailBackEnd(ModelBackend):
	def authenticate(self, username=None, password=None, **kwargs):
		UserModel=get_user_model()
		try:
			user=UserModel.objects.get(email=username)
			print("try")
			
		except UserModel.DoesNotExist:
			print("except")
			return None
		else:
			print("else")
			if user.check_password(password):
				print("user return")
				
				return user
		return None

