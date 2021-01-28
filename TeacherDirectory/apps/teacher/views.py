import io
import os

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
import csv
from django.views.generic import ListView,DetailView
from TeacherDirectory import settings
from .filters import NameFilter
from . forms import TeacherCsvModelForm
from django.views import View
from .models import TeacherCsvModel
from ..accounts.models import User, Subject
class TeacherUploadCsvView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        if request.user.is_superuser:
            form=TeacherCsvModelForm()
            context={'form':form}
            return render(request,'teacher/teacher_add.html',context)
        else:
            messages.info(request, "please login as superuser")
            return redirect('accounts:user-login')

    def post(self,request):
        form = TeacherCsvModelForm(request.POST , request.FILES)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            obj=TeacherCsvModel.objects.get(activated=False)
            paramFile = io.TextIOWrapper(obj.csv_file)
            portfolio1 = csv.DictReader(paramFile)
            list_of_dict = list(portfolio1)
            for value in list_of_dict:
                if len(User.objects.filter(email=value['Email Address']))>0:
                    continue
                else:
                    user=User.objects.create(first_name=value['First Name'],last_name=value['Last Name'],
                                                 email=value['Email Address'],room_number=value['Room Number'],
                                                 username=value['Email Address'],phone_number=value['Phone Number'])
                    if value['Profile picture'].endswith('jpg') or value['Profile picture'].endswith('JPG'):
                        image=value['Profile picture']
                        file_available=os.path.isfile(os.path.join(settings.STATIC_ROOT, f'images/{image}'))
                        if file_available:
                            file = open(os.path.join(settings.STATIC_ROOT, f'images/{image}'), "rb")
                            user.avatar.save(f"{image}", file, save=True)
                        else:
                            file = open(os.path.join(settings.STATIC_ROOT, f'images/{21230}.JPG'), "rb")
                            user.avatar.save(f"{21230}.JPG", file, save=True)
                    else:
                        file = open(os.path.join(settings.STATIC_ROOT, f'images/{21230}.JPG'), "rb")
                        user.avatar.save(f"{21230}.JPG", file, save=True)
                    teacher_taught_value=value['Subjects taught'].split(', ')
                    for subject_value in teacher_taught_value[:5]:
                        subject_assign = Subject.objects.get(subject_name=subject_value.capitalize())
                        user.subject.add(subject_assign)
                        user.save()
            obj.activated=True
            obj.save()
            messages.success(request, "All the data successfully save")
            return redirect('teacher-list')
        else:
            return redirect('teacher-list')


class TeacherListView(LoginRequiredMixin, ListView):
    model = User
    paginate_by = 2
    template_name='teacher/teacher_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = NameFilter(self.request.GET, queryset=self.get_queryset())
        return context

class TeacherDetailView(DetailView):
    model = User
    template_name = 'teacher/teacher_detail.html'
