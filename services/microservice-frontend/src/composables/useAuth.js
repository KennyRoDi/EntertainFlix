import { ref } from 'vue'
const usuario = ref(JSON.parse(localStorage.getItem('usuario')) || null)

function login(userData) {
  usuario.value = userData
  localStorage.setItem('usuario', JSON.stringify(userData))
}

function logout() {
  usuario.value = null
  localStorage.removeItem('usuario')
}

export function useAuth() {
  return {
    usuario,
    login,
    logout
}

}