from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.database import get_db
from app.models import Usuario


router = APIRouter(
    prefix="/login",
    tags=["Autenticación"]
)


class LoginRequest(BaseModel):
    correo: EmailStr
    contraseña: str


@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    try:
    
        usuario = (
            db.query(Usuario)
            .filter(Usuario.correo == credentials.correo)
            .first()
        )

        if not usuario:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

  
        if usuario.contrasena != credentials.contraseña:
            raise HTTPException(
                status_code=401,
                detail="Correo o contraseña incorrectos."
            )

      
        if not usuario.estado:
            raise HTTPException(
                status_code=403,
                detail="El usuario se encuentra inactivo."
            )

        # Identificar rol
        if usuario.id_rol not in [1, 2, 3, 4]:
            raise HTTPException(
                status_code=403,
                detail="El usuario no tiene un rol válido."
            )

        # Respuesta
        return {
            "success": True,
            "mensaje": "Inicio de sesión exitoso",
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "correo": usuario.correo,
                "id_rol": usuario.id_rol,
                "estado": usuario.estado
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
