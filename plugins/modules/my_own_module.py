#!/usr/bin/python

# Copyright: (c) 2026, Pavel (@ShishelM)
# GNU General Public License v3.0+ (see COPYING or https://gnu.org)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Создает текстовый файл с заданным содержимым
version_added: "1.0.0"
description: Создает или обновляет файл на удаленном хосте, поддерживая идемпотентность.
options:
    path:
        description: Абсолютный путь к создаваемому файлу.
        required: true
        type: str
    content:
        description: Строковое содержимое текстового файла.
        required: true
        type: str
author:
    - Pavel (@ShishelM)
'''

EXAMPLES = r'''
- name: Создать конфигурационный файл
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/netology.txt
    content: "Hello DevOps from my own module!"
'''

RETURN = r'''
path:
    description: Путь к созданному файлу.
    type: str
    returned: always
content:
    description: Содержимое, которое было записано.
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    target_path = module.params['path']
    target_content = module.params['content']
    
    result['path'] = target_path
    result['content'] = target_content

    # Проверяем, существует ли файл
    file_exists = os.path.exists(target_path)
    
    current_content = ""
    if file_exists:
        # Если существует, читаем его содержимое для проверки идемпотентности
        with open(target_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

    # Если файла нет или контент отличается — планируем изменения
    if not file_exists or current_content != target_content:
        result['changed'] = True

    # Если запущены в режиме check_mode, просто выходим
    if module.check_mode:
        module.exit_json(**result)

    # Если зафиксированы изменения — производим физическую запись файла
    if result['changed']:
        try:
            # Создаем родительские директории, если их нет
            dir_name = os.path.dirname(target_path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(target_content)
        except Exception as e:
            module.fail_json(msg=f"Не удалось записать файл: {str(e)}", **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
