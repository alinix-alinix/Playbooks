# Anycast role examples

```yaml
- name: include_role anycast_role
  include_role:
    name: anycast_role
  hosts: anycast_service
  vars:
    anycast_ip: "10.9.9.163"
    anycast_ospf_interface_cost: 10
    anycast_ospf_interface_priority: 1
    anycast_ospf_auth_key: "{{ lookup('hashi_vault', 'secret=infra/data/noc/routers/mikrotik/ospf/{}
              mount_point=secrets token={} url=https://vault/'.format('service_zones_md5',vault_access_token)).password }}"
    anycast_ospf_auth_key_id: 5
    anycast_ospf_area_auto: true
    anycast_leader_service: "haproxy"
  serial:
    - 1
    - 50%
    - 100%
  tags: test
```

## This role allows you to anycast whatever you want. Anycast services have to be deployed only in 3 DCs of a certain company, because this playbook is created according to existing OSPF service areas

- DC1: 98.0.1.1
- DC2: 98.0.2.1
- DC3: 98.0.3.1

Service area will be applied automatically. Still you can override the service area id by using this combination of variables, but in most cases this is useless:

anycast_ospf_auto_area: false
anycast_ospf_area_manual: "100.1.1.1"

anycast_leader_service variable allow you to link bird service to some other service. If Leading service is killed or stopped, the same will happen to bird.
Important: Make sure the leader service is already present in the systemd. In case you're goin to add it later in the playbook, you should add post_task reenabling bird to form correct systemd simlinks
# systemd reenable bird
