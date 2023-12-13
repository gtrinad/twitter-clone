import os
import uuid

from fastapi import APIRouter, Depends, UploadFile, File, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app_fast.CRUD.users_crud import get_current_user_by_api_key
from app_fast.db_and_models.models import Images, User
from app_fast.db_and_models.schemas import ImagesResponse
from app_fast.db_and_models.session import get_async_session

router = APIRouter(tags=["Media"])


@router.post("/medias", response_model=ImagesResponse)
async def upload_media(
    request: Request,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user_by_api_key),
):
    # Создаём директорию для пользователя, если она не существует
    user_media_dir = os.path.join("images", str(current_user.id))
    os.makedirs(user_media_dir, exist_ok=True)

    # Сохраняем изображение в директорию пользователя
    file_extension = file.filename.split(".")[-1]
    image_name = str(uuid.uuid4())
    image_filename = f"{image_name}.{file_extension}"
    image_path = os.path.join(user_media_dir, image_filename)

    # Сохранение загруженного файла в файловой системе
    with open(image_path, "wb") as image_file:
        image_file.write(file.file.read())

    # Создайте запись в базе данных с путем к изображению
    new_image = Images(url=image_path)

    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)

    return {"result": True, "media_id": new_image.id}
