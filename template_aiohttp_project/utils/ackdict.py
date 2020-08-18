import asyncio
import time
# from conf import ACK_TIME_OUT #logger

ACK_TIME_OUT = 30
__ack_dict = {"test":{"ts":1576483507.095369}}


def put_ack(cid, ack):
    __ack_dict[cid] = ack


def get_ack(cid):
    ack = __ack_dict.get(cid, None)
    if ack:
        del __ack_dict[cid]
    return ack
  
  
async def clean_expire_ack():
    """
    清理过期的无主的ack
    """
    while True:
        # logger.debug("start clean ack ...")
        expire_keys = []
        for (k,v) in __ack_dict.items():
            if not isinstance(v,dict):
                expire_keys.append(k)
            elif not v['ts']:   # ts为空则为非法ack
                expire_keys.append(k)
            elif (time.time() - v['ts']) > ACK_TIME_OUT:
                expire_keys.append(k)
            else:
                continue
        
        for expire_key in expire_keys:
            # logger.debug('expire ack cleaned:%s',__ack_dict[expire_key])
            del __ack_dict[expire_key]
        
        await asyncio.sleep(5*60)
