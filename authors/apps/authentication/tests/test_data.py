from ..models import User
USER = {
    "email": "johndoe@email.com",
    "username": "johndoe",
    "password": "johndoe.T5",
}


def generate_test_data():
    """ method to generate test data """
    user = User.objects.create_user(
        USER["username"],
        USER["email"],
        USER["password"]
    )
    user.save()
