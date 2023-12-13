from httpx import AsyncClient


# Тест на подписку на пользователя
async def test_follow_user(client: AsyncClient):
    header = {"api-key": "token_2"}
    following_id = 1

    # Аутентификация как фоловер
    response = await client.post(url=f"/api/users/{following_id}/follow", headers=header)
    assert response.status_code == 200
    assert response.json()["result"] is True


# Тест на отписку от пользователя
async def test_unfollow_user(client: AsyncClient):
    header = {"api-key": "token_2"}
    following_id = 1

    # Аутентификация как фоловер
    response = await client.post(url=f"/api/users/{following_id}/follow", headers=header)

    # Отписка как фоловер
    response = await client.delete(url=f"/api/users/{following_id}/follow", headers=header)
    assert response.status_code == 200
    assert response.json()["result"] is True
