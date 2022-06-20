from functools import wraps

from src.dto.dto import DTOError
from src.dao.user import DAOUser
from src.model.model import Usuarios
from src.util.http_codes import Status


def requires_user(f):
    @wraps(f)
    def wrap(self, user_id, *args, **kwargs):
        try:
            user = DAOUser.get_user_by_username(user_id)

            # un usuario no activado es como un usuario inexistente
            if not user.activo:
                raise Usuarios.DoesNotExist()

        except Usuarios.DoesNotExist:
            return DTOError(status_code=Status.HTTP_404_NOT_FOUND,
                            message="Usuario no encontrado",
                            code="not_found").to_response()
        return f(self, user, *args, **kwargs)
    return wrap
