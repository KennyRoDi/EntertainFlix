<template>
  <div class="page font-sans min-h-screen flex flex-col">
    <Navbar />

    <main class="flex-grow flex justify-center items-center px-4 py-16">
      <div class="w-full max-w-md">
        <form
          @submit.prevent="iniciarSesion"
          class="form-card shadow rounded p-6 space-y-4"
        >
          <h2 class="text-2xl font-bold text-center mb-4">Iniciar Sesión</h2>

          <!-- Google Login Button -->
          <div class="space-y-3">
            <button
              @click="handleSocialLogin('google')"
              type="button"
              class="w-full btn-social-google py-2 rounded flex items-center justify-center space-x-2"
              :disabled="loading"
            >
              <svg viewBox="0 0 48 48" class="w-5 h-5" width="24" height="24">
                <path fill="#FFC107"
                  d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,19.044-8.136,19.044-19.5C43.044,22.684,43.434,21.319,43.611,20.083z" />
                <path fill="#FF3D00"
                  d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.665,8.318,6.306,14.691z" />
                <path fill="#4CAF50"
                  d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z" />
                <path fill="#1976D2"
                  d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.08,5.592c3.551-2.329,5.999-6.388,5.999-11.234C39.324,22.382,43.044,21.319,43.611,20.083z" />
              </svg>
              <span>{{ loading ? 'Procesando...' : 'Continuar con Google' }}</span>
            </button>
          </div>

          <p v-if="apiMessage" class="mt-2 text-xs text-center p-2 bg-blue-50 text-blue-800 rounded">
            {{ apiMessage }}
          </p>

          <div class="flex items-center">
            <div class="flex-grow border-t border-gray-300"></div>
            <span class="flex-shrink mx-4 text-gray-500 text-sm">o continuar con</span>
            <div class="flex-grow border-t border-gray-300"></div>
          </div>

          <div>
            <label class="block text-sm font-semibold mb-1">Correo o Usuario</label>
            <input
              v-model="inputUsuario"
              type="text"
              placeholder="usuario@correo.com"
              class="w-full input-field px-4 py-2 rounded"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold mb-1">Contraseña</label>
            <div class="relative">
              <input
                v-model="inputPassword"
                :type="passwordFieldType"
                placeholder=""
                class="w-full input-field px-4 py-2 rounded pr-10"
              />
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-2 top-1/2 transform -translate-y-1/2 p-1 text-gray-500 hover:text-gray-700 focus:outline-none"
                aria-label="Toggle password visibility">
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                  viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.875 5.875C12.44 14.73 10 12.5 10 12c0-.5.21-1.01.625-1.375M21 12c-1.275 4.057-5.065 7-9.543 7a9.97 9.97 0 01-1.563-.029m5.875 5.875A3 3 0 1012 15a3 3 0 001.875-5.375z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <p v-if="error" class="error-text text-sm text-center">{{ error }}</p>

          <button
            type="submit"
            class="w-full btn-primary py-2 rounded"
            :disabled="loading"
          >
            {{ loading ? "Verificando..." : "Iniciar Sesión" }}
          </button>

          <div class="text-sm text-center meta-text pt-2">
            ¿No tienes cuenta?
            <router-link to="/registro" class="link">Regístrate</router-link>
          </div>
        </form>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import Navbar from "@/components/Navbar.vue";
import Footer from "@/components/Footer.vue";
import { useAuth } from "@/composables/useAuth.js";
import { useUsers } from "@/composables/useUser.js";

/* Constantes de OAuth / rutas */
const GOOGLE_CLIENT_ID = "623164831395-ooojq523bftisjcj28ift0cvts7keq0e.apps.googleusercontent.com";
const REDIRECT_PATH = "/inicio-sesion";

/* Router y estado del formulario */
const router = useRouter();
const inputUsuario = ref("");
const inputPassword = ref("");
const error = ref("");
const apiMessage = ref("");
const loading = ref(false);

/* Composables: auth y usuarios */
const { login } = useAuth();
const { users, loadAll, registerUser } = useUsers();

/* UI: toggle para mostrar/ocultar contraseña */
const showPassword = ref(false);
const passwordFieldType = computed(() =>
  showPassword.value ? "text" : "password"
);

/* Ejecutar al montar: manejar posible redirect de Google */
onMounted(() => {
  handleGoogleRedirect();
});

/* -------------------------------
   Utilidades
   ------------------------------- */

/* Decodifica un JWT (id_token) y devuelve el payload como objeto */
function decodeJWT(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    console.error('Error decoding JWT:', e);
    return null;
  }
}

/* Genera un nombre de usuario aleatorio a partir del email (para cuentas creadas vía Google) */
function generateUsername(email) {
  const baseName = email.split('@')[0];
  const randomNum = Math.floor(Math.random() * 9999);
  return `${baseName}${randomNum}`;
}

/* -------------------------------
   Google OAuth (social login)
   ------------------------------- */

/* Inicia el flujo OAuth redirigiendo a Google */
function handleSocialLogin(provider) {
  if (provider === 'google') {
    const redirectUri = window.location.origin + REDIRECT_PATH;
    const authUrl = 'https://accounts.google.com/o/oauth2/v2/auth';
    const nonce = crypto.randomUUID();
    
    const params = new URLSearchParams({
      client_id: GOOGLE_CLIENT_ID,
      redirect_uri: redirectUri,
      response_type: 'id_token',
      scope: 'openid email profile',
      nonce: nonce,
    });
    
    window.location.href = `${authUrl}?${params.toString()}`;
  }
}

/*
  Maneja el redirect desde Google: si llega un id_token en el hash,
  decodifica el token, verifica si el usuario existe y lo loguea;
  si no existe, lo registra (registerUser) y luego lo loguea.
*/
async function handleGoogleRedirect() {
  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);
  const idToken = params.get('id_token');

  if (idToken) {
    loading.value = true;
    apiMessage.value = "Procesando tu inicio de sesión con Google...";
    
    try {
      const userInfo = decodeJWT(idToken);
      if (!userInfo || !userInfo.email) {
        throw new Error('No se pudo obtener la información del usuario');
      }
      localStorage.setItem('google_id_token', idToken);
      await loadAll();
      let existingUser = users.value.find(u => u.correo === userInfo.email);
      
      if (existingUser) {
        apiMessage.value = "¡Bienvenido de nuevo!";
        login({
          id: existingUser.id,
          nombre: existingUser.nombre,
          usuario: existingUser.usuario,
          rol: existingUser.rol,
          correo: existingUser.correo
        });
        
        router.replace({ path: '/' });
      } else {
        apiMessage.value = "Creando tu cuenta...";
        
        const newUser = {
          nombre: userInfo.name || userInfo.email.split('@')[0],
          correo: userInfo.email,
          usuario: generateUsername(userInfo.email),
          contraseña: crypto.randomUUID(), 
          rol: 'contratista', 
          googleId: userInfo.sub, 
        };
        
        await registerUser(newUser);
        
        await loadAll();
        const createdUser = users.value.find(u => u.correo === userInfo.email);
        
        if (createdUser) {
          apiMessage.value = "¡Cuenta creada! Bienvenido.";
          login({
            id: createdUser.id,
            nombre: createdUser.nombre,
            usuario: createdUser.usuario,
            rol: createdUser.rol,
            correo: createdUser.correo
          });
          
          router.replace({ path: '/' });
        }
      }
    } catch (err) {
      console.error('Error en autenticación de Google:', err);
      error.value = "Error al iniciar sesión con Google. Por favor, intenta de nuevo.";
      apiMessage.value = "";
      // Clean up the URL
      router.replace({ path: REDIRECT_PATH });
    } finally {
      loading.value = false;
    }
  }
}

/* -------------------------------
   Login estándar (usuario + contraseña)
   ------------------------------- */

/* Intenta iniciar sesión comparando usuario/email + contraseña contra el listado de users */
async function iniciarSesion() {
  error.value = "";
  loading.value = true;
  
  try {
    await loadAll();

    const usuarioEncontrado = users.value.find(
      (u) =>
        (u.usuario === inputUsuario.value || u.correo === inputUsuario.value) &&
        u.contraseña === inputPassword.value
    );

    if (usuarioEncontrado) {
      login({
        id: usuarioEncontrado.id,
        nombre: usuarioEncontrado.nombre,
        usuario: usuarioEncontrado.usuario,
        rol: usuarioEncontrado.rol,
        correo: usuarioEncontrado.correo
      });
      router.push("/");
    } else {
      error.value = "Credenciales inválidas. Verifica tu usuario y contraseña.";
    }
  } catch (err) {
    console.error('Error en inicio de sesión:', err);
    error.value = "Error al iniciar sesión. Por favor, intenta de nuevo.";
  } finally {
    loading.value = false;
  }
}
</script>


<style scoped>
.page {
  background-color: var(--color-body-bg);
  color: var(--color-text);
  min-height: 100vh;
  transition: background-color 180ms ease, color 180ms ease;
}

.form-card {
  background-color: var(--color-background-light);
  color: var(--color-text);
  border-radius: 0.5rem;
  transition: background-color 180ms ease, color 180ms ease;
}

.input-field {
  width: 100%;
  background-color: var(--color-body-bg);
  color: var(--color-text);
  border: 1px solid var(--color-background-light);
  transition: background-color 180ms ease, color 180ms ease,
    border-color 180ms ease;
  outline: none;
}

.input-field:focus {
  box-shadow: 0 0 0 3px var(--color-primary-button-bg);
}

.error-text {
  color: #dc2626;
}

.btn-primary {
  background-color: var(--color-primary-button-bg);
  color: var(--color-primary-button-text);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: filter 120ms ease, opacity 120ms ease;
  cursor: pointer;
}

.btn-primary:hover:not(:disabled) {
  filter: brightness(0.9);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.meta-text {
  color: var(--color-text-light);
}

.link {
  color: var(--color-primary-button-bg);
  font-weight: 600;
  margin-left: 0.25rem;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

.btn-social-google {
  background-color: white;
  color: #444;
  border: 1px solid var(--color-border);
  font-weight: 500;
  transition: background-color 120ms ease;
}

.btn-social-google:hover:not(:disabled) {
  background-color: #f0f0f0;
}

.btn-social-google:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>