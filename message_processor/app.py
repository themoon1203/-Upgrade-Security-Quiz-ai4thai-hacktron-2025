from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime
from colorlog import ColoredFormatter
from logging import StreamHandler, basicConfig, getLogger, INFO
from time import time


getLogger('').handlers.clear()

basicConfig(level=INFO)
logger = getLogger('processor')

logger.handlers.clear()
logger.propagate = False

handler = StreamHandler()
formatter = ColoredFormatter(
    '%(log_color)s%(levelname)s:%(name)s:%(message)s',
    log_colors={
        'INFO': 'yellow',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)
handler.setFormatter(formatter)
logger.handlers = [handler]

class MessageProcessor(FastAPI):
    def __init__(self):
        super().__init__(title='Message Processor Service')
        self.setup_route()

    def setup_route(self):
        @self.post('/process')
        async def process_message(request: Request):
            payload = await request.json()
            logger.info('Processor: Received request from gateway with payload: %s' % (
                payload
            ))

            request_id = 'REQ-%s-%s' % (datetime.now().strftime('%Y%m%d%H%M%S'),str(hash(str(payload)) % 1000).zfill(3))
            message = payload.get('message', 'Hello from make me happy')

            return JSONResponse(content={
                'answer': message,
                'request_id': request_id,
                'timestamp': time()
            })

        @self.get('/health')
        async def health_check():
            return {'status': 'Processor Up!'}