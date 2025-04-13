from .models import Post

def user_posts(request):
    if request.user.is_authenticated:
        posts = Post.objects.filter(author=request.user).order_by("-created_at", "-id")  # Posts del usuario logueado
    else:
        posts = None  # No hay usuario autenticado

    return {"user_posts": posts}
