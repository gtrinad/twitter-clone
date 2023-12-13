from httpx import AsyncClient


async def test_like_tweet(client: AsyncClient):
    header_for_create_tweet = {"api-key": "token_1"}
    header_for_likes = {"api-key": "token_2"}

    # Создаем новый твит (чтобы получить его ID)
    tweet_data = {"tweet_data": "Test tweet"}
    create_response = await client.post(
        url="/api/tweets", json=tweet_data, headers=header_for_create_tweet
    )
    tweet_id = create_response.json()["tweet_id"]

    # Ставим "лайк" на созданный твит
    response = await client.post(
        url=f"/api/tweets/{tweet_id}/likes", headers=header_for_likes
    )
    assert response.status_code == 200

    # Проверяем, что результат содержит ожидаемые данные
    result = response.json()
    assert result["result"] is True


async def test_unlike_tweet(client: AsyncClient):
    header_for_create_tweet = {"api-key": "token_1"}
    header_for_likes = {"api-key": "token_2"}

    # Создаем новый твит (чтобы получить его ID)
    tweet_data = {"tweet_data": "Test tweet"}
    create_response = await client.post(
        url="/api/tweets", json=tweet_data, headers=header_for_create_tweet
    )
    tweet_id = create_response.json()["tweet_id"]

    # Ставим "лайк" на созданный твит
    like_response = await client.post(
        url=f"/api/tweets/{tweet_id}/likes", headers=header_for_likes
    )
    assert like_response.status_code == 200

    # Снимаем "лайк" с твита
    response = await client.delete(
        url=f"/api/tweets/{tweet_id}/likes", headers=header_for_likes
    )
    assert response.status_code == 200

    # Проверяем, что результат содержит ожидаемые данные
    result = response.json()
    assert result["result"] is True
