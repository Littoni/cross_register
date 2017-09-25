"""
Release: 0.2.2
Author: Golikov Ivan
Date: 25.09.2017
"""

from json import dumps


INVALID_JSON_PATH_MARK = 'INVALID'


def invalidate_json_path(pbx_port):
    from .models import PBXPort

    PBXPort.objects.filter(pk=pbx_port.pk).update(json_path=INVALID_JSON_PATH_MARK)


def get_parent_and_invalidate_json_path(crosspoint):
    pbxport = crosspoint.get_parent()

    if pbxport:
        invalidate_json_path(pbxport)


def restore_json_path():
    from .models import PBXPort

    invalid_ports = PBXPort.objects.filter(json_path=INVALID_JSON_PATH_MARK)

    for pbx_port in invalid_ports:
        pbx_port.update_json()


def pbxport_post_save(instance, created, raw=False, **kwargs):
    if created and not raw:
        from .models import HistoricalPBXPort, PBXPort
        from .utils import (
            CrosspathPointEncoder,
            get_crosspath,
        )

        instance_qs = PBXPort.objects.filter(pk=instance.pk)

        if not instance.main_source:
            instance_qs.update(main_source=instance)

        cp = get_crosspath(instance.pk)
        instance.json_path = dumps(cp, cls=CrosspathPointEncoder)
        instance.save()

        last_port_state = instance.history.values()[0]
        last_saved_historical_port = HistoricalPBXPort.objects.get(pk=last_port_state['history_id'])
        last_saved_historical_port.delete()

        last_port_state = instance.history.values()[0]
        last_saved_historical_port = HistoricalPBXPort.objects.get(pk=last_port_state['history_id'])
        last_saved_historical_port.json_path = instance.json_path
        last_saved_historical_port.save()


def on_crosspoint_pre_change(instance, raw=False, **kwargs):
    from .models import CrossPoint

    if not raw:
        if instance.source is not None:
            get_parent_and_invalidate_json_path(instance.source)

        try:
            old_instance = CrossPoint.objects.get(pk=instance.pk)
            get_parent_and_invalidate_json_path(old_instance)
        except:
            pass


def autocreate_location(instance, created, raw=False, **kwargs):
    if created and not raw:
        from .models import Cabinet, Location, Room

        new_location = Location()
        if isinstance(instance, Cabinet):
            new_location.cabinet = instance
        elif isinstance(instance, Room):
            new_location.room = instance

        new_location.save()


def on_crosspoint_post_change(instance, created=False, raw=False, **kwargs):
    """Обработчик сигналов post_save и post_delete объектов ExtensionBox, Phone, PunchBlock

    После сохранения нового объекта без источника, выставляется значение поля
    main_source = self

    Также после изменения и удаления обновляется json_path
    """
    from .models import CrossPoint

    if not raw:
        if created and not instance.main_source:
            instance_qs = CrossPoint.objects.filter(pk=instance.pk)
            instance_qs.update(main_source=instance)

        restore_json_path()


def subscriber_phones_changed(instance, action, reverse, model, pk_set, **kwargs):
    from .models import Phone

    pre_actions = ['pre_add', 'pre_remove', 'pre_clean']
    post_actions = ['post_add', 'post_remove', 'post_clean']

    if action in pre_actions:
        phones_set = Phone.objects.filter(pk__in=pk_set)
        pbx_ports = set(map(lambda x: x.get_parent(), phones_set))

        for pbx_port in pbx_ports:
            invalidate_json_path(pbx_port)
    elif action in post_actions:
        restore_json_path()


def subscriber_pre_changed(instance, raw=False, **kwargs):
    if not raw and instance.pk:
        for phone in instance.phones.all():
            get_parent_and_invalidate_json_path(phone)


def subscriber_post_changed(instance, raw=False, **kwargs):
    if not raw:
        restore_json_path()
