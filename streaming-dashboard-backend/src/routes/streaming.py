"""
Rotas para controle de streaming multicast
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.platform_integrations import PlatformManager
from src.models.platform import Platform
from src.models.user import User
import json
import logging

logger = logging.getLogger(__name__)

streaming_bp = Blueprint('streaming', __name__)
platform_manager = PlatformManager()

@streaming_bp.route('/platforms', methods=['GET'])
@jwt_required()
def get_platforms():
    """Lista todas as plataformas disponíveis"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "Usuário não encontrado"}), 404
        
        # Obter plataformas configuradas pelo usuário
        user_platforms = Platform.query.filter_by(user_id=user_id).all()
        
        platforms_data = []
        for platform in user_platforms:
            # Descriptografar credenciais
            credentials = json.loads(platform.decrypt_credentials())
            
            # Autenticar com a plataforma
            is_authenticated = platform_manager.authenticate_platform(
                platform.name, credentials
            )
            
            # Obter status do stream
            platform_service = platform_manager.get_platform(platform.name)
            status = {"is_live": False, "viewer_count": 0}
            rtmp_info = {"rtmp_url": "", "stream_key": ""}
            
            if is_authenticated and platform_service:
                status = platform_service.get_stream_status()
                rtmp_url = platform_service.get_rtmp_url()
                stream_key = platform_service.get_stream_key() if hasattr(platform_service, 'get_stream_key') else None
                
                rtmp_info = {
                    "rtmp_url": rtmp_url or "",
                    "stream_key": stream_key or "CONFIGURE_IN_PLATFORM"
                }
            
            platforms_data.append({
                "id": platform.id,
                "name": platform.name,
                "display_name": platform.display_name,
                "is_active": platform.is_active,
                "is_authenticated": is_authenticated,
                "status": status,
                "rtmp_info": rtmp_info,
                "created_at": platform.created_at.isoformat(),
                "updated_at": platform.updated_at.isoformat()
            })
        
        return jsonify({
            "platforms": platforms_data,
            "total_count": len(platforms_data)
        })
        
    except Exception as e:
        logger.error(f"Erro ao listar plataformas: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/platforms/<int:platform_id>/status', methods=['GET'])
@jwt_required()
def get_platform_status(platform_id):
    """Obtém status detalhado de uma plataforma específica"""
    try:
        user_id = get_jwt_identity()
        platform = Platform.query.filter_by(id=platform_id, user_id=user_id).first()
        
        if not platform:
            return jsonify({"error": "Plataforma não encontrada"}), 404
        
        # Descriptografar credenciais e autenticar
        credentials = json.loads(platform.decrypt_credentials())
        is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
        
        if not is_authenticated:
            return jsonify({
                "error": "Falha na autenticação com a plataforma",
                "platform": platform.name
            }), 401
        
        # Obter serviço da plataforma
        platform_service = platform_manager.get_platform(platform.name)
        if not platform_service:
            return jsonify({"error": "Serviço da plataforma não disponível"}), 503
        
        # Obter status detalhado
        status = platform_service.get_stream_status()
        rtmp_url = platform_service.get_rtmp_url()
        stream_key = platform_service.get_stream_key() if hasattr(platform_service, 'get_stream_key') else None
        
        return jsonify({
            "platform": {
                "id": platform.id,
                "name": platform.name,
                "display_name": platform.display_name
            },
            "status": status,
            "rtmp_info": {
                "rtmp_url": rtmp_url or "",
                "stream_key": stream_key or "CONFIGURE_IN_PLATFORM"
            },
            "is_authenticated": True,
            "timestamp": platform.updated_at.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter status da plataforma {platform_id}: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/status/all', methods=['GET'])
@jwt_required()
def get_all_platforms_status():
    """Obtém status de todas as plataformas do usuário"""
    try:
        user_id = get_jwt_identity()
        user_platforms = Platform.query.filter_by(user_id=user_id, is_active=True).all()
        
        all_status = {}
        total_viewers = 0
        active_streams = 0
        
        for platform in user_platforms:
            try:
                # Descriptografar credenciais e autenticar
                credentials = json.loads(platform.decrypt_credentials())
                is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
                
                if is_authenticated:
                    platform_service = platform_manager.get_platform(platform.name)
                    if platform_service:
                        status = platform_service.get_stream_status()
                        all_status[platform.name] = {
                            "platform_id": platform.id,
                            "display_name": platform.display_name,
                            "status": status,
                            "is_authenticated": True
                        }
                        
                        # Somar visualizadores
                        if status.get("is_live"):
                            total_viewers += status.get("viewer_count", 0)
                            active_streams += 1
                    else:
                        all_status[platform.name] = {
                            "platform_id": platform.id,
                            "display_name": platform.display_name,
                            "status": {"is_live": False, "viewer_count": 0},
                            "is_authenticated": False,
                            "error": "Serviço não disponível"
                        }
                else:
                    all_status[platform.name] = {
                        "platform_id": platform.id,
                        "display_name": platform.display_name,
                        "status": {"is_live": False, "viewer_count": 0},
                        "is_authenticated": False,
                        "error": "Falha na autenticação"
                    }
                    
            except Exception as e:
                logger.error(f"Erro ao processar plataforma {platform.name}: {e}")
                all_status[platform.name] = {
                    "platform_id": platform.id,
                    "display_name": platform.display_name,
                    "status": {"is_live": False, "viewer_count": 0},
                    "is_authenticated": False,
                    "error": str(e)
                }
        
        return jsonify({
            "platforms": all_status,
            "summary": {
                "total_platforms": len(user_platforms),
                "active_streams": active_streams,
                "total_viewers": total_viewers,
                "timestamp": platform.updated_at.isoformat() if user_platforms else None
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter status de todas as plataformas: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/rtmp/endpoints', methods=['GET'])
@jwt_required()
def get_rtmp_endpoints():
    """Obtém endpoints RTMP de todas as plataformas configuradas"""
    try:
        user_id = get_jwt_identity()
        user_platforms = Platform.query.filter_by(user_id=user_id, is_active=True).all()
        
        endpoints = {}
        
        for platform in user_platforms:
            try:
                # Descriptografar credenciais e autenticar
                credentials = json.loads(platform.decrypt_credentials())
                is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
                
                if is_authenticated:
                    platform_service = platform_manager.get_platform(platform.name)
                    if platform_service:
                        rtmp_url = platform_service.get_rtmp_url()
                        stream_key = platform_service.get_stream_key() if hasattr(platform_service, 'get_stream_key') else None
                        
                        endpoints[platform.name] = {
                            "platform_id": platform.id,
                            "display_name": platform.display_name,
                            "rtmp_url": rtmp_url or "",
                            "stream_key": stream_key or "CONFIGURE_IN_PLATFORM",
                            "full_url": f"{rtmp_url}{stream_key}" if rtmp_url and stream_key else "",
                            "is_ready": bool(rtmp_url and stream_key)
                        }
                    
            except Exception as e:
                logger.error(f"Erro ao obter RTMP para {platform.name}: {e}")
                endpoints[platform.name] = {
                    "platform_id": platform.id,
                    "display_name": platform.display_name,
                    "rtmp_url": "",
                    "stream_key": "",
                    "full_url": "",
                    "is_ready": False,
                    "error": str(e)
                }
        
        return jsonify({
            "endpoints": endpoints,
            "total_count": len(endpoints)
        })
        
    except Exception as e:
        logger.error(f"Erro ao obter endpoints RTMP: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/multicast/start', methods=['POST'])
@jwt_required()
def start_multicast():
    """Inicia streaming multicast para todas as plataformas ativas"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title', 'Live Stream')
        description = data.get('description', '')
        selected_platforms = data.get('platforms', [])  # Lista de IDs ou nomes de plataformas
        
        user_platforms = Platform.query.filter_by(user_id=user_id, is_active=True).all()
        
        # Filtrar plataformas selecionadas se especificado
        if selected_platforms:
            user_platforms = [p for p in user_platforms if p.id in selected_platforms or p.name in selected_platforms]
        
        results = {}
        successful_starts = 0
        
        for platform in user_platforms:
            try:
                # Descriptografar credenciais e autenticar
                credentials = json.loads(platform.decrypt_credentials())
                is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
                
                if is_authenticated:
                    platform_service = platform_manager.get_platform(platform.name)
                    if platform_service and hasattr(platform_service, 'start_stream'):
                        success = platform_service.start_stream(title, description)
                        results[platform.name] = {
                            "success": success,
                            "message": "Stream iniciado com sucesso" if success else "Falha ao iniciar stream"
                        }
                        if success:
                            successful_starts += 1
                    else:
                        results[platform.name] = {
                            "success": False,
                            "message": "Plataforma não suporta início automático de stream"
                        }
                else:
                    results[platform.name] = {
                        "success": False,
                        "message": "Falha na autenticação"
                    }
                    
            except Exception as e:
                logger.error(f"Erro ao iniciar stream em {platform.name}: {e}")
                results[platform.name] = {
                    "success": False,
                    "message": f"Erro: {str(e)}"
                }
        
        return jsonify({
            "results": results,
            "summary": {
                "total_platforms": len(user_platforms),
                "successful_starts": successful_starts,
                "failed_starts": len(user_platforms) - successful_starts
            },
            "message": f"Multicast iniciado em {successful_starts}/{len(user_platforms)} plataformas"
        })
        
    except Exception as e:
        logger.error(f"Erro ao iniciar multicast: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/multicast/stop', methods=['POST'])
@jwt_required()
def stop_multicast():
    """Para streaming multicast em todas as plataformas ativas"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        selected_platforms = data.get('platforms', [])
        
        user_platforms = Platform.query.filter_by(user_id=user_id, is_active=True).all()
        
        # Filtrar plataformas selecionadas se especificado
        if selected_platforms:
            user_platforms = [p for p in user_platforms if p.id in selected_platforms or p.name in selected_platforms]
        
        results = {}
        successful_stops = 0
        
        for platform in user_platforms:
            try:
                # Descriptografar credenciais e autenticar
                credentials = json.loads(platform.decrypt_credentials())
                is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
                
                if is_authenticated:
                    platform_service = platform_manager.get_platform(platform.name)
                    if platform_service and hasattr(platform_service, 'stop_stream'):
                        success = platform_service.stop_stream()
                        results[platform.name] = {
                            "success": success,
                            "message": "Stream parado com sucesso" if success else "Falha ao parar stream"
                        }
                        if success:
                            successful_stops += 1
                    else:
                        results[platform.name] = {
                            "success": False,
                            "message": "Plataforma não suporta parada automática de stream"
                        }
                else:
                    results[platform.name] = {
                        "success": False,
                        "message": "Falha na autenticação"
                    }
                    
            except Exception as e:
                logger.error(f"Erro ao parar stream em {platform.name}: {e}")
                results[platform.name] = {
                    "success": False,
                    "message": f"Erro: {str(e)}"
                }
        
        return jsonify({
            "results": results,
            "summary": {
                "total_platforms": len(user_platforms),
                "successful_stops": successful_stops,
                "failed_stops": len(user_platforms) - successful_stops
            },
            "message": f"Multicast parado em {successful_stops}/{len(user_platforms)} plataformas"
        })
        
    except Exception as e:
        logger.error(f"Erro ao parar multicast: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

@streaming_bp.route('/obs/config', methods=['GET'])
@jwt_required()
def get_obs_config():
    """Gera configuração para OBS Studio com múltiplos outputs RTMP"""
    try:
        user_id = get_jwt_identity()
        user_platforms = Platform.query.filter_by(user_id=user_id, is_active=True).all()
        
        obs_outputs = []
        
        for platform in user_platforms:
            try:
                # Descriptografar credenciais e autenticar
                credentials = json.loads(platform.decrypt_credentials())
                is_authenticated = platform_manager.authenticate_platform(platform.name, credentials)
                
                if is_authenticated:
                    platform_service = platform_manager.get_platform(platform.name)
                    if platform_service:
                        rtmp_url = platform_service.get_rtmp_url()
                        stream_key = platform_service.get_stream_key() if hasattr(platform_service, 'get_stream_key') else None
                        
                        if rtmp_url and stream_key:
                            obs_outputs.append({
                                "name": f"{platform.display_name} Stream",
                                "type": "rtmp_output",
                                "settings": {
                                    "server": rtmp_url,
                                    "key": stream_key,
                                    "use_auth": False
                                },
                                "platform": platform.name,
                                "platform_id": platform.id
                            })
                        
            except Exception as e:
                logger.error(f"Erro ao gerar config OBS para {platform.name}: {e}")
        
        # Configuração completa do OBS
        obs_config = {
            "version": "1.0",
            "multicast_outputs": obs_outputs,
            "recommended_settings": {
                "video": {
                    "base_resolution": "1920x1080",
                    "output_resolution": "1920x1080",
                    "fps": 30
                },
                "audio": {
                    "sample_rate": 44100,
                    "channels": 2
                },
                "encoding": {
                    "video_encoder": "x264",
                    "audio_encoder": "aac",
                    "video_bitrate": 2500,
                    "audio_bitrate": 128
                }
            },
            "instructions": [
                "1. Abra o OBS Studio",
                "2. Vá em Configurações > Stream",
                "3. Configure cada plataforma como um serviço personalizado",
                "4. Use as URLs e chaves fornecidas",
                "5. Para multicast, use plugins como 'Multiple RTMP outputs'"
            ]
        }
        
        return jsonify(obs_config)
        
    except Exception as e:
        logger.error(f"Erro ao gerar configuração OBS: {e}")
        return jsonify({"error": "Erro interno do servidor"}), 500

