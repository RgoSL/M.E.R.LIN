// Lógica de Funcionalidades em um Arquivo Único

// Inicializando as Animações de Scroll
AOS.init(); // Import do AOS
AOS.init({
  disable: false, 
  startEvent: 'DOMContentLoaded', 
  initClassName: 'aos-init', 
  animatedClassName: 'aos-animate', 
  useClassNames: false,
  disableMutationObserver: false, 
  debounceDelay: 50, 
  throttleDelay: 99, 
  
  offset: 120,
  delay: 0, 
  duration: 400, 
  easing: 'ease', 
  once: false, 
  mirror: false, 
  anchorPlacement: 'top-bottom', 
});
// Fim da Inicialização do AOS

// Ativação de Links nos Cards

// Fim da Ativação de Links