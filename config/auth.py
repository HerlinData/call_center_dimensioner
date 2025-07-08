"""
Manejo de autenticación segura
"""

import streamlit as st
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
    """Gestor de autenticación segura"""
    
    def __init__(self):
        # Cargar configuración desde variables de entorno
        self.access_key = os.getenv('ACCESS_KEY')
        if not self.access_key:
            raise ValueError("ACCESS_KEY es requerido en variables de entorno")
        
        self.session_key = "authenticated"
        self.login_time_key = "login_time"
        self.attempt_key = "login_attempts"
        self.last_attempt_key = "last_attempt"
        self.timeout_hours = int(os.getenv('SESSION_TIMEOUT_HOURS', '8'))
        self.max_attempts = 3
        self.lockout_minutes = 15
        
        # Generar salt para hash
        self.salt = os.getenv('JWT_SECRET_KEY', secrets.token_hex(32)).encode('utf-8')
    
    def _hash_password(self, password: str) -> str:
        """Crear hash seguro de la contraseña"""
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), self.salt, 100000).hex()
    
    def _check_lockout(self) -> bool:
        """Verificar si el usuario está bloqueado por intentos fallidos"""
        attempts = st.session_state.get(self.attempt_key, 0)
        last_attempt = st.session_state.get(self.last_attempt_key)
        
        if attempts >= self.max_attempts and last_attempt:
            if datetime.now() - last_attempt < timedelta(minutes=self.lockout_minutes):
                return True
            else:
                # Reset counter after lockout period
                st.session_state[self.attempt_key] = 0
                return False
        return False
    
    def authenticate(self, input_key: str) -> bool:
        """Verificar clave de acceso con medidas de seguridad"""
        
        # Verificar si está bloqueado
        if self._check_lockout():
            return False
        
        # Validar entrada
        if not input_key or len(input_key.strip()) == 0:
            self._record_failed_attempt()
            return False
        
        # Comparación segura (tiempo constante)
        input_hash = self._hash_password(input_key)
        expected_hash = self._hash_password(self.access_key)
        
        if secrets.compare_digest(input_hash, expected_hash):
            st.session_state[self.session_key] = True
            st.session_state[self.login_time_key] = datetime.now()
            st.session_state[self.attempt_key] = 0  # Reset attempts
            return True
        else:
            self._record_failed_attempt()
            return False
    
    def _record_failed_attempt(self):
        """Registrar intento fallido"""
        attempts = st.session_state.get(self.attempt_key, 0)
        st.session_state[self.attempt_key] = attempts + 1
        st.session_state[self.last_attempt_key] = datetime.now()
    
    def is_authenticated(self) -> bool:
        """Verificar si el usuario está autenticado"""
        if not st.session_state.get(self.session_key, False):
            return False
        
        # Verificar timeout
        login_time = st.session_state.get(self.login_time_key)
        if login_time and datetime.now() - login_time > timedelta(hours=self.timeout_hours):
            self.logout()
            return False
        
        return True
    
    def logout(self):
        """Cerrar sesión y limpiar datos sensibles"""
        keys_to_clear = [
            self.session_key,
            self.login_time_key,
            self.attempt_key,
            self.last_attempt_key
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_login_form(self) -> Optional[bool]:
        """Mostrar formulario de login con medidas de seguridad"""
        
        # Verificar si está bloqueado
        if self._check_lockout():
            attempts = st.session_state.get(self.attempt_key, 0)
            last_attempt = st.session_state.get(self.last_attempt_key)
            remaining_time = self.lockout_minutes - (datetime.now() - last_attempt).total_seconds() / 60
            
            st.error(f"🔒 Cuenta bloqueada por {attempts} intentos fallidos. "
                    f"Inténtalo nuevamente en {remaining_time:.1f} minutos.")
            return False
        
        st.markdown("""
        <div style="max-width: 400px; margin: 5rem auto; padding: 3rem; 
                    background: rgba(255, 255, 255, 0.9); border-radius: 15px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); text-align: center;">
            <h2 style="color: #2c3e50; margin-bottom: 2rem;">🔐 Acceso al Sistema</h2>
            <p style="color: #7f8c8d; margin-bottom: 2rem;">Ingresa la clave de acceso</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar intentos restantes si hay intentos fallidos
        attempts = st.session_state.get(self.attempt_key, 0)
        if attempts > 0:
            remaining = self.max_attempts - attempts
            st.warning(f"⚠️ Intentos restantes: {remaining}")
        
        with st.form("login_form"):
            password = st.text_input("Clave de acceso", type="password", 
                                   placeholder="Ingresa tu clave",
                                   help="La cuenta se bloquea después de 3 intentos fallidos")
            submitted = st.form_submit_button("🔓 Ingresar", use_container_width=True)
            
            if submitted:
                if self.authenticate(password):
                    st.success("✅ Acceso concedido")
                    st.rerun()
                else:
                    attempts = st.session_state.get(self.attempt_key, 0)
                    if attempts >= self.max_attempts:
                        st.error("🔒 Cuenta bloqueada por exceder el número de intentos permitidos.")
                    else:
                        remaining = self.max_attempts - attempts
                        st.error(f"❌ Clave incorrecta. Intentos restantes: {remaining}")
                    return False
        
        return None

# Instancia global
auth_manager = AuthManager()