# encoding: utf-8

from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='/tmp')

from django.conf import settings
from django import forms
from django.db.models import Q, Count
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

class FileForm(forms.Form):

    file = forms.FileField(storage=fs)

    class Meta:
        fields = ('image',)

    def clean(self):
        image = self.cleaned_data['image']
        if image.size > settings.MAX_UPLOAD_BYTE:
            raise forms.ValidationError(u"Votre fichier ne doit pas dépasser %s Mo." % settings.MAX_UPLOAD_MB)

    def get_display_order(self):
        return self.prefix.split('-').pop()

@require_POST
@login_required
@csrf_exempt
def upload_media(request):
    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        ad_pk = request.POST.get('ad_pk', None)
        if ad_pk:
            ad = Organization.objects.get(pk=ad_pk, owner=request.user)
        else:
            ad = None
        media = Media(
            image=request.FILES['image'],
            owner=request.user,
            organization=ad,
            # type=request.POST.get('type', None),
            # file_typemime= request.POST.get('file_typemime', None)
        )
        media.save()

        return JsonResponse({
            'success': True,
            'pk': media.pk,
            # 'file_typemime': new_file.file_typemime,
            'ad_pk': media.ad_id,
        })
    return JsonResponse({ 'success': False, 'errors': form.errors })

@require_GET
@login_required
@csrf_exempt
def delete_media(request):
    if request.GET.get('pk'):
        media = Media.objects.get(owner=request.user, pk=request.GET.get('pk'))
        media.image.storage.delete(media.image.name)
        media.delete()
        return JsonResponse({ 'success': True })
    return JsonResponse({ 'success': False })