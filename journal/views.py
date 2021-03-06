# This file is part of Cregister - cross register management software
# Copyright (C) 2017  Golikov Ivan <ivnglkv@eml.cc>
#
# Cregister is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cregister is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Cregister.  If not, see <http://www.gnu.org/licenses/>.

from json import loads
from math import ceil
import re

from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView

from .models import PBXPort, PBX
from .utils import CrosspathPointDecoder


def pbx_ports_view(request, pbx, page):
    context = {}
    template = 'journal/pbx_ports.html'

    ports_per_page = 100

    current_page = int(page)

    first_element_index = (current_page - 1) * ports_per_page
    last_element_index = first_element_index + ports_per_page

    pbxports_list = PBXPort.objects.filter(pbx=pbx)[first_element_index:last_element_index]
    pbxports_count = PBXPort.objects.filter(pbx=pbx).count()
    pages_count = ceil(pbxports_count / ports_per_page)

    last_element_index = first_element_index + pbxports_list.count()

    context['pbx'] = pbx
    context['pbx_object'] = PBX.objects.get(pk=pbx)
    context['pbxports_count'] = pbxports_count
    context['current_page'] = current_page
    context['pages_count'] = pages_count
    context['first_element_index'] = first_element_index + 1
    context['last_element_index'] = last_element_index
    context['can_add_pbxport'] = request.user.has_perm('journal.add_pbxport')

    crosspath = [
        loads(point.json_path, cls=CrosspathPointDecoder) for point in pbxports_list
    ]

    context['crosspath'] = crosspath

    return render(request, template, context)


def subscriber_card_view(request, card):
    context = {}
    template = 'journal/subscriber_card.html'

    pbxport = PBXPort.objects.get(subscriber_number=card)

    context['pbxport'] = pbxport
    context['point'] = loads(pbxport.json_path, cls=CrosspathPointDecoder)

    last_pbxport_state = pbxport.history.values()[0]

    last_edit_person = None
    try:
        last_edit_person = User.objects.get(pk=last_pbxport_state['history_user_id'])
    except ObjectDoesNotExist:
        pass

    context['last_edit_person'] = last_edit_person

    return render(request, template, context)


def search(request):
    result = None

    search_input = request.GET.get('search_input', None)

    if search_input is not None and re.match('\d+', search_input):
        get_object_or_404(PBXPort, subscriber_number=int(search_input))
        result = redirect(reverse('journal:subscriber_card', args=(search_input,)))
    else:
        raise Http404

    return result


class PBXPortsView(ListView):
    model = PBXPort
    template_name = 'journal/pbx_ports.html'

    def get_queryset(self, *args, **kwargs):
        return PBXPort.objects.filter(pbx=int(kwargs['pbx']))


def help_view(request, page_name=None):
    help_file_name = 'user_manual.pdf'

    return redirect(settings.MEDIA_URL + help_file_name)
