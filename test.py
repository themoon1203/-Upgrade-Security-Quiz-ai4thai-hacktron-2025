import asyncio
import httpx

GATEWAY_URL = 'http://localhost:5000/messages'
VALID_TOKEN = 'makemehappy'
INVALID_TOKEN = 'wrongtoken'

async def test_valid_token_post_with_payload():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GATEWAY_URL,
            json={'message': 'Hello from test.py!'},
            headers={'Authorization': 'Bearer %s' % (VALID_TOKEN)}
        )
        print('POST with payload:', response.status_code, response.json())

async def test_valid_token_post_no_payload():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GATEWAY_URL,
            json={},
            headers={'Authorization': 'Bearer %s' % (VALID_TOKEN)}
        )
        print('POST no payload:', response.status_code, response.json())

async def test_valid_token_get():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GATEWAY_URL,
            headers={'Authorization': 'Bearer %s' % (VALID_TOKEN)}
        )
        print('GET:', response.status_code, response.json())

async def test_invalid_token():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GATEWAY_URL,
            json={'message': 'This should fail'},
            headers={'Authorization': 'Bearer %s' % (INVALID_TOKEN)}
        )
        print('Invalid credentials:', response.status_code, response.text)

async def main():
    await test_valid_token_post_with_payload()
    await test_valid_token_post_no_payload()
    await test_valid_token_get()
    await test_invalid_token()

if __name__ == '__main__':
    asyncio.run(main())