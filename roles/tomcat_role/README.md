# Установка web-сервера tomcat. Полностью параметризованный. Кроме томката, настраивает еще и окружение.

Пример использования: 
```yaml
- name: include_role tomcat_role
  include_role:
    name: tomcat_role
  vars:
    install_java: "true"
    java_version: "8u301"
    tomcat_management_app_username: "tomcat-admin"
    tomcat_management_app_password: "s3cret_passw0rd"
    tomcat_instance_name: "tomcat"
    tomcat_version: "{{ global_tomcat_version }}"
    tomcat_dynamic_memory: "true"
    tomcat_dynamic_memory_offheap: "{{ offheap }}"
    tomcat_sysctl_vars:
    - param: 'fs.inotify.max_user_watches'
      value: '16384'
    - param: 'fs.inotify.max_user_instances'
      value: '256'
    - param: 'net.ipv4.ip_local_port_range'
      value: '15000 61000'
    - param: 'net.core.somaxconn'
      value: '1024'
    - param: 'net.core.netdev_max_backlog'
      value: '2000'
    - param: 'net.ipv4.tcp_max_syn_backlog'
      value: '2048'
    - param: 'fs.file-max'
      value: '30000'
    tomcat_additional_folders:
    - path: "/ignite"
      mode: "0755"
      owner: "tomcat"
      group: "tomcat"
    - path: "/ignite/work"
      mode: "0755"
      owner: "tomcat"
      group: "tomcat"
    tomcat_xx_parameters:
    - "+UseG1GC"
    - "+UseLinuxPosixThreadCPUClocks"
    - "-ScavengeBeforeFullGC"  
    - "+DisableExplicitGC" 
    - "+UnlockCommercialFeatures"
    - "+FlightRecorder"
    tomcat_additional_ports:
      - "5701-{{ 5700 + (ansible_play_hosts_all | length) }}/tcp"  # Hazelcast discovery port range
```

Роль ставит томкат:
 - при необходимости поставит два томката на хост, но simlink /opt/tomcat будет создан только для инстанса томката с именем по-умолчанию tomcat.
 - роль проверяет установку заданного инстанса томката, проводит апгрейд/даунгрейд в случае необходимости, полный редеплой, если меняются пользователи и группы, отвечающие за томкат, или просто обновляет шаблоны.
 - динамическая и ручная установка параметров памяти сервера томкат.
 - роль проверяет базовые порты, необходимые для работы томката. Если один из портов уже слушается, томкат не установится без изменения в переменных.
 - при необходимости, объявляем дополнительные порты, необходимые для работы приложеньки в переменной tomcat_additional_ports
 - и многое другое.

Со всеми переменными можно ознакомиться в infra/roles/tomcat_role/defaults/main.yml
