# EntertainFlix

## Descripción del proyecto.

EntertainFlix es una plataforma web especializada que centraliza y simplifica la contratación de servicios de entretenimiento (músicos, artistas, shows, etc.).

El proyecto aborda la ineficiencia de depender de redes sociales, ofreciendo a los oferentes un espacio de visibilidad dedicado y a los contratistas herramientas de búsqueda, filtrado, comparación y un sistema de reseñas.

La plataforma garantiza un flujo de trabajo asistido, desde la gestión de perfiles hasta la administración de solicitudes y contratos.

## Instrucciones de despliegue local.

**Clonar el repositorio y moverse a la raiz**
```bash
git clone https://github.com/KennyRoDi/EntertainFlix.git

cd Entertainflix/services/microservice-frontend
```

**Instalar dependencias**
```bash
npm install
```

**Ejecutar en modo desarrollo**
```bash
npm run dev
```

## Capturas de pantalla del sistema en funcionamiento.

#### Página de inicio (oscuro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/be672d93-3658-409d-9696-11e033da18b5" />

#### Página de inicio (claro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/312344b8-3e5d-4f5e-bb83-47eaecaab34c" />

#### Perfil de oferente (oscuro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a296daab-9779-450b-82ac-03781c245915" />

### Perfil de oferente (claro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/8851aed8-a490-47f1-869e-88b64ad9b28a" />

#### Perfil de contratista (oscuro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a042ca41-dea7-4d76-aff5-2e66ec813bf4" />

#### Perfil de contratista (claro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/0b7a2fa2-268f-4beb-b4d8-12fe1d413031" />

#### Ventana de inicio y registro (oscuro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e7c8a686-4ba1-474a-b978-bec51f585c62" />

#### Ventana de inicio y registro (claro):

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/01e6c011-f34f-4dd2-a703-d2df7f8dccb1" />

## Estructura del repositorio:

```bash
EntertainFlix/
└── services/
    ├── microservice-frontend/
    │── .github/
    │   └── workflows/
    │── .vscode/
    │── public/
    │   └── assets/
    │       └── images/   
    │   └── vite.svg
    │
    │── src/
    │   ├── assets/
    │   │   └── json/     
    │   ├── components/   
    │   ├── composables/
    │   │   └── useAuth.js
    │   ├── router/
    │   │   └── index.js
    │   ├── views/        
    │   ├── App.vue      
    │   ├── main.js
    │   ├── style.css
    │   └── themes.css
    │
    │── .gitignore
    │── README.md
    │── index.html
    │── package.json
    │── vite.config.js
    │── tailwind.config.js
    ├── microservice-java/
    ├── microservice-js/
    └── microservice-py/
```
## Referencias bibliográficas.
Broadcom. (s.f.). Spring Boot. Spring. Recuperado de: https://spring.io/projects/spring-boot#overview 

DevDocs. (s.f.). JavaScript documentation. Recuperado de: https://devdocs.io/javascript/

draw.io. (s.f.). Getting started — Editor. Recuperado de: https://www.drawio.com/doc/getting-started-edito 

Express. (n.d.). Express - Node.js web application framework. Recuperado de: https://expressjs.com/

Figma. (s.f.). Help Center. Recuperado de: https://help.figma.com/hc/en-us/categories/360002042553

GeeksforGeeks. (2025, 23 de julio). Hexagonal architecture - system design. Recuperado de: https://www.geeksforgeeks.org/system-design/hexagonal-architecture-system-design/

GeeksforGeeks. (2025, 23 de julio). SQL cheat sheet ( basic to advanced). Recuperado de: https://www.geeksforgeeks.org/sql/sql-cheat-sheet/

GeeksforGeeks. (2025, 29 de agosto). Spring Boot tutorial. Recuperado de: https://www.geeksforgeeks.org/advance-java/spring-boot/

GeeksforGeeks. (2025, 10 de septiembre). FastAPI tutorial. Recuperado de: https://www.geeksforgeeks.org/python/fastapi-tutorial/

GeeksforGeeks. (2025, 24 de septiembre). Express.js tutorial. Recuperado de: https://www.geeksforgeeks.org/node-js/express-js/

GeeksforGeeks. (2025, 30 de octubre). Introduction to REST API. Recuperado de: https://www.geeksforgeeks.org/node-js/rest-api-introduction/

GeeksforGeeks. (2025, 7 de noviembre). Introduction to GitHub Actions. Recuperado de: https://www.geeksforgeeks.org/git/github-actions/

GitHub Docs. (s.f.). Actions. GitHub. Recuperado de: https://docs.github.com/en/actions 

GitHub Docs. (s.f.). Hello World. GitHub. Recuperado de: https://docs.github.com/en/get-started/start-your-journey/hello-world 

MongoDB, Inc. (2025). Welcome to the MongoDB docs. MongoDB. Recuperado de: https://www.mongodb.com/docs/

Mozilla. (2025, 8 de julio). JavaScript (MDN Web Docs). Recuperado de: https://developer.mozilla.org/en-US/docs/Web/JavaScript

Postman. (s.f.). Overview. Postman Learning Center. Recuperado de: https://learning.postman.com/docs/introduction/overview/ 

Ramírez, S. (s.f.). FastAPI. Recuperado de: https://fastapi.tiangolo.com/ 

Refsnes Data. (2025). MongoDB tutorial. W3Schools. Recuperado de: https://www.w3schools.com/mongodb/

Refsnes Data. (2025). PostgreSQL tutorial. W3Schools. Recuperado de: https://www.w3schools.com/postgresql/index.php

Tailwind CSS. (s.f.). Docs. Recuperado de: https://v2.tailwindcss.com/docs 

The PostgreSQL Global Development Group. (2025). PostgreSQL 18.0 documentation. PostgreSQL. Recuperado de: https://www.postgresql.org/docs/current/index.html 

Vite. (s.f.). Guide. Recuperado de: https://vite.dev/guide/ 

Vue.js. (s.f.). Introduction. Recuperado de: https://vuejs.org/guide/introduction.html 
