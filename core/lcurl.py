import logging
import aiohttp
import async_timeout

logger = logging.getLogger(__name__)


class Lcurl(object):

    async def get(self, session='', url='', params={}, headers={}, response_type='json'):
        try:
            with async_timeout.timeout(5):
                async with session.get(url, params=params, headers=headers) as r:
                    if r.status != 200:
                        return False
                    else:
                        if response_type == 'binary':
                            response = await r.read()
                        elif response_type == 'text':
                            response = await r.text()
                        else:
                            response = await r.json(content_type=None)
                        return response
        except Exception as e:
            logging.error(e)
            return False

    async def post(self, session='', url='', data='', headers={}, response_type='json'):
        try:
            with async_timeout.timeout(5):
                async with session.post(url, data=data, headers=headers) as r:
                    if r.status != 200:
                        return False
                    else:
                        if response_type == 'binary':
                            response = await r.read()
                        elif response_type == 'text':
                            response = await r.text()
                        else:
                            response = await r.json(content_type=None)
                        return response
        except Exception as e:
            logging.error(e)
            return False