from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreateUpdateForm
from django.utils.text import slugify


class HomeView(View):
	def get(self, request):
		posts = Post.objects.all()
		return render(request, 'home/index.html', {'posts':posts})


class PostDetailView(View):
	def get(self, request, post_id, post_slug):
		post = get_object_or_404(Post, pk=post_id, slug=post_slug)
		comments = post.pcomments.filter(is_reply=False)
		return render(request, 'home/detail.html', {'post':post, 'comments':comments})


class PostDeleteView(LoginRequiredMixin, View):
	def get(self, request, post_id):
		post = get_object_or_404(Post, pk=post_id)
		if post.user.id == request.user.id:
			post.delete()
			messages.success(request, 'post deleted successfully', 'success')
		else:
			messages.error(request, 'you cant delete this post', 'danger')
		return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
	form_class = PostCreateUpdateForm

	def setup(self, request, *args, **kwargs):
		self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
		return super().setup(request, *args, **kwargs)

	def dispatch(self, request, *args, **kwargs):
		post = self.post_instance
		if not post.user.id == request.user.id:
			messages.error(request, 'you cant update this post', 'danger')
			return redirect('home:home')
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(instance=post)
		return render(request, 'home/update.html', {'form':form})

	def post(self, request, *args, **kwargs):
		post = self.post_instance
		form = self.form_class(request.POST, instance=post)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['body'][:30])
			new_post.save()
			messages.success(request, 'you updated this post', 'success')
			return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
	form_class = PostCreateUpdateForm

	def get(self, request, *args, **kwargs):
		form = self.form_class
		return render(request, 'home/create.html', {'form':form})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_post = form.save(commit=False)
			new_post.slug = slugify(form.cleaned_data['body'][:30])
			new_post.user = request.user
			new_post.save()
			messages.success(request, 'you created a new post', 'success')
			return redirect('home:post_detail', new_post.id, new_post.slug)
