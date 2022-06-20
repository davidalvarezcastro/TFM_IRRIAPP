from src.model.model import Usuarios


class DAOUser():

    @staticmethod
    def get_users():
        return Usuarios.select()

    @staticmethod
    def get_user_by_email(email):
        return Usuarios.get(Usuarios.email == email)

    @staticmethod
    def get_user_by_id(user_id):
        return Usuarios.get(Usuarios.id_user == user_id)

    @staticmethod
    def get_user_by_username(user_id):
        return Usuarios.get(Usuarios.username == user_id)

    @staticmethod
    def delete_user_by_username(user_id):
        try:
            # es necesario eliminar los tokens asociados
            user = Usuarios.get(Usuarios.username == user_id)
            user.delete_instance()
        except Exception:
            pass
