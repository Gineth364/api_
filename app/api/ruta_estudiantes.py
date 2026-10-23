
from fastapi import APIRouter, HTTPException
from app.models.estudiantes import Usuario
from app.repositories.estudiantes_repo import UsuarioRepository

router = APIRouter(
    prefix="/estudiantes",
    tags=["Gestión de estudiantes"]
)

repo = UsuarioRepository()


@router.get("/")
def listar_estudiantes():
    try:
        return repo.obtener_todos()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/{id_estudiante}")
def obtener_estudiante(id_estudiante: int):
    try:
        estudiante = repo.obtener_por_id(id_estudiante)

        if estudiante is None:
            raise HTTPException(
                status_code=404,
                detail="Estudiante no encontrado"
            )

        return estudiante

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/")
def crear_estudiante(estudiante: Usuario):
    try:
        nuevo_id = repo.crear(estudiante)

        if nuevo_id is None:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No se pudo registrar el estudiante. "
                    "Verifica que el usuario exista en la tabla usuarios."
                )
            )

        return {
            "mensaje": "Estudiante registrado exitosamente",
            "id": nuevo_id
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.put("/{id_estudiante}")
def actualizar_estudiante(
    id_estudiante: int,
    estudiante: Usuario
):
    try:
        exito = repo.actualizar(id_estudiante, estudiante)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Estudiante no encontrado"
            )

        return {
            "mensaje": "Estudiante actualizado correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.delete("/{id_estudiante}")
def eliminar_estudiante(id_estudiante: int):
    try:
        exito = repo.eliminar(id_estudiante)

        if not exito:
            raise HTTPException(
                status_code=404,
                detail="Estudiante no encontrado"
            )

        return {
            "mensaje": "Estudiante eliminado correctamente"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
