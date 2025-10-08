// Inicializando as Animações de Scroll
AOS.init(); 
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
  duration: 1000, 
  easing: 'ease-out', 
  once: false, 
  mirror: false, 
  anchorPlacement: 'top-bottom', 
});
// Fim da Inicialização do AOS

// Começo da Ativação de Links nos Cards
const devs = { // Array com as Redes Sociais de Cada ID, Vulgo Desenvolvedor
  "mota": {
    redes: [
    "https://www.instagram.com/jaokky/",
    "https://www.linkedin.com/in/jo%C3%A3o-mota-a59b6035b/",
    "https://github.com/joaopedrosantanamotalol"
    ],
    usadas: []
  },
  "emi": {
    redes: [
     "https://www.instagram.com/emycspri__/",
     "https://github.com/emycspri"
    ],
    usadas: []
  },
  "diggo": {
    redes: [
      "https://www.instagram.com/Rd0.ls/",
      "https://www.linkedIn.com/in/limarodrigo-",
      "https://www.github.com/RgoSL"
    ],
    usadas: []
  }
};

function abrirRedeAleatoria(devId) {
  const dev = devs[devId];
  if (!dev) return;

  const { redes, usadas } = dev;

  if (usadas.length === redes.length) {
    dev.usadas = [];
  }

  const restantes = redes.filter((url) => !dev.usadas.includes(url));

  const aleatoria = restantes[Math.floor(Math.random() * restantes.length)];

  dev.usadas.push(aleatoria);

  // Método Para Abrir as Redes em uma Nova Guia
  window.open(aleatoria, "_blank");
}

// Métodos JavaScript Para Adicionar Ações aos Cards de Desenvolvedor
document.querySelectorAll(".card").forEach(card => { // "Captura" o Elemento que Será Trabalhado, no Caso o Card de Desenvolvedor
  card.addEventListener("click", () => { // Adiciona a Função de Click ao Card
    abrirRedeAleatoria(card.id);
  });
});
// Fim da Ativação de Links

// Começo da Rede Social Aleatória
const redesPorTipo = { // Array com as Redes Sociais
  linkedin: [
    "https://www.linkedIn.com/in/limarodrigo-", 
    "https://www.linkedin.com/in/jo%C3%A3o-mota-a59b6035b/"
  ],
  instagram: [
    "https://www.instagram.com/Rd0.ls/", 
    "https://www.instagram.com/jaokky/",
    "https://www.instagram.com/emycspri__/"
  ]
};

const usadosPorTipo = { 
  linkedin: [],
  instagram: []
};

function abrirRedePorTipo(rede) {
  const lista = redesPorTipo[rede];
  const usados = usadosPorTipo[rede];

  if (!lista) return;

  if (usados.length === lista.length) {
    usadosPorTipo[rede] = [];
  }

  const restantes = lista.filter(link => !usados.includes(link));
  const aleatorio = restantes[Math.floor(Math.random() * restantes.length)];

  usados.push(aleatorio);
  window.open(aleatorio, "_blank");
}

// Mais Métodos JavaScript Para Adicionar Ações aos Links
document.querySelectorAll(".link-rede").forEach(link => { // O Elemento em Questão é a Classe no Footer com os Links
  link.addEventListener("click", (e) => { // Adiciona uma Função de Click Nova a Eles
    e.preventDefault(); // Evita que Qualquer Link Seja Aberto Antes de Passar Pela Lógica do Código

    const rede = link.getAttribute("data-rede");
    abrirRedePorTipo(rede);
  });
});
// Fim da Rede Social Aleatória

// Começo da Imagem do GitHub Clicável
document.getElementById("git").addEventListener("click", function() {
    window.open("https://github.com/RgoSL/M.E.R.LIN", "_blank");
});
// Fim da Imagem do GitHub Clicável