# Установка java
Переменные: 
 - java_version в виде "8u308" (по-умолчанию), 
 - java origin: "zulu" (zulu или jdk)
Пример использования: 

```yaml
- name: include_role java-role
  include_role:
    name: java-role
  vars:
    java_origin: "zulu"
    java_version: "8u308"
