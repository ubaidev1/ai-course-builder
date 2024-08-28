from users.models import User


def create_admin():
    """
    Takes email, password, first name and last name as input and created user with  admin =True by default.
    """
    email = input("Enter email: ")
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    password = input("Enter Password: ")

    user = User.objects.create_superuser(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    print("Admin created successfully !")
    return user
