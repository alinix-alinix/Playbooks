# -*- coding: utf-8 -*-
import http.server
import os
import base64
from datetime import datetime

USERNAME = '{{ dir_exposer_username }}'
PASSWORD = '{{ dir_exposer_password }}'

class AuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET запроса с базовой аутентификацией"""
        if self._send_authentication_header():
            return  # Если аутентификация не пройдена, возвращаем из метода

        # Логика листинга файлов в папке
        base_directory = '{{ dir_exposer_dir_to_expose }}'  # Папка, из которой выводятся файлы
        requested_path = self.path.strip('/')  # Убираем слеши в начале и в конце пути
        if not requested_path:
            requested_path = '.'  # если не указан путь, показываем корень

        # Полный путь к файлу или папке
        directory_path = os.path.join(base_directory, requested_path)

        # Если запрашиваемый путь не существует или не является директорией, проверяем, файл ли это
        if not os.path.exists(directory_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Directory or file not found.'.encode())
            return

        # Если это файл, отдаем его
        if os.path.isfile(directory_path):
            self._send_file(directory_path)
            return

        # Если это папка, выводим список файлов
        if os.path.isdir(directory_path):
            self._send_directory_listing(directory_path, requested_path)
            return

    def _send_file(self, file_path):
        """Отправка содержимого файла"""
        self.send_response(200)
        self.send_header('Content-type', 'application/octet-stream')  # Определите тип контента в зависимости от файлов
        self.send_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
        self.end_headers()

        with open(file_path, 'rb') as file:
            self.wfile.write(file.read())

    def _send_directory_listing(self, directory_path, requested_path):
        """Отправка листинга файлов в директории"""
        files = os.listdir(directory_path)
        files.sort()  # Сортируем файлы

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Формируем HTML-страницу с файлами и папками
        self.wfile.write('<html><body><h1>Directory Listing</h1><table border="1"><tr><th>Name</th><th>Size</th><th>Last modified</th></tr>'.encode())

        for filename in files:
            file_path = os.path.join(directory_path, filename)
            file_size = os.path.getsize(file_path)
            file_mtime = os.path.getmtime(file_path)
            # Используем локальное время
            file_mtime_str = datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')

            # Проверка, является ли объект директорией
            if os.path.isdir(file_path):
                # Для папок создаем ссылку для перехода в эту папку
                self.wfile.write(f'<tr><td><a href="/{requested_path}/{filename}/">{filename}</a></td><td>-</td><td>{file_mtime_str}</td></tr>'.encode())
            else:
                # Для файлов создаем ссылку для скачивания
                self.wfile.write(f'<tr><td><a href="/{requested_path}/{filename}">{filename}</a></td><td>{file_size} bytes</td><td>{file_mtime_str}</td></tr>'.encode())

        self.wfile.write('</table></body></html>'.encode())  # Закрываем HTML

    def _send_authentication_header(self):
        """Проверка аутентификации с использованием Basic Auth"""
        auth = self.headers.get('Authorization')
        if auth is None or not self._is_authenticated(auth):
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Restricted Area"')
            self.end_headers()
            self.wfile.write('Authentication required.'.encode())
            return True  # Не прошел аутентификацию
        return False  # Пройдено

    def _is_authenticated(self, auth):
        """Проверка введенных логина и пароля"""
        auth_type, auth_string = auth.split(' ', 1)
        if auth_type.lower() != 'basic':
            return False

        try:
            auth_string = base64.b64decode(auth_string.strip()).decode('utf-8')  # decode для Python 3
            username, password = auth_string.split(':', 1)
        except (ValueError, TypeError):
            return False

        return username == USERNAME and password == PASSWORD

if __name__ == "__main__":
    os.chdir('{{ dir_exposer_dir_to_expose }}')  # Указываем нужный каталог
    server_address = ('', {{ dir_exposer_listen_port }})  # Указываем порт
    httpd = http.server.HTTPServer(server_address, AuthHandler)
    print("Serving at port {{ dir_exposer_listen_port }}...")
    httpd.serve_forever()
