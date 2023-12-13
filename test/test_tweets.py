from httpx import AsyncClient


async def test_create_tweet(client: AsyncClient):
    header = {"api-key": "token_1"}

    # Создаем новый твит
    tweet_data = {"tweet_data": "Test tweet"}
    response = await client.post(url="/api/tweets", json=tweet_data, headers=header)
    assert response.status_code == 200

    # Проверяем, что результат содержит ожидаемые данные
    result = response.json()
    assert result["result"] is True
    assert "tweet_id" in result


async def test_delete_tweet(client: AsyncClient):
    header = {"api-key": "token_1"}

    # Создаем новый твит (чтобы получить его ID)
    tweet_data = {"tweet_data": "Test tweet"}
    create_response = await client.post(url="/api/tweets", json=tweet_data, headers=header)
    tweet_id = create_response.json()["tweet_id"]

    # Удаляем созданный твит
    response = await client.delete(url=f"/api/tweets/{tweet_id}", headers=header)
    assert response.status_code == 200

    # Проверяем, что результат содержит ожидаемые данные
    result = response.json()
    assert result["result"] is True


async def test_get_tweets(client: AsyncClient):
    header = {"api-key": "token_1"}

    # Получаем ленту твитов
    response = await client.get(url="/api/tweets", headers=header)
    assert response.status_code == 200

    # Проверяем, что результат содержит ожидаемые данные
    result = response.json()
    assert result["result"] is True
    assert "tweets" in result
    assert isinstance(result["tweets"], list)
