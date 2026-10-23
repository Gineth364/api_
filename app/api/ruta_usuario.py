
from fastapi import APIRouter, HTTPException
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepository
import psycopg2


router = APIRouter(
    prefix="/usuarios",
    tags=["Gestión de usuarios"]
)

repo = UsuarioRepository()


@router.get("/")
def listar_usuarios():
    try:
        return repo.obtener_todos()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{id_usuario}")
def obtener_usuario(id_usuario: int):
    try:
        usuario = repo.obtener_por_id(id_usuario)

        if usuario is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return usuario

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/", status_code=201)
def crear_usuario(usuario: Usuario):
    try:
        nuevo_id = repo.crear(usuario)

        return {
            "mensaje": "Usuario registrado exitosamente",
            "id": nuevo_id
        }

    except psycopg2.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un registro con uno de los valores únicos."
        )

    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=400,
            detail="El rol indicado no existe."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.put("/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario: Usuario):
    try:
        exito = repo.actualizar(id_usuario, usuario)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "mensaje": "Usuario actualizado correctamente"
        }

    except HTTPException:
        raise

    except psycopg2.errors.UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Ya existe otro registro con uno de los valores únicos."
        )

    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=400,
            detail="La operación hace referencia a un registro que no existe."
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    try:
        exito = repo.eliminar(id_usuario)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        return {
            "mensaje": "Usuario eliminado correctamente"
        }

    except HTTPException:
        raise

    except psycopg2.errors.ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail=(
                "No se puede eliminar el usuario porque está relacionado "
                "con otros registros. Elimina o reasigna esas relaciones primero."
            )
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
