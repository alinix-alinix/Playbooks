# example include

```yaml
- name: add firewalld ports
    firewalld_ports:
      - '80/tcp'
      - '443/tcp'
  include_role:
    name: firewalld_role
```
