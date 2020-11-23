from django.views import generic

from django.db.models import Q

from blog import models as BlogModels

from constance import config

from .forms import SearchForm


class Base(generic.ListView):
    template_name = 'base.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs_categories'] = BlogModels.BlogCategory.objects.all()
        context['videocasts_categories'] = BlogModels.VideocastCategory.objects.all()
        context['podcast_categories'] = BlogModels.PodcastCategory.objects.all()
        context['podcasts'] = BlogModels.Podcast.objects.order_by('-pk').filter(publish=True)[:2]
        context['config'] = config
        return context

    def get_queryset(self):
        pass


class Index(Base):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_blog'] = BlogModels.Blog.objects.order_by('-pk').filter(publish=True)[:1]
        context['skills'] = BlogModels.Skill.objects.all()
        context['blogs'] = BlogModels.Blog.objects.order_by('-pk').filter(publish=True)[1:5]
        context['videocasts'] = BlogModels.Videocast.objects.order_by('-pk').filter(publish=True)[:4]
        return context


class Search(Base):
    template_name = 'search.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            context['blogs'] = BlogModels.Blog.objects.order_by('-pk').filter(Q(title__icontains=query) | Q(content__icontains=query))
            context['videocasts'] = BlogModels.Videocast.objects.order_by('-pk').filter(Q(title__icontains=query) | Q(content__icontains=query))
            context['podcasts'] = BlogModels.Podcast.objects.order_by('-pk').filter(Q(title__icontains=query) | Q(content__icontains=query))
        return context


class Blog(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Blog.objects.all()
        return context


class BlogArchiveByCategoryPK(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Blog.objects.filter(category=self.kwargs['pk'])
        return context


class BlogSingle(Base):
    template_name = 'single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_content'] = BlogModels.Blog.objects.filter(slug=self.kwargs['slug'])
        return context


class Videocast(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Videocast.objects.all()
        return context


class VideocastArchiveByCategoryPK(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Videocast.objects.filter(category=self.kwargs['pk'])
        return context


class VideocastSingle(Base):
    template_name = 'single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_content'] = BlogModels.Videocast.objects.filter(slug=self.kwargs['slug'])
        return context


class Podcast(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Podcast.objects.all()
        return context


class PodArchiveByCategoryPK(Base):
    template_name = 'archive.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archives'] = BlogModels.Podcast.objects.filter(category=self.kwargs['pk'])
        return context


class PodSingle(Base):
    template_name = 'single.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['single_content'] = BlogModels.Podcast.objects.filter(slug=self.kwargs['slug'])
        return context
