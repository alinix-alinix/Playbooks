# Установка службы memcached

Пример использования:

```yaml
- name: include_role memcached-role
  include_role:
    name: memcached-role
  vars:
memcached_user: "memcached"
memcached_group: "memcached"
memcached_listen_address: 0.0.0.0
memcached_listen_port: 11211
memcached_cache_size: 64  # megabytes
memcached_connections_limit: 1024
memcached_max_item_size: "1M"
memcached_service_state: "started"
memcached_service_enabled: "true"
memcached_restart_mode: "always"
memcached_restart_timeout: "10s"
memcache_logfile: "/var/log/memcached.log"
```

С помощью переменных:

- создается окружение (пользователь, группа)
- создается сокет
- создается служба с указанными параметрами
