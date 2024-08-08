# Role installs and setups the logrotate. For importing in other roles, or to be used on it's own

Example:

```yaml
- name: setup logrotate
  include_role:
    name: logrotate_role
  vars:
    logrotate_retention_days: 10  # logs retention period
    logrotate_period: "daily"  # How often to rotate daily or hourly
    logrotate_filename: "test" # logrotate filename. That file will be created in /etc/logrotate.d folder
    logrotate_task_list:  # we can add one or more masks to rotate
    - log_file_mask: "/opt/tomcat/logs/catalina.out"  # file mask to rotate
      switch_user:  # if required, state user to which it's necesary to switch to
      copytruncate: true 
      nocreate: false
      notifempty: true
      compress: true
      missingok : true
      postrorate: true  # if this option is set "true", postrotate script is required
      postrotate_script: 'find /var/log/tomcat{{ global_tomcat_version }}/ \( -name \*.log -o -name \*.gz -o -name \*.txt \) -mtime +5 -type "f" -exec rm -rfv {} \;'
```

logrotate_period and logrotate_filename values are strictly checked:
1.logrotate_period has to be set with "daily/horly" value. No other option is acceptable.
2.logrotate_filename has to contain not-empty string.

If logrotate_period option is set to "hourly",  role will create logrotate-hourly.timer unit in default systemd folder.
Certain rotation parameters like filename, retention period or logrotate period are global for all the following tasks in the file created by the role.
