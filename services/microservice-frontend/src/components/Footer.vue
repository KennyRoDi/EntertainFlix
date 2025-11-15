<template>
  <footer class="footer">
    <div class="max-w-6xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-6">
      <div>
        <h3 class="footer-heading-main">ENTERTAINFLIX</h3>
        <div class="flex space-x-4">
          <i class="fab fa-facebook"></i>
          <i class="fab fa-linkedin"></i>
          <i class="fab fa-youtube"></i>
          <i class="fab fa-instagram"></i>
        </div>
        <div>
          <h4 class="footer-heading-sub">Redes Sociales</h4>
          <div class="flex space-x-4">
            <a href="https://www.facebook.com/yourpage" target="_blank" aria-label="Facebook">
              <img src="https://img.icons8.com/fluent/48/000000/facebook-new.png" alt="Facebook" class="h-8 w-8" />
            </a>
            <a href="https://twitter.com/yourpage" target="_blank" aria-label="Twitter">
              <img src="https://img.icons8.com/fluent/48/000000/twitter.png" alt="Twitter" class="h-8 w-8" />
            </a>
            <a href="https://www.linkedin.com/in/yourpage" target="_blank" aria-label="LinkedIn">
              <img src="https://img.icons8.com/fluent/48/000000/linkedin.png" alt="LinkedIn" class="h-8 w-8" />
            </a>
          </div>
        </div>

      </div>
      <div>
        <h4 class="footer-heading-sub">Empresa</h4>
        <ul class="footer-list">
          <li>Equipo</li>
          <li>Visión</li>
          <li>Únete</li>
        </ul>
      </div>
      <div>
        <h4 class="footer-heading-sub">Soporte</h4>
        <ul class="footer-list">
          <li>FAQ</li>
          <li>Términos y Condiciones</li>
          <li>Política de Privacidad</li>
        </ul>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped>
.footer {
  background-color: var(--color-footer-bg);
  color: var(--color-footer-text);
  font-size: 0.875rem;
  padding: 2.5rem 1rem;
}

.footer-heading-main {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-footer-heading);
  margin-bottom: 1rem;
}

.footer-heading-sub {
  font-weight: 600;
  color: var(--color-footer-heading);
  margin-bottom: 0.5rem;
}

.footer-list {
  list-style: none;
  padding: 0;
  line-height: 1.5;
}
</style>