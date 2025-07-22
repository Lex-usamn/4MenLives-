"""
Serviços de integração com plataformas de streaming
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class PlatformIntegrationService:
    """Classe base para integração com plataformas de streaming"""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.base_url = ""
        self.headers = {}
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com a plataforma"""
        raise NotImplementedError
        
    def get_stream_key(self) -> Optional[str]:
        """Obtém a chave de stream"""
        raise NotImplementedError
        
    def get_rtmp_url(self) -> Optional[str]:
        """Obtém a URL RTMP para streaming"""
        raise NotImplementedError
        
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém o status atual do stream"""
        raise NotImplementedError
        
    def get_viewer_count(self) -> int:
        """Obtém o número de visualizadores"""
        raise NotImplementedError
        
    def start_stream(self, title: str = "", description: str = "") -> bool:
        """Inicia o stream"""
        raise NotImplementedError
        
    def stop_stream(self) -> bool:
        """Para o stream"""
        raise NotImplementedError

class TwitchIntegration(PlatformIntegrationService):
    """Integração com Twitch"""
    
    def __init__(self):
        super().__init__("twitch")
        self.base_url = "https://api.twitch.tv/helix"
        self.client_id = None
        self.access_token = None
        self.broadcaster_id = None
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com Twitch usando OAuth"""
        try:
            self.client_id = credentials.get("client_id")
            self.access_token = credentials.get("access_token")
            
            if not self.client_id or not self.access_token:
                return False
                
            # Validar token e obter broadcaster_id
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Client-Id": self.client_id
            }
            
            response = requests.get(f"{self.base_url}/users", headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    self.broadcaster_id = data["data"][0]["id"]
                    self.headers = headers
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na autenticação Twitch: {e}")
            return False
    
    def get_stream_key(self) -> Optional[str]:
        """Obtém a chave de stream do Twitch"""
        try:
            if not self.broadcaster_id:
                return None
                
            url = f"{self.base_url}/streams/key"
            params = {"broadcaster_id": self.broadcaster_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    return data["data"][0]["stream_key"]
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao obter stream key Twitch: {e}")
            return None
    
    def get_rtmp_url(self) -> Optional[str]:
        """Obtém URL RTMP do Twitch"""
        try:
            # Obter servidor de ingest recomendado
            response = requests.get("https://ingest.twitch.tv/ingests")
            if response.status_code == 200:
                data = response.json()
                if data.get("ingests"):
                    # Usar o primeiro servidor disponível
                    ingest_server = data["ingests"][0]["url_template"]
                    return ingest_server.replace("{stream_key}", "")
            
            # Fallback para servidor padrão
            return "rtmp://live.twitch.tv/app/"
            
        except Exception as e:
            logger.error(f"Erro ao obter RTMP URL Twitch: {e}")
            return "rtmp://live.twitch.tv/app/"
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém status do stream Twitch"""
        try:
            if not self.broadcaster_id:
                return {"is_live": False, "viewer_count": 0}
                
            url = f"{self.base_url}/streams"
            params = {"user_id": self.broadcaster_id}
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    stream_data = data["data"][0]
                    return {
                        "is_live": True,
                        "viewer_count": stream_data.get("viewer_count", 0),
                        "title": stream_data.get("title", ""),
                        "game_name": stream_data.get("game_name", ""),
                        "started_at": stream_data.get("started_at")
                    }
            
            return {"is_live": False, "viewer_count": 0}
            
        except Exception as e:
            logger.error(f"Erro ao obter status Twitch: {e}")
            return {"is_live": False, "viewer_count": 0}
    
    def get_viewer_count(self) -> int:
        """Obtém número de visualizadores"""
        status = self.get_stream_status()
        return status.get("viewer_count", 0)

class YouTubeIntegration(PlatformIntegrationService):
    """Integração com YouTube Live"""
    
    def __init__(self):
        super().__init__("youtube")
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.api_key = None
        self.access_token = None
        self.channel_id = None
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com YouTube"""
        try:
            self.api_key = credentials.get("api_key")
            self.access_token = credentials.get("access_token")
            
            if not self.api_key or not self.access_token:
                return False
                
            # Validar token e obter channel_id
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {"part": "id", "mine": "true", "key": self.api_key}
            
            response = requests.get(f"{self.base_url}/channels", headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("items"):
                    self.channel_id = data["items"][0]["id"]
                    self.headers = headers
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro na autenticação YouTube: {e}")
            return False
    
    def create_broadcast(self, title: str, description: str = "") -> Optional[str]:
        """Cria um broadcast no YouTube"""
        try:
            url = f"{self.base_url}/liveBroadcasts"
            params = {"part": "snippet,status", "key": self.api_key}
            
            data = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "scheduledStartTime": datetime.utcnow().isoformat() + "Z"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }
            
            response = requests.post(url, headers=self.headers, params=params, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get("id")
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar broadcast YouTube: {e}")
            return None
    
    def create_stream(self, title: str) -> Optional[Dict[str, str]]:
        """Cria um stream no YouTube"""
        try:
            url = f"{self.base_url}/liveStreams"
            params = {"part": "snippet,cdn", "key": self.api_key}
            
            data = {
                "snippet": {
                    "title": title
                },
                "cdn": {
                    "format": "1080p",
                    "ingestionType": "rtmp"
                }
            }
            
            response = requests.post(url, headers=self.headers, params=params, json=data)
            if response.status_code == 200:
                result = response.json()
                return {
                    "stream_id": result.get("id"),
                    "stream_name": result["cdn"]["ingestionInfo"]["streamName"],
                    "rtmp_url": result["cdn"]["ingestionInfo"]["ingestionAddress"]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar stream YouTube: {e}")
            return None
    
    def get_rtmp_url(self) -> Optional[str]:
        """Obtém URL RTMP do YouTube"""
        # YouTube usa URLs dinâmicas, precisa criar stream primeiro
        return "rtmp://a.rtmp.youtube.com/live2/"
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém status do stream YouTube"""
        try:
            if not self.channel_id:
                return {"is_live": False, "viewer_count": 0}
                
            url = f"{self.base_url}/search"
            params = {
                "part": "id",
                "channelId": self.channel_id,
                "eventType": "live",
                "type": "video",
                "key": self.api_key
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("items"):
                    # Há streams ao vivo
                    video_id = data["items"][0]["id"]["videoId"]
                    
                    # Obter detalhes do vídeo
                    video_url = f"{self.base_url}/videos"
                    video_params = {
                        "part": "liveStreamingDetails,snippet",
                        "id": video_id,
                        "key": self.api_key
                    }
                    
                    video_response = requests.get(video_url, headers=self.headers, params=video_params)
                    if video_response.status_code == 200:
                        video_data = video_response.json()
                        if video_data.get("items"):
                            item = video_data["items"][0]
                            return {
                                "is_live": True,
                                "viewer_count": int(item.get("liveStreamingDetails", {}).get("concurrentViewers", 0)),
                                "title": item.get("snippet", {}).get("title", ""),
                                "started_at": item.get("liveStreamingDetails", {}).get("actualStartTime")
                            }
            
            return {"is_live": False, "viewer_count": 0}
            
        except Exception as e:
            logger.error(f"Erro ao obter status YouTube: {e}")
            return {"is_live": False, "viewer_count": 0}

class FacebookIntegration(PlatformIntegrationService):
    """Integração com Facebook Live"""
    
    def __init__(self):
        super().__init__("facebook")
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = None
        self.page_id = None
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com Facebook"""
        try:
            self.access_token = credentials.get("access_token")
            self.page_id = credentials.get("page_id")
            
            if not self.access_token or not self.page_id:
                return False
                
            # Validar token
            params = {"access_token": self.access_token}
            response = requests.get(f"{self.base_url}/me", params=params)
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Erro na autenticação Facebook: {e}")
            return False
    
    def create_live_video(self, title: str, description: str = "") -> Optional[Dict[str, str]]:
        """Cria um vídeo ao vivo no Facebook"""
        try:
            url = f"{self.base_url}/{self.page_id}/live_videos"
            params = {"access_token": self.access_token}
            
            data = {
                "title": title,
                "description": description,
                "status": "LIVE_NOW"
            }
            
            response = requests.post(url, params=params, data=data)
            if response.status_code == 200:
                result = response.json()
                return {
                    "video_id": result.get("id"),
                    "stream_url": result.get("stream_url"),
                    "secure_stream_url": result.get("secure_stream_url")
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao criar live video Facebook: {e}")
            return None
    
    def get_rtmp_url(self) -> Optional[str]:
        """Obtém URL RTMP do Facebook"""
        # Facebook usa URLs dinâmicas, precisa criar live video primeiro
        return "rtmps://live-api-s.facebook.com:443/rtmp/"
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém status do stream Facebook"""
        try:
            if not self.page_id:
                return {"is_live": False, "viewer_count": 0}
                
            url = f"{self.base_url}/{self.page_id}/live_videos"
            params = {"access_token": self.access_token}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    # Verificar se há vídeos ao vivo ativos
                    for video in data["data"]:
                        if video.get("status") == "LIVE":
                            return {
                                "is_live": True,
                                "viewer_count": video.get("live_views", 0),
                                "title": video.get("title", ""),
                                "started_at": video.get("creation_time")
                            }
            
            return {"is_live": False, "viewer_count": 0}
            
        except Exception as e:
            logger.error(f"Erro ao obter status Facebook: {e}")
            return {"is_live": False, "viewer_count": 0}

class InstagramIntegration(PlatformIntegrationService):
    """Integração com Instagram Live"""
    
    def __init__(self):
        super().__init__("instagram")
        self.base_url = "https://graph.facebook.com/v18.0"
        self.access_token = None
        self.user_id = None
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com Instagram"""
        try:
            self.access_token = credentials.get("access_token")
            self.user_id = credentials.get("user_id")
            
            if not self.access_token or not self.user_id:
                return False
                
            # Validar token
            params = {"access_token": self.access_token}
            response = requests.get(f"{self.base_url}/{self.user_id}", params=params)
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Erro na autenticação Instagram: {e}")
            return False
    
    def get_rtmp_url(self) -> Optional[str]:
        """Obtém URL RTMP do Instagram"""
        # Instagram Live Producer usa URLs dinâmicas
        return "rtmps://live-upload.instagram.com/rtmp/"
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém status do stream Instagram"""
        try:
            if not self.user_id:
                return {"is_live": False, "viewer_count": 0}
                
            url = f"{self.base_url}/{self.user_id}/live_media"
            params = {"access_token": self.access_token}
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("data"):
                    # Instagram retorna apenas streams ativos
                    live_media = data["data"][0]
                    return {
                        "is_live": True,
                        "viewer_count": 0,  # Instagram não fornece contagem em tempo real
                        "title": "Instagram Live",
                        "started_at": live_media.get("timestamp")
                    }
            
            return {"is_live": False, "viewer_count": 0}
            
        except Exception as e:
            logger.error(f"Erro ao obter status Instagram: {e}")
            return {"is_live": False, "viewer_count": 0}

class TikTokIntegration(PlatformIntegrationService):
    """Integração com TikTok Live"""
    
    def __init__(self):
        super().__init__("tiktok")
        self.base_url = "https://open-api.tiktok.com"
        self.access_token = None
        self.user_id = None
        
    def authenticate(self, credentials: Dict[str, str]) -> bool:
        """Autentica com TikTok"""
        try:
            self.access_token = credentials.get("access_token")
            self.user_id = credentials.get("user_id")
            
            if not self.access_token or not self.user_id:
                return False
                
            # TikTok tem API limitada para live streaming
            # Principalmente para leitura de dados, não para streaming direto
            return True
            
        except Exception as e:
            logger.error(f"Erro na autenticação TikTok: {e}")
            return False
    
    def get_rtmp_url(self) -> Optional[str]:
        """TikTok não suporta RTMP direto via API pública"""
        # TikTok Live requer uso do app móvel ou ferramentas específicas
        return None
    
    def get_stream_status(self) -> Dict[str, Any]:
        """Obtém status do stream TikTok"""
        # TikTok API pública não fornece status de live streaming
        return {"is_live": False, "viewer_count": 0}

class PlatformManager:
    """Gerenciador de todas as integrações de plataformas"""
    
    def __init__(self):
        self.platforms = {
            "twitch": TwitchIntegration(),
            "youtube": YouTubeIntegration(),
            "facebook": FacebookIntegration(),
            "instagram": InstagramIntegration(),
            "tiktok": TikTokIntegration()
        }
        
    def get_platform(self, platform_name: str) -> Optional[PlatformIntegrationService]:
        """Obtém integração de uma plataforma específica"""
        return self.platforms.get(platform_name.lower())
    
    def authenticate_platform(self, platform_name: str, credentials: Dict[str, str]) -> bool:
        """Autentica com uma plataforma específica"""
        platform = self.get_platform(platform_name)
        if platform:
            return platform.authenticate(credentials)
        return False
    
    def get_all_stream_status(self) -> Dict[str, Dict[str, Any]]:
        """Obtém status de todas as plataformas autenticadas"""
        status = {}
        for name, platform in self.platforms.items():
            try:
                status[name] = platform.get_stream_status()
            except Exception as e:
                logger.error(f"Erro ao obter status {name}: {e}")
                status[name] = {"is_live": False, "viewer_count": 0, "error": str(e)}
        
        return status
    
    def get_total_viewers(self) -> int:
        """Obtém total de visualizadores em todas as plataformas"""
        total = 0
        for platform in self.platforms.values():
            try:
                total += platform.get_viewer_count()
            except Exception:
                continue
        
        return total
    
    def get_rtmp_endpoints(self) -> Dict[str, Dict[str, str]]:
        """Obtém endpoints RTMP de todas as plataformas"""
        endpoints = {}
        for name, platform in self.platforms.items():
            try:
                rtmp_url = platform.get_rtmp_url()
                stream_key = platform.get_stream_key() if hasattr(platform, 'get_stream_key') else None
                
                if rtmp_url:
                    endpoints[name] = {
                        "rtmp_url": rtmp_url,
                        "stream_key": stream_key or "CONFIGURE_IN_PLATFORM"
                    }
            except Exception as e:
                logger.error(f"Erro ao obter RTMP {name}: {e}")
        
        return endpoints

