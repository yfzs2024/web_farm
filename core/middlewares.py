import json
from django.utils.decorators import async_only_middleware
from django.http import HttpRequest, JsonResponse

# my middlewares

@async_only_middleware
class LoginRequireMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_paths = ['/api/login/', '/api/login']

    async def __call__(self, request: HttpRequest):
        path = request.path
        user = await request.auser()

        # 判断是否为不要认证的url
        if path not in self.allowed_paths:
            # 判断是否登录
            if not user.is_authenticated:
                return JsonResponse({'error':'Request Unauthorized'}, status=401)

        return await self.get_response(request)

@async_only_middleware
class ParseJsonMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, request: HttpRequest):
        data = request.body
        # 放行非 POST
        if request.method == 'POST':
            # 检测Content-Type
            if request.content_type != 'application/json':
                return JsonResponse({'error': 'Content-Type must be application/json'}, status=415)
            # 解析json
            try:
                json_data = json.loads(data.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse({'error':'Invalid JSON'}, status=400)
            # 拒绝非字典顶层json
            if not isinstance(json_data, dict):
                return JsonResponse({'error': 'JSON body must be an object'}, status=400)
            else:
                setattr(request, 'json_data', json_data)

        return await self.get_response(request)