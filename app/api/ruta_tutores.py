
from fastapi import APIRouter, HTTPException
from app.models.tutores import Usuario
from app.repositories.tutores_repo import TutoresRepository

router = APIRouter(
    prefix="/tutores",
    tags=["Gestión de tutores"]
)

repo = TutoresRepository()


@router.get("/")
def listar_tutores():
    try:
        return repo.obtener_todos()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{id_tutor}")
def obtener_tutor(id_tutor: int):
    try:
        if id_tutor <= 0:
            raise HTTPException(
                status_code=400,
                detail="El ID del tutor debe ser mayor que cero"
            )

        tutor = repo.obtener_por_id(id_tutor)

        if tutor is None:
            raise HTTPException(
                status_code=404,
                detail="Tutor no encontrado"
            )

        return tutor

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/", status_code=201)
def crear_tutor(tutor: Usuario):
    try:
        if tutor.id_tutor is None:
            raise HTTPException(
                status_code=400,
                detail="Debes indicar el ID de un usuario existente para registrar su perfil de tutor"
            )

        nuevo_id = repo.crear(tutor)

        return {
            "mensaje": "Tutor registrado exitosamente",
            "id": nuevo_id
        }

    except HTTPException:
        raise

    except Exception as e:
        mensaje = str(e).lower()

        if "foreign key" in mensaje or "foreignkey" in mensaje:
            raise HTTPException(
                status_code=400,
                detail="El usuario indicado no existe"
            )

        if "duplicate key" in mensaje or "unique constraint" in mensaje:
            raise HTTPException(
                status_code=409,
                detail="Ya existe un perfil de tutor con ese identificador"
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.put("/{id_tutor}")
def actualizar_tutor(id_tutor: int, tutor: Usuario):
    try:
        if id_tutor <= 0:
            raise HTTPException(
                status_code=400,
                detail="El ID del tutor debe ser mayor que cero"
            )

        exito = repo.actualizar(id_tutor, tutor)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Tutor no encontrado"
            )

        return {
            "mensaje": "Tutor actualizado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/{id_tutor}")
def eliminar_tutor(id_tutor: int):
    try:
        if id_tutor <= 0:
            raise HTTPException(
                status_code=400,
                detail="El ID del tutor debe ser mayor que cero"
            )

        exito = repo.eliminar(id_tutor)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Tutor no encontrado"
            )

        return {
            "mensaje": "Tutor eliminado correctamente"
        }

    except HTTPException:
        raise

    except Exception as e:
        mensaje = str(e).lower()

        if "foreign key" in mensaje or "foreignkey" in mensaje:
            raise HTTPException(
                status_code=409,
                detail="No se puede eliminar el tutor porque tiene prácticas relacionadas"
            )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
