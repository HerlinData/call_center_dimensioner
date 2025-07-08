"""
Manejo de autenticación segura para Flet
"""

from typing import Optional
from datetime import datetime, timedelta
import hashlib
import os
import secrets
import bcrypt
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class AuthManager:
    """Gestor de autenticación segura para Flet"""
    
    def __init__(self):
        self.access_key = os.getenv('ACCESS_KEY', 'by_hyb')
        self.max_attempts = 3
        self.session_timeout = 3600  # 1 hora en segundos
        
        # Estado de sesión en memoria (para Flet)
        self.session_state = {
            'authenticated': False,
            'login_time': None,
            'attempts': 0,
            'last_attempt': None,
            'blocked_until': None
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash de contraseña usando bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verificar contraseña contra hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def _is_blocked(self) -> tuple[bool, Optional[datetime]]:
        """Verificar si la cuenta está bloqueada"""
        attempts = self.session_state.get('attempts', 0)
        last_attempt = self.session_state.get('last_attempt')
        
        if attempts >= self.max_attempts and last_attempt:
            # Bloqueo por 15 minutos después de 3 intentos fallidos
            block_until = last_attempt + timedelta(minutes=15)
            if datetime.now() < block_until:
                return True, block_until
            else:
                # Reset después del bloqueo
                self.session_state['attempts'] = 0
                return False, None
        
        return False, None
    
    def authenticate(self, password: str) -> tuple[bool, str]:
        """
        Autenticar usuario
        Retorna: (éxito, mensaje)
        """
        # Verificar bloqueo
        is_blocked, block_until = self._is_blocked()
        if is_blocked:
            remaining = block_until - datetime.now()
            minutes = int(remaining.total_seconds() / 60)
            return False, f"🔒 Cuenta bloqueada. Intenta en {minutes} minutos."
        
        # Verificar contraseña usando comparación de tiempo constante
        expected = self.access_key.encode('utf-8')
        provided = password.encode('utf-8')
        
        if secrets.compare_digest(expected, provided):
            # Autenticación exitosa
            self.session_state['authenticated'] = True
            self.session_state['login_time'] = datetime.now()
            self.session_state['attempts'] = 0  # Reset attempts
            return True, "✅ Acceso concedido"
        else:
            # Autenticación fallida
            self._record_failed_attempt()
            attempts = self.session_state.get('attempts', 0)
            remaining = self.max_attempts - attempts
            
            if remaining <= 0:
                return False, "🔒 Cuenta bloqueada por exceder el número de intentos permitidos."
            else:
                return False, f"❌ Clave incorrecta. Intentos restantes: {remaining}"
    
    def _record_failed_attempt(self):
        """Registrar intento fallido"""
        attempts = self.session_state.get('attempts', 0)
        self.session_state['attempts'] = attempts + 1
        self.session_state['last_attempt'] = datetime.now()
    
    def is_authenticated(self) -> bool:
        """Verificar si el usuario está autenticado y la sesión es válida"""
        if not self.session_state.get('authenticated', False):
            return False
        
        # Verificar timeout de sesión
        login_time = self.session_state.get('login_time')
        if login_time:
            if (datetime.now() - login_time).total_seconds() > self.session_timeout:
                self.logout()
                return False
        
        return True
    
    def logout(self):
        """Cerrar sesión"""
        # Limpiar estado de sesión
        keys_to_clear = ['authenticated', 'login_time']
        for key in keys_to_clear:
            if key in self.session_state:
                del self.session_state[key]
    
    def get_remaining_attempts(self) -> int:
        """Obtener intentos restantes"""
        attempts = self.session_state.get('attempts', 0)
        return max(0, self.max_attempts - attempts)
    
    def get_session_info(self) -> dict:
        """Obtener información de la sesión"""
        return {
            'authenticated': self.is_authenticated(),
            'login_time': self.session_state.get('login_time'),
            'attempts': self.session_state.get('attempts', 0),
            'remaining_attempts': self.get_remaining_attempts()
        }


# Instancia global del gestor de autenticación
auth_manager = AuthManager()