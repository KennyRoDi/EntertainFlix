import { useUsers } from "@/composables/useUser.js";

export async function loginUser(usuario, contraseña) {
    try {
        // Try backend first
        const response = await fetch(`http://localhost:3001/api/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ usuario, contraseña }),
            credentials: "include"
        })

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        return await response.json();
    } catch (error) {
        console.warn("Backend unavailable, using local auth");
        
        // Fallback: Use local users from composable
        const { users, loadAll } = useUsers();
        await loadAll();
        
        const foundUser = users.value.find(
            (u) =>
                (u.usuario === usuario || u.correo === usuario) &&
                u.contraseña === contraseña
        );

        if (foundUser) {
            return {
                user: {
                    id: foundUser.id,
                    nombre: foundUser.nombre,
                    usuario: foundUser.usuario,
                    rol: foundUser.rol,
                    correo: foundUser.correo
                },
                token: "local_token_" + Math.random()
            };
        }

        throw new Error("Credenciales inválidas");
    }
}

export async function googleLogin(idToken) {
    try {
        const response = await fetch(`http://localhost:3001/api/auth/google`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ idToken }),
            credentials: "include"
        })

        if (!response.ok) {
            throw new Error("Google login failed");
        }

        return await response.json();
    } catch (error) {
        console.warn("Backend unavailable, using mock Google login");
        return {
            user: {
                id: Math.random(),
                nombre: "Google User",
                usuario: "google_user_" + Math.random().toString(36).substr(2, 9),
                rol: "contratista",
                correo: "user@google.com"
            },
            token: "mock_token_google"
        };
    }
}

export function logout() {
    sessionStorage.clear();
    localStorage.removeItem('usuario');
}