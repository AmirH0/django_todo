from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerilizer, UserSerializer
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerilizer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# class LimitedLoginView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         username = request.data.get("username")
#         ip = request.META.get("REMOTE_ADDR") or "unknown"
#         key = f"login_attempts:{username}:{ip}"

#         # تعداد تلاش‌ها را از کش بخوان
#         attempts = cache.get(key, 0)
#         print(f"🔹 Username: {username}, Attempts: {attempts}")  # 👈 برای تست در لاگ

#         # اگر بیشتر از 5 تلاش داشت
#         if attempts >= 5:
#             return Response(
#                 {"detail": "تعداد تلاش‌های شما زیاد است. لطفاً بعداً تلاش کنید."},
#                 status=status.HTTP_429_TOO_MANY_REQUESTS,
#             )

#         # اجرای لاگین اصلی
#         response = super().post(request, *args, **kwargs)

#         # اگر لاگین موفق بود → تلاش‌ها ریست شود
#         if response.status_code == 200:
#             cache.delete(key)
#         else:
#             # افزایش تلاش‌ها تا ۵ دقیقه
#             cache.set(key, attempts + 1, timeout=60 * 5)

#         return response
