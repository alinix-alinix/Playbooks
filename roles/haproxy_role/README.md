# This role installs and setups haproxy. Binary file is taken from local NAS. You can have dynamic cpu core map (default) or static one. In the least case you should provide the number of threads to spawn for haproxy. Dynamic cpu map will cause the use of all available cores to spawn haproxy threads.

Example: 
```yaml
- name: include_role haproxy_role
  include_role:
    name: haproxy_role
  hosts: balancer_from_inventory
  vars:
    haproxy_version: "2.4.7"
    haproxy_frontends:
    - name: "stats"
      system: true  # system frontend, showing haproxy stats. Has no tradicial backend. 
      bind: ":1936"  # listen address
      mode: "http"  # http or tcp mode
      options:
        - name: "stats"
          value: "enable"
        - name: "stats realm"
          value: "Haproxy\ Statistics"
        - name: "stats uri"
          value: "/stats"
        - name: "stats refresh"
          value: "5s"
        - name: "stats auth"
          value: "{{ haproxy_stats_user }}:{{ haproxy_stats_password }}"
      acl: []
      use_backend: []
    - name: "health"
      system: true  # system frontend, showing haproxy healthcheck if needed. Has no tradicial backend. 
      bind: "127.0.0.1:1937"
      mode: "http"
      options:
        - name: "monitor-uri"
          value: "/healthz"
        - name: "option"
          value: "dontlognull"
      acl: []
      use_backend: []
    - name: "http_port_80"
      system: false  # tradicial frontend. it should have a backend
      bind: ":80"
      mode: "http"
      options:
        - name: "option"
          value: "forwardfor"
        - name: "http-request add-header"
          value: "X-Forwarded-Host %[req.hdr(host)]"
        - name: "http-request add-header"
          value: "X-Forwarded-Server %[req.hdr(host)]"
        - name: "http-request add-header"
          value: "X-Forwarded-Port %[dst_port]"
      acl:  # you can have several ACLS rules to forward requests to corresponding backend
        - name: "is_crmtest"
          criteria: "hdr(host) -i"
          value: "some-resource.local"
      use_backend:  #  you can have several backends corresponding with ACL
        - name: "some-resource"
          criteria: "is_some-resource"
    haproxy_backends:
      - name: "some-resource"
        balance_algorythm: "roundrobin"
        weight_by_the_closest: true
        weight_of_the_nearest_backend: 100
        weight_of_the_far_backend: 5
        options:
          - name: "option"
            value: "httpchk"
          - name: "http-check"
            value: "send meth GET uri /some_endpoint/login.jsp"
          - name: "http-check"
            value: "expect status 200"  # you can have more powerful healthchecks if needed
        forward:  # list of servers to which balancer forwards incoming requests
          - name: "some-resourse-host1"
            uri: "some-resourse-host1.local:8080"
            check: true
            weight: 50
          - name: "some-resourse-host2"
            uri: "some-resourse-host2.local:8080"
            check: true
            weight: 50     
    haproxy_sysctl_vars:
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
      serial: 1
```

By setting flags and values, listed above or in defaults folder of the role, you can template almost all options for your haproxy instance. 

Several files will be created in configuration folder /etc/haproxy:
01.haproxy_global.cfg
02.haproxy_system_frontend.cfg
03.frontend1.cfg
03.frontend2.cfg
....
03.frontendN.cfg
04.backend1.cfg
04.backend2.cfg
...
04.backendM.cfg

This system of namings is absolutely necessary, because haproxy parses its settings folder in alphabetical order :D
