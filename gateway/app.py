from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import FastAPI, Request, HTTPException, Depends
from httpx import AsyncClient
from logging import basicConfig, getLogger, INFO


basicConfig(level=INFO)
logger = getLogger('gateway')

class Gateway(FastAPI):
    SECURITY = HTTPBearer()
    CREDENTIALS = 'makemehappy'

    def __init__(self):
        super().__init__(title='Gateway Service')

        self.setup_route()

    @staticmethod
    def verify_credential(credentials: HTTPAuthorizationCredentials = Depends(SECURITY)):
        if credentials.credentials != Gateway.CREDENTIALS:
            raise HTTPException(status_code=403, detail='Invalid credentials')
        return credentials.credentials

    def setup_route(self):
        @self.get('/messages')
        @self.post('/messages')
        async def forward_message(request: Request, credentials: str = Depends(Gateway.verify_credential)):
            target_url = 'http://message_processor:5001/process'
            async with AsyncClient() as client:
                if request.method == 'POST':
                    payload = await request.json()
                    logger.info('Gateway: Received POST request from user with payload: %s' % (
                        payload
                    ))
                    data = await client.post(target_url, json=payload)

                else:
                    logger.info('Gateway: Received GET request from user')
                    data = await client.post(target_url, json={})

            logger.info('Gateway: Response from message-processor: %s' % (
                data.text
            ))
            return JSONResponse(content=data.json())

        @self.get('/health')
        async def health_check():
            return {'status': 'Gateway Up!'}

