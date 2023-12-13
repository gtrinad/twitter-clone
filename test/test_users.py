from httpx import AsyncClient


async def test_get_current_user(client: AsyncClient):
    header = {"api-key": "token_1"}

    response = await client.get(url=f"/api/users/me", headers=header)

    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response.json()["user"]["name"] == "name_1"


async def test_get_user_by_id(client: AsyncClient):
    response = await client.get(url="/api/users/2")

    assert response.status_code == 200
    assert response.json()["result"] is True
    assert response.json()["user"]["name"] == "name_2"
