import { createRouter, createWebHistory } from 'vue-router'
import Inicio from '@/views/Inicio.vue'
import Categorias from '../views/Categorias.vue'
import Servicios from '../views/Servicios.vue'
import Chat from '../views/Chat.vue'
import InicioSesion from '../views/InicioSesion.vue'
import Registro from '../views/Registro.vue'
import Detalle from '../views/Detalle.vue'
import Perfil from '../views/Perfil.vue'
import Solicitudes from '../views/Solicitudes.vue'
import DetallePrevista from '../views/DetallePrevista.vue'
import AgendarPrevista from '../views/AgendarPrevista.vue'
import CatalogoCategoria from '../views/CatalogoCategoria.vue'
import Cliente from '../views/Cliente.vue'
import Revision from '../views/Revision.vue'
import Publicar from '../views/Publicar.vue'
import paquetesPerfil from '../components/paquetesPerfil.vue';
import resenasPerfil from '../components/resenasPerfil.vue';
import solicitudesPerfil from '../components/solicitudesPerfil.vue';

const routes =
    [
        { path: '/', name: 'Inicio', component: Inicio },
        { path: '/categorias', name: 'Categorias', component: Categorias },
        { path: '/servicios', name: 'Servicios', component: Servicios },
        { path: '/chat', name: 'Chat', component: Chat },
        { path: '/inicio-sesion', name: 'InicioSesion', component: InicioSesion },
        { path: '/registro', name: 'Registro', component: Registro },
        { path: '/detalle/:id', name: 'Detalle', component: Detalle },
        { path: '/perfil/:usuario', name: 'Perfil', component: Perfil ,
            children: [
                { path: 'paquetes', name: 'paquetesPerfil', component: paquetesPerfil },
                { path: 'resenas', name: 'resenasPerfil', component: resenasPerfil },
                { path: 'solicitudes', name: 'solicitudesPerfil', component: solicitudesPerfil }
            ]
        },
        { path: '/solicitudes', name: 'Solicitudes', component: Solicitudes },
        { path: '/detalle-prevista/:id', name: 'DetallePrevista', component: DetallePrevista },
        { path: '/agendar-prevista/:id', name: 'AgendarPrevista', component: AgendarPrevista }, 
        { path: '/catalogo-categoria/:nombre', name: 'CatalogoCategoria', component: CatalogoCategoria },
        { path: '/cliente', name: 'Cliente', component: Cliente },
        { path: '/revision', name: 'Revision', component: Revision },
        { path: '/publicar', name: 'Publicar', component: Publicar },
    ]

export default createRouter({
    history: createWebHistory(),
    routes
})
