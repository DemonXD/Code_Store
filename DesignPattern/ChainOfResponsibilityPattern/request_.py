class Requests:
    def __init__(self, is_s, is_a, HM, HU, P):
        self.Meta = {}
        self.Meta['is_superuser'] = is_s
        self.Meta['is_authenticated'] = is_a
        self.Meta['HTTP_X_ORIGIN_METHOD'] = HM
        self.Meta['HTTP_X_ORIGIN_URL'] = HU
        self.Meta['PERMIT'] = P


def get_requests():
    request_11P = Requests(True, True, 'PUT', '/api/v1/data/counterdata/', True) # 超级用户 直接通过 200
    request_111P = Requests(False, True, 'GET', '/api/v1/data/counterdata/', True) # 登录用户 资源正确 有权限 200
    request_00P = Requests(False, False, 'GET', '/api/v1/data/counterdata/', True) # 未登录用户 401
    request_110P = Requests(False, True, 'GET', '/api/v1/data/counterdata/', False) # 登录用户 有资源 无权限 403
    request_101P = Requests(False, True, 'PUT', '/api/v1/data/counterdata/', True) # 登录用户 无资源
    return [request_11P, request_111P, request_00P, request_110P, request_101P]