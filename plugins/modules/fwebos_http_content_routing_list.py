from ansible_collections.fortinet.fortiweb.plugins.module_utils.network.fwebos.fwebos import (fwebos_argument_spec, is_global_admin, is_vdom_enable)
from ansible.module_utils.connection import Connection
from ansible.module_utils.basic import AnsibleModule

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
module: fwebos_http_content_routing_policy_list
description:
  - Configure FortiWeb HTTP Content Routing Policy list for Server Policy via RESTful APIs
"""

EXAMPLES = """
"""

RETURN = """
"""

obj_url = '/api/v2.0/cmdb/server-policy/policy/http-content-routing-list'

# /api/v2.0/cmdb/server-policy/policy/http-content-routing-list?mkey=jobk_server_policy?mkey=jobk_server_policy

# {
#     "data": {
#         "profile-inherit": "enable",
#         "is-default": "no",
#         "status": "enable",
#         "content-routing-policy-name": "jobk_content_routing_policy",
#         "web-protection-profile": ""
#     }
# }

rep_dict = {
    "profile_inherit": "profile-inherit",
    "is_default": "is-default",
    "content_routing_policy_name": "content-routing-policy-name",
    "web_protection_profile": "web-protection-profile"
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
    payload1['data'].pop('name')
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
        profile_inherit=dict(type=str),
        is_default=dict(type=str),
        status=dict(type=str),
        content_routing_policy_name=dict(type=str),
        mkey=dict(type=str),
        web_protection_profile=dict(type=str),
        name=dict(type=str) #name is not used, throws error on line 101 if not set. Excluded parameter from api on line 62
    )

    argument_spec.update(fwebos_argument_spec)

    required_if = [('name')]
    module = AnsibleModule(argument_spec=argument_spec, required_if=required_if)
    module = AnsibleModule(argument_spec=argument_spec)
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