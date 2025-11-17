import { ref } from 'vue'

const usuario = ref(null)
const authToken = ref(null)

function login(userData) {
  usuario.value = userData
  // Store only non-sensitive user info in localStorage
  localStorage.setItem('usuario', JSON.stringify({
    id: userData.id,
    nombre: userData.nombre,
    usuario: userData.usuario,
    rol: userData.rol,
    correo: userData.correo
  }))
}

function setToken(token) {
  authToken.value = token
  // Store token in sessionStorage (cleared on browser close)
  sessionStorage.setItem('authToken', token)
}

function getToken() {
  return authToken.value || sessionStorage.getItem('authToken')
}

function logout() {
  usuario.value = null
  authToken.value = null
  localStorage.removeItem('usuario')
  sessionStorage.removeItem('authToken')
  // Clear all sensitive data
  sessionStorage.clear()
}

function isAuthenticated() {
  return !!usuario.value && !!getToken()
}

export function useAuth() {
  return {
    usuario,
    login,
    setToken,
    getToken,
    logout,
    isAuthenticated
  }
}