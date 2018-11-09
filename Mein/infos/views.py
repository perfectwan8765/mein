from django.shortcuts import render
from .models import MainInfo, SubInfo, GradeInfo
from django.views import generic
from django.core.paginator import Paginator
# Create your views here.

class IndexList(generic.ListView):
    template_name = 'main.html'
    context_object_name = "main_list"
    paginate_by = 5
    queryset = MainInfo.objects.filter(region='강남구')

    def get_context_data(self, **kwargs):
        context = super(IndexList, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context


class MainList(generic.ListView):
    template_name = 'main.html'
    context_object_name = "main_list"
    paginate_by = 5

    def get_queryset(self):
        return MainInfo.objects.filter(region=self.kwargs['region'])

    def get_context_data(self, **kwargs):
        context = super(MainList, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['region'] = self.kwargs['region'] if self.kwargs['region'] else '강남구'
        print('region', context['region'])
        return context


class DetailHos(generic.DetailView):
    model = MainInfo
    template_name = 'detail.html'

class SearchList(generic.ListView):
    template_name = 'main.html'
    context_object_name = "main_list"
    paginate_by = 5

    def get_queryset(self):
        topic = self.request.GET.get('topic')
        keyword = self.request.GET.get('keyword')

        if topic == 'name':
            return MainInfo.objects.filter(name__contains=keyword)
        elif topic == 'addr':
            return MainInfo.objects.filter(addr__contains=keyword)
        else:
            return MainInfo.objects.filter(tel__contains=keyword)

    def get_context_data(self, **kwargs):
        context = super(SearchList, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 10
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        context['topic'] = self.request.GET.get('topic')
        context['keyword'] = self.request.GET.get('keyword')
        return context
