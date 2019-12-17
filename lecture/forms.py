from django import forms
from django.forms import ModelForm

from .models import Course, Notice, Enrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'semester', 'year', 'description', ]

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "강의명"
        self.fields['semester'].label = "학기"
        self.fields['year'].label = "년도"
        self.fields['description'].label = "강의개요"

    def save(self, commit=True):
        self.instance = Course(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance


class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'file', ]
        widgets = {"file": forms.FileInput(attrs={'id': 'files', 'required': True, 'multiple': True})}

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "제목"
        self.fields['content'].label = "내용"
        self.fields['file'].label = "첨부파일"

    def save(self, commit=True):
        self.instance = Notice(**self.cleaned_data)
        if commit:
            self.instance.save()
        return self.instance
