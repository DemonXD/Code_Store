// 打印--->Device._meta.__dict__后显示的数据

{
    'model': <Model: Device>, 
    'database': <peewee.PostgresqlDatabase object at 0x7fd8e9c446d8>, 
    'fields': 
    {
        'id': <AutoField: Device.id>, 
        'hostname': <CharField: Device.hostname>, 
        'ip_address': <CharField: Device.ip_address>, 
        'user_name': <CharField: Device.user_name>, 
        'password': <CharField: Device.password>, 
        'is_added': <BooleanField: Device.is_added>, 
        'status': <CharField: Device.status>, 
        'flag': <BigIntegerField: Device.flag>, 
        'is_removed': <BooleanField: Device.is_removed>, 
        'create_time': <CharField: Device.create_time>, 
        'modified_time': <CharField: Device.modified_time>
    }, 
    'columns': {
        'id': <AutoField: Device.id>, 
        'hostname': <CharField: Device.hostname>, 
        'ip_address': <CharField: Device.ip_address>, 
        'user_name': <CharField: Device.user_name>, 
        'password': <CharField: Device.password>, 
        'is_added': <BooleanField: Device.is_added>, 
        'status': <CharField: Device.status>, 
        'flag': <BigIntegerField: Device.flag>, 
        'is_removed': <BooleanField: Device.is_removed>, 
        'create_time': <CharField: Device.create_time>, 
        'modified_time': <CharField: Device.modified_time>
    }, 
    'combined': {
        'id': <AutoField: Device.id>, 
        'hostname': <CharField: Device.hostname>, 
        'ip_address': <CharField: Device.ip_address>, 
        'user_name': <CharField: Device.user_name>, 
        'password': <CharField: Device.password>, 
        'is_added': <BooleanField: Device.is_added>, 
        'status': <CharField: Device.status>, 
        'flag': <BigIntegerField: Device.flag>, 
        'is_removed': <BooleanField: Device.is_removed>, 
        'create_time': <CharField: Device.create_time>, 
        'modified_time': <CharField: Device.modified_time>
    }, 
    '_sorted_field_list': <peewee._SortedFieldList object at 0x7fd8e53a1978>, 
    'sorted_fields': [
        <AutoField: Device.id>, 
        <CharField: Device.hostname>,
        <CharField: Device.ip_address>, 
        <CharField: Device.user_name>, 
        <CharField: Device.password>, 
        <BooleanField: Device.is_added>, 
        <CharField: Device.status>, 
        <BigIntegerField: Device.flag>, 
        <BooleanField: Device.is_removed>, 
        <CharField: Device.create_time>, 
        <CharField: Device.modified_time>
    ], 
    'sorted_field_names': [
        'id', 
        'hostname', 
        'ip_address', 
        'user_name', 
        'password', 
        'is_added', 
        'status', 
        'flag', 
        'is_removed', 
        'create_time', 
        'modified_time'
    ], 
    'defaults': {
        <CharField: Device.hostname>: 'raspberry', 
        <BooleanField: Device.is_added>: False, 
        <CharField: Device.status>: '1',
        <BigIntegerField: Device.flag>: 10, 
        <BooleanField: Device.is_removed>: False, 
        <CharField: Device.create_time>: '2019-07-18 15: 25', 
        <CharField: Device.modified_time>: '2019-07-18 15: 25'
    }, 
    '_default_by_name': {
        'hostname': 'raspberry', 
        'is_added': False, 
        'status': '1', 
        'flag': 10, 
        'is_removed': False, 
        'create_time': '2019-07-18 15: 25', 
        'modified_time': '2019-07-18 15: 25'
    }, 
    '_default_dict': {
        <CharField: Device.hostname>: 'raspberry',
        <BooleanField: Device.is_added>: False,
        <CharField: Device.status>: '1', 
        <BigIntegerField: Device.flag>: 10, 
        <BooleanField: Device.is_removed>: False, 
        <CharField: Device.create_time>: '2019-07-18 15: 25', 
        <CharField: Device.modified_time>: '2019-07-18 15: 25'
    }, 
    '_default_callables': {}, 
    '_default_callable_list': [], 
    'name': 'device', 
    'table_function': None, 
    'legacy_table_names': True, 
    'table_name': 'device', 
    '_table': None, 'indexes': [], 
    'constraints': None, 
    '_schema': None, 
    'primary_key': <AutoField: Device.id>, 
    'composite_key': False,
    'auto_increment': True, 
    'only_save_dirty': False, 
    'depends_on': None, 
    'table_settings': None, 
    'without_rowid': False, 
    'temporary': False, 
    'refs': {}, 
    'backrefs': {
        <ForeignKeyField: DeviceService.device>: <Model: DeviceService>
    }, 
    'model_refs': defaultdict(<class 'list'>),
    {}, 
    'model_backrefs': defaultdict(<class 'list'>,
    {<Model: DeviceService>: [<ForeignKeyField: DeviceService.device>
        ]
    }), 
    'manytomany': {}, 
    'options': {}, 
    '_additional_keys': set(), 
    '_db_hooks': []
}