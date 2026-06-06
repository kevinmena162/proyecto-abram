from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Author, Post, Comment

def feed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    authors = Author.objects.all()
    # Suggestions (all authors except maybe the first one or just all of them for simplicity)
    suggestions = list(authors)[:5]
    context = {
        'posts': posts,
        'authors': authors,
        'suggestions': suggestions,
    }
    return render(request, 'authors/feed.html', context)

def profile_view(request, username):
    author = get_object_or_404(Author, username=username)
    posts = author.posts.all().order_by('-created_at')
    authors = Author.objects.all()
    context = {
        'author': author,
        'posts': posts,
        'authors': authors,
    }
    return render(request, 'authors/profile.html', context)

def post_detail_json(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = []
    for comment in post.comments.all().order_by('created_at'):
        # Get profile picture of comment author if they are one of our authors
        comment_author = Author.objects.filter(username=comment.author_name).first()
        pfp_url = comment_author.profile_picture.url if comment_author and comment_author.profile_picture else '/static/img/default_avatar.png'
        
        comments.append({
            'author_name': comment.author_name,
            'pfp_url': pfp_url,
            'text': comment.text,
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    
    data = {
        'id': post.id,
        'author_name': post.author.name,
        'author_username': post.author.username,
        'author_pfp': post.author.profile_picture.url if post.author.profile_picture else '/static/img/default_avatar.png',
        'author_occupation': post.author.occupation,
        'image_url': post.image.url,
        'caption': post.caption,
        'likes_count': post.likes_count,
        'location': post.location,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M'),
        'comments': comments,
    }
    return JsonResponse(data)

@csrf_exempt
def add_comment_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            post_id = data.get('post_id')
            author_name = data.get('author_name', 'visitante').strip()
            text = data.get('text', '').strip()
            
            if not text:
                return JsonResponse({'error': 'El comentario no puede estar vacío.'}, status=400)
                
            post = get_object_or_404(Post, id=post_id)
            
            # Clean author_name (remove @ if present)
            if author_name.startswith('@'):
                author_name = author_name[1:]
            if not author_name:
                author_name = 'visitante'
                
            comment = Comment.objects.create(
                post=post,
                author_name=author_name,
                text=text
            )
            
            # Get profile pic if they commented as one of our authors
            comment_author = Author.objects.filter(username=author_name).first()
            pfp_url = comment_author.profile_picture.url if comment_author and comment_author.profile_picture else '/static/img/default_avatar.png'
            
            return JsonResponse({
                'success': True,
                'comment': {
                    'author_name': comment.author_name,
                    'pfp_url': pfp_url,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
                }
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
            
    return JsonResponse({'error': 'Método no permitido.'}, status=405)

