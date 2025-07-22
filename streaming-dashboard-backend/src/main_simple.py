from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)

# Configuração CORS para permitir acesso de qualquer origem
CORS(app, origins="*")

# Configuração básica
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Dados simulados para demonstração
platforms_data = {
    'twitch': {'name': 'Twitch', 'connected': True, 'viewers': 1247, 'status': 'OFFLINE'},
    'youtube': {'name': 'YouTube', 'connected': True, 'viewers': 3521, 'status': 'OFFLINE'},
    'facebook': {'name': 'Facebook', 'connected': True, 'viewers': 892, 'status': 'OFFLINE'},
    'tiktok': {'name': 'TikTok', 'connected': False, 'viewers': 0, 'status': 'OFFLINE'},
    'instagram': {'name': 'Instagram', 'connected': True, 'viewers': 654, 'status': 'OFFLINE'}
}

guests_data = [
    {'id': 1, 'name': 'João Silva', 'status': 'connected', 'latency': 45},
    {'id': 2, 'name': 'Maria Santos', 'status': 'connected', 'latency': 67},
    {'id': 3, 'name': 'Pedro Costa', 'status': 'disconnected', 'latency': 0}
]

streaming_status = {'active': False, 'start_time': None}

@app.route('/')
def index():
    return jsonify({
        'message': 'Dashboard de Streaming Multicast API',
        'version': '1.0',
        'status': 'running'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

# Rotas de autenticação simplificadas
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Autenticação simples para demonstração
    if username == 'admin' and password == '123456':
        return jsonify({
            'success': True,
            'token': 'demo-token-12345',
            'user': {'id': 1, 'username': 'admin', 'email': 'admin@example.com'}
        })
    else:
        return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify({
        'success': True,
        'message': 'Usuário registrado com sucesso',
        'user': {'id': 2, 'username': data.get('username'), 'email': data.get('email')}
    })

# Rotas de usuários
@app.route('/api/users')
def get_users():
    return jsonify([
        {'id': 1, 'username': 'admin', 'email': 'admin@example.com', 'created_at': '2025-01-01'}
    ])

# Rotas de plataformas
@app.route('/api/platforms')
def get_platforms():
    return jsonify(list(platforms_data.values()))

@app.route('/api/platforms/<platform_id>', methods=['PUT'])
def update_platform(platform_id):
    if platform_id in platforms_data:
        data = request.get_json()
        platforms_data[platform_id].update(data)
        return jsonify(platforms_data[platform_id])
    return jsonify({'error': 'Platform not found'}), 404

# Rotas de convidados
@app.route('/api/guests')
def get_guests():
    return jsonify(guests_data)

@app.route('/api/guests', methods=['POST'])
def create_guest():
    data = request.get_json()
    new_guest = {
        'id': len(guests_data) + 1,
        'name': data.get('name'),
        'status': 'disconnected',
        'latency': 0,
        'token': f'guest-token-{len(guests_data) + 1}'
    }
    guests_data.append(new_guest)
    return jsonify(new_guest)

@app.route('/api/guests/<int:guest_id>', methods=['DELETE'])
def delete_guest(guest_id):
    global guests_data
    guests_data = [g for g in guests_data if g['id'] != guest_id]
    return jsonify({'success': True})

# Rotas de streaming
@app.route('/api/streaming/status')
def get_streaming_status():
    return jsonify(streaming_status)

@app.route('/api/streaming/start', methods=['POST'])
def start_streaming():
    global streaming_status, platforms_data
    streaming_status['active'] = True
    streaming_status['start_time'] = datetime.now().isoformat()
    
    # Atualizar status das plataformas conectadas
    for platform in platforms_data.values():
        if platform['connected']:
            platform['status'] = 'AO VIVO'
    
    return jsonify({'success': True, 'status': streaming_status})

@app.route('/api/streaming/stop', methods=['POST'])
def stop_streaming():
    global streaming_status, platforms_data
    streaming_status['active'] = False
    streaming_status['start_time'] = None
    
    # Atualizar status das plataformas
    for platform in platforms_data.values():
        platform['status'] = 'OFFLINE'
    
    return jsonify({'success': True, 'status': streaming_status})

@app.route('/api/streaming/platforms')
def get_streaming_platforms():
    return jsonify(list(platforms_data.values()))

# Rotas de análises
@app.route('/api/analytics/viewers')
def get_viewers_analytics():
    return jsonify({
        'total_viewers': sum(p['viewers'] for p in platforms_data.values()),
        'by_platform': {k: v['viewers'] for k, v in platforms_data.items()},
        'history': [
            {'time': '10:00', 'viewers': 1200},
            {'time': '10:05', 'viewers': 1350},
            {'time': '10:10', 'viewers': 1420},
            {'time': '10:15', 'viewers': 1580},
            {'time': '10:20', 'viewers': 1720},
            {'time': '10:25', 'viewers': 1890},
            {'time': '10:30', 'viewers': 2100}
        ]
    })

@app.route('/api/analytics/latency')
def get_latency_analytics():
    return jsonify({
        'guests': [
            {'name': 'João', 'latency': 45},
            {'name': 'Maria', 'latency': 67},
            {'name': 'Pedro', 'latency': 0}
        ],
        'average': 37.3
    })

# Configuração para servir arquivos estáticos (se necessário)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

