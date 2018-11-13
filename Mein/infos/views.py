from django.shortcuts import render
from .models import MainInfo, SubInfo, GradeInfo, SpecialInfo
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
        special_q = None
        day_q = None
        sub_q = None
        sub = 0  if not self.request.GET.get('sub') else self.request.GET.get('sub')
        spec = 0 if not self.request.GET.get('spec') else self.request.GET.get('spec')
        day = 0 if not self.request.GET.get('day') else self.request.GET.get('day')

        if spec != 0 :
            if '응급실' in spec : special_q = Q(emergency='Y') if special_q is None else special_q & Q(emergency='Y')
            if '사지접합' in spec : special_q = Q(limbs='Y') if special_q is None else special_q & Q(limbs='Y')
            if '신생아' in spec : special_q = Q(newborn='Y') if special_q is None else special_q & Q(newborn='Y')
            if '조산산모' in spec : special_q = Q(pregnent='Y') if special_q is None else special_q & Q(pregnent='Y')
            if '화상' in spec : special_q = Q(burn='Y') if special_q is None else special_q & Q(burn='Y')
            if '응급투석' in spec : special_q = Q(dialysis='Y') if special_q is None else special_q & Q(dialysis='Y')
            special_list = SpecialInfo.objects.filter(special_q).values_list('hpid', flat=True)
            special_q = None
            for special_hp in special_list:
                special_q = Q(hpid=special_hp) if special_q is None else special_q | Q(hpid=special_hp)

        if day != 0 :
            if '토요일' in day : day_q = Q(saturdayStart__contains='0') if day_q is None else day_q & Q(saturdayStart__contains='0')
            if '일요일' in day : day_q = Q(sundayStart__contains='0') if day_q is None else day_q & Q(sundayStart__contains='0')
            if '공휴일' in day : day_q = Q(holidayStart__contains='0') if day_q is None else day_q & Q(holidayStart__contains='0')
            day_list = SubInfo.objects.filter(day_q).values_list('hpid', flat=True)
            day_q = None
            for day_hp in day_list:
                day_q = Q(hpid=day_hp) if day_q is None else day_q | Q(hpid=day_hp)

        if sub != 0:
            for s in sub.split(","):
                sub_q = Q(subject__contains=s) if sub_q is None else sub_q & Q(subject__contains=s)

        if special_q is None : special_q = Q(name__contains="")
        if day_q is None : day_q = Q(name__contains="")
        if sub_q is None : sub_q = Q(name__contains="")

        main_q = special_q & day_q & sub_q

        return MainInfo.objects.filter(main_q)

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
        if self.request.GET.get('spec'): context['spec'] = self.request.GET.get('spec')
        if self.request.GET.get('day') : context['day'] = self.request.GET.get('day')
        return context


