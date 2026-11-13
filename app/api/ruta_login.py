
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from app.core.database import Database

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)


class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str


@router.post("/login")
def login(credentials: LoginRequest):

    db = Database()
    conexion = db.get_connection()

    if conexion is None:
        raise HTTPException(
            status_code=503,
            detail="No fue posible conectar con la base de datos."
        )

    try:
        cursor = conexion.cursor()

        cursor.execute(
            """
            SELECT
                id_usuario,
                nombre,
                apellido,
                correo,
                id_rol,
                estado,
                contrasena
            FROM usuarios
            WHERE correo = %s
            """,
            (credentials.correo,)
        )

        usuario = cursor.fetchone()

        cursor.close()

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

        if usuario["contrasena"] != credentials.contraseña:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

        if not usuario["estado"]:
            raise HTTPException(
                status_code=403,
                detail="El usuario se encuentra inactivo."
            )

        if usuario["id_rol"] not in [1, 2, 3, 4]:
            raise HTTPException(
                status_code=403,
                detail="El usuario no tiene un rol válido."
            )

        return {
            "success": True,
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id_usuario": usuario["id_usuario"],
                "nombre": usuario["nombre"],
                "apellido": usuario["apellido"],
                "correo": usuario["correo"],
                "id_rol": usuario["id_rol"],
                "estado": usuario["estado"]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Error en autenticación:", str(e))
        raise HTTPException(
            status_code=500,
            detail="Error interno al iniciar sesión."
        )

    finally:
        conexion.close()
