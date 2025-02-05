from ansible_collections.fortinet.fortiweb.plugins.module_utils.network.fwebos.fwebos import (fwebos_argument_spec, is_global_admin, is_vdom_enable)
from ansible.module_utils.connection import Connection
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
module: fwebos_http_content_routing_policy_match_list
description:
  - Configure FortiWeb HTTP Content Routing Policy Match list via RESTful APIs
"""

EXAMPLES = """
"""

RETURN = """
"""

obj_url = '/api/v2.0/server/httpcontentrouting.matchlist'

# https://fwa.uniserv.de:8443/api/v2.0/server/httpcontentrouting.matchlist?mkey=jobk

# q_type: 0
# id: 0
# match-object: http-host
# match-object_val: 1
# match-condition: match-begin
# match-condition_val: 1
# x509-subject-name: E
# x509-subject-name_val: 1
# match-expression: jobk
# name:
# value:
# concatenate: and
# concatenate_val: 2
# name-match-condition: match-begin
# name-match-condition_val: 1
# value-match-condition: match-begin
# value-match-condition_val: 1
# start-ip:
# end-ip:
# reverse: disable
# reverse_val: 0
# country-list: []
# ip-list:
# ip-range:
# ip-list-file:
# ztna-ems-tag:
# ztna-ems-tag-combine: or
# ztna-ems-tag-combine_val: 3

rep_dict = {
    "match_object": "match-object",
    "match_object_val": "match-object_val",
    "match_condition": "match-condition",
    "match_condition_val": "match-condition_val",
    "x509_subject_name": "x509-subject-name",
    "x509_subject_name_val": "x509-subject-name_val",
    "match_expression": "match-expression",
    "name_match_condition": "name-match-condition",
    "name_match_condition_val": "name-match-condition_val",
    "value_match_condition": "value-match-condition",
    "value_match_condition_val": "value-match-condition_val",
    "start_ip": "start-ip",
    "end_ip": "end-ip",
    "country_list": "country-list",
    "ip_list": "ip-list",
    "ip_range": "ip-range",
    "ip_list_file": "ip-list-file",
    "ztna_ems_tag": "ztna-ems-tag",
    "ztna_ems_tag_combine": "ztna-ems-tag-combine",
    "ztna_ems_tag_combine_val": "ztna-ems-tag-combine_val"
}

def param_check(module, connection):
    res = True
    action = module.params['action']
    err_msg = ''

    if (action == 'add' or action == 'edit' or action == 'delete') and module.params['name'] is None:
        err_msg = 'name need to set'
        res = False
    if is_vdom_enable(connection) and module.params['vdom'] is None:
        err_msg = 'vdom enable, vdom need to set'
        res = False

    return res, err_msg


def add_obj(module, connection):
    payload1 = {}
    payload1['data'] = module.params
    payload1['data'].pop('action')
    replace_key(payload1['data'], rep_dict)

    code, response = connection.send_request(f"{obj_url}?mkey={payload1['data']['mkey']}", payload1)

    return code, response
    # return 200, payload1

def edit_obj(module, connection):
    payload1 = {}
    payload1['data'] = module.params
    payload1['data'].pop('action')
    replace_key(payload1['data'], rep_dict)

    code, response = connection.send_request(f"{obj_url}?mkey={payload1['data']['mkey']}&sub_mkey={payload1['data']['id']}", payload1)

    return code, response

def replace_key(src_dict, rep_dict):
    for key in rep_dict:
        if key in src_dict:
            new_key = rep_dict[key]
            src_dict[new_key] = src_dict.pop(key)


def main():
    argument_spec = dict(
        action=dict(type=str),
        mkey=dict(type=str),
        q_type=dict(type=str),
        id=dict(type=str),
        match_object=dict(type=str),
        match_object_val=dict(type=int),
        match_condition=dict(type=str),
        match_condition_val=dict(type=int),
        x509_subject_name=dict(type=str),
        x509_subject_name_val=dict(type=int),
        match_expression=dict(type=str),
        name=dict(type=str),
        value=dict(type=str),
        concatenate=dict(type=str),
        concatenate_val=dict(type=int),
        name_match_condition=dict(type=str),
        name_match_condition_val=dict(type=int),
        value_match_condition=dict(type=str),
        value_match_condition_val=dict(type=int),
        start_ip=dict(type=str),
        end_ip=dict(type=str),
        reverse=dict(type=str),
        reverse_val=dict(type=int),
        country_list=dict(type=list),
        ip_list=dict(type=list),
        ip_range=dict(type=str),
        ip_list_file=dict(type=str),
        ztna_ems_tag=dict(type=str),
        ztna_ems_tag_combine=dict(type=str),
        ztna_ems_tag_combine_val=dict(type=int),
        vdom=dict(type='str')
    )

    argument_spec.update(fwebos_argument_spec)

    required_if = [('name')]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if)
    action = module.params['action']
    result = {}
    connection = Connection(module._socket_path)
    param_pass, param_err = param_check(module, connection)

    if is_vdom_enable(connection) and param_pass:
        connection.change_auth_for_vdom(module.params['vdom'])

    if not param_pass:
        result['err_msg'] = param_err
        result['failed'] = True
    elif action == 'add':
        code, response = add_obj(module, connection)
        result['res'] = response
        result['changed'] = True
    elif action == 'get':
        pass
        # code, response = get_obj(module, connection)
        # result['res'] = response
    elif action == 'edit':
        code, response = edit_obj(module, connection)
        # TODO get object check if exists
        # if 'id' not in response.keys():
        #     result['failed'] = True
        #     res = False
        #     result['err_msg'] = 'Entry not found'
        # else:
        #     result['res'] = response
        #     result['changed'] = True
        result['res'] = response
        result['changed'] = True

        # code, data = get_obj(module, connection)
        # if 'results' in data.keys() and data['results'] and type(data['results']) is not int:
        #     res, new_data = needs_update(module, data['results'])
        # else:
        #     result['failed'] = True
        #     res = False
        #     result['err_msg'] = 'Entry not found'
        # if res:
        #     new_data1 = {}
        #     new_data1['data'] = new_data
        #     code, response = edit_obj(module, new_data1, connection)
        #     result['res'] = response
        #     result['changed'] = True
    elif action == 'delete':
        pass
        # code, data = get_obj(module, connection)
        # if 'results' in data.keys() and data['results'] and type(data['results']) is not int:
        #     code, response = delete_obj(module, connection)
        #     result['res'] = response
        #     result['changed'] = True
        # else:
        #     result['failed'] = True
        #     res = False
        #     result['err_msg'] = 'Entry not found'
    else:
        # result['err_msg'] = 'error action: ' + action
        # result['failed'] = True
        pass

    if 'errcode' in str(result):
        result['changed'] = False
        result['failed'] = True
        result['err_msg'] = 'Please check error code'

    module.exit_json(**result)


    result['name'] = module.params['name']
    module.exit_json(**result)


if __name__ == '__main__':
    main()