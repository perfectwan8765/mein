from django.shortcuts import render
from .models import MainInfo, SubInfo, GradeInfo
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

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
        context['max_index'] = max_index
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
        context['max_index'] = max_index
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
        context['max_index'] = max_index
        context['topic'] = self.request.GET.get('topic')
        context['keyword'] = self.request.GET.get('keyword')
        return context

class DivList(generic.ListView):
    template_name = 'checkMain.html'
    context_object_name = "main_list"
    paginate_by = 5

    def get_queryset(self):
        q = Q(name__contains="")
        sub = 0  if not self.request.GET.get('sub') else self.request.GET.get('sub')
        if self.request.GET.get('emergency') : q= q & Q(emergency='Y')
        if self.request.GET.get('limbs') : q= q & Q(limbs='Y')
        if self.request.GET.get('newborn') : q= q & Q(newborn='Y')
        if self.request.GET.get('pregnent') : q= q & Q(pregnent='Y')
        if self.request.GET.get('burn') : q= q & Q(burn='Y')
        if self.request.GET.get('dialysis') : q= q & Q(dialysis='Y')
        # if self.request.GET.get('saturday') : q= q | Q(saturdayStart='Y')
        # if self.request.GET.get('sunday') : q= q | Q(sundayStart='Y')
        # if not self.request.GET.get('holiday') : q= q | Q(emergency='Y')
        if sub != 0:
            for s in sub.split(","):
                q = q & Q(subject__contains=s)
        print(q)
        return MainInfo.objects.filter(q)

    def get_context_data(self, **kwargs):
        context = super(DivList, self).get_context_data(**kwargs)
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
        context['max_index'] = max_index
        if self.request.GET.get('sub') : context['sub'] = self.request.GET.get('sub')
        if self.request.GET.get('emergency') : context['emergency'] = self.request.GET.get('emergency')
        if self.request.GET.get('limbs') : context['limbs'] = self.request.GET.get('limbs')
        if self.request.GET.get('newborn'): context['newborn'] = self.request.GET.get('newborn')
        if self.request.GET.get('pregnent') : context['pregnent'] = self.request.GET.get('pregnent')
        if self.request.GET.get('burn') : context['burn'] = self.request.GET.get('burn')
        if self.request.GET.get('dialysis') : context['dialysis'] = self.request.GET.get('dialysis')
        return context


