#!/usr/bin/env python3
"""
Простой HTTP сервер для демонстрации фронтенда создания профиля
"""

import json
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import cgi

class ProfileHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """Обработка POST запросов для создания профиля"""
        if self.path == '/api/profile/create':
            self.handle_create_profile()
        else:
            self.send_error(404, "Endpoint not found")
    
    def handle_create_profile(self):
        """Обработка создания профиля"""
        try:
            # Получаем размер контента
            content_length = int(self.headers.get('Content-Length', 0))
            
            # Читаем данные
            post_data = self.rfile.read(content_length)
            
            # Парсим JSON
            profile_data = json.loads(post_data.decode('utf-8'))
            
            # Валидация данных
            validation_result = self.validate_profile_data(profile_data)
            
            if validation_result['valid']:
                # В реальном приложении здесь была бы запись в базу данных
                profile_id = self.save_profile(profile_data)
                
                # Отправляем успешный ответ
                response = {
                    'success': True,
                    'message': 'Профиль успешно создан',
                    'profile_id': profile_id
                }
                self.send_response(200)
            else:
                # Отправляем ошибку валидации
                response = {
                    'success': False,
                    'message': validation_result['message']
                }
                self.send_response(400)
            
            # Отправляем заголовки
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            # Отправляем ответ
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
        except Exception as e:
            print(f"Error processing request: {e}")
            self.send_error(500, "Internal server error")
    
    def validate_profile_data(self, data):
        """Валидация данных профиля"""
        required_fields = [
            'name', 'surname', 'gender', 'age', 'city', 
            'ethnicity', 'religion', 'religious_level', 'education',
            'height', 'weight', 'marital_status', 'has_children', 
            'polygamy', 'goal'
        ]
        
        # Проверяем обязательные поля
        for field in required_fields:
            if field not in data or data[field] is None:
                return {
                    'valid': False,
                    'message': f'Поле "{field}" обязательно для заполнения'
                }
        
        # Проверяем возраст
        if not isinstance(data['age'], int) or data['age'] < 18 or data['age'] > 100:
            return {
                'valid': False,
                'message': 'Возраст должен быть от 18 до 100 лет'
            }
        
        # Проверяем рост
        if not isinstance(data['height'], int) or data['height'] < 100 or data['height'] > 250:
            return {
                'valid': False,
                'message': 'Рост должен быть от 100 до 250 см'
            }
        
        # Проверяем вес
        if not isinstance(data['weight'], int) or data['weight'] < 30 or data['weight'] > 200:
            return {
                'valid': False,
                'message': 'Вес должен быть от 30 до 200 кг'
            }
        
        # Проверяем пол
        if data['gender'] not in ['male', 'female']:
            return {
                'valid': False,
                'message': 'Пол должен быть male или female'
            }
        
        # Проверяем семейное положение
        if data['marital_status'] not in ['single', 'divorced', 'widowed']:
            return {
                'valid': False,
                'message': 'Некорректное семейное положение'
            }
        
        # Проверяем образование
        if data['education'] not in ['none', 'secondary', 'higher']:
            return {
                'valid': False,
                'message': 'Некорректный уровень образования'
            }
        
        # Проверяем цель знакомства
        if data['goal'] not in ['friendship', 'communication', 'marriage']:
            return {
                'valid': False,
                'message': 'Некорректная цель знакомства'
            }
        
        return {'valid': True}
    
    def save_profile(self, data):
        """Сохранение профиля (демонстрационная функция)"""
        # В реальном приложении здесь была бы запись в базу данных
        import random
        profile_id = random.randint(1000, 9999)
        
        # Сохраняем в файл для демонстрации
        profiles_file = 'profiles.json'
        profiles = []
        
        if os.path.exists(profiles_file):
            try:
                with open(profiles_file, 'r', encoding='utf-8') as f:
                    profiles = json.load(f)
            except:
                profiles = []
        
        # Добавляем новый профиль
        profile_record = {
            'id': profile_id,
            'data': data,
            'created_at': '2024-01-01T00:00:00Z'  # В реальном приложении использовался бы datetime
        }
        
        profiles.append(profile_record)
        
        # Сохраняем в файл
        with open(profiles_file, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        
        print(f"Profile created with ID: {profile_id}")
        return profile_id
    
    def do_OPTIONS(self):
        """Обработка CORS preflight запросов"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        """Добавляем CORS заголовки ко всем ответам"""
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

def run_server(port=8000):
    """Запуск сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ProfileHandler)
    print(f"Сервер запущен на порту {port}")
    print(f"Откройте http://localhost:{port} в браузере")
    print("Для остановки сервера нажмите Ctrl+C")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()

if __name__ == '__main__':
    import sys
    
    # Определяем порт из аргументов командной строки
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Порт должен быть числом")
            sys.exit(1)
    
    run_server(port) 