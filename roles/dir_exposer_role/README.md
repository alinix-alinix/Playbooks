# dir_exposer

This role places a python web-server with basic auth on a host and exposes a certain folder.
May be useful to publish some logs so that the developers could read them logs by themselves.

Example:
```yaml
- role: dir_exposer_role
  tags: dir_exposer
  vars:
    dir_exposer_python_ver: "2.7"
    dir_exposer_username: "log-reader"
    dir_exposer_password: "lolwut"
    dir_exposer_dir_to_expose: "/opt/tomcat/logs"
```
