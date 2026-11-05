Motion Frames — motion design por quadros
Skill de motion design profissional: vídeos verticais 1080x1920 a 60fps gerados quadro a quadro a partir de uma única página HTML — animação como função pura do número do quadro, com tipografia cinética, morphs, elementos 3D, fundos vivos e efeitos sonoros sincronizados.
Professional motion design skill: vertical 1080x1920 @ 60fps videos rendered frame-by-frame from a single HTML file — animation as a pure function of the frame number.
Como funciona
A animação é uma página HTML cuja cena inteira vive em renderFrame(n): dado o número do quadro, ela calcula exatamente o que está na tela. Sem relógio (Date.now, requestAnimationFrame), sem aleatório sem semente — tudo é fórmula fechada (springs analíticos, easings, interpolação), então o resultado é determinístico: mesmo input, mesmos pixels.
Um Chromium headless fotografa a página quadro a quadro (via CDP, sem dependências de npm), com suporte a renderização em paralelo (shards) para vídeos longos.
O ffmpeg monta o MP4 e mistura a trilha de efeitos sonoros sintetizados — cada som amarrado ao mesmo número de quadro do evento visual.
Como cada quadro é independente, dá para sincronizar a animação palavra por palavra com uma narração (transcrição com timestamps), retomar renders de qualquer ponto e gerar variações mudando só os parâmetros da cena.
Estrutura
motion-frames/
├── SKILL.md            # o sistema completo: regras, gramáticas, checklist, erros conhecidos
├── README.md           # este arquivo
└── pipeline/
    ├── template.html   # página-base com helpers (spring, seg, easings, hash) e o esqueleto renderFrame(n)
    ├── render.mjs      # renderizador quadro a quadro (CDP, sem dependências)
    ├── preview.mjs     # renderiza só quadros escolhidos, para conferência rápida
    └── sfx_kit.py      # kit de SFX sintetizados (pop, tick, whoosh, shimmer, pad) por número de quadro
Instalação
Como skill (recomendado): copie a pasta motion-frames para ~/workspace/custom-skills/ do seu ambiente de agente. A skill passa a ser descoberta automaticamente nas próximas conversas.
Uso avulso: envie o zip da skill no chat do seu agente e peça para usá-la ("usa essa skill para criar um vídeo sobre…"). O agente lê o SKILL.md, descompacta o pipeline e produz.
Requisitos
Node.js 18+ — para o renderizador (usa apenas módulos nativos).
ffmpeg — para montar o MP4 final.
Chromium headless — um chrome-headless-shell acessível. O renderizador procura, nesta ordem: a variável CHROME_BIN, um chrome-headless-shell ao lado do script, e caminhos conhecidos. Para baixar um:
  npx @puppeteer/browsers install chrome-headless-shell
  (nem todo Chromium serve: builds com política de domínio/WebGL podem recusar execução standalone — o headless shell avulso funciona.)
Python 3 + numpy + scipy — para o kit de SFX (pip install numpy scipy).
Opcional: faster-whisper (pip install faster-whisper) para sincronizar vídeos com narração, palavra por palavra.
Uso rápido
# 1. Comece do template e escreva sua cena em renderFrame(n)
cp pipeline/template.html meu-video.html

# 2. Confira quadros-chave antes de renderizar tudo (contact sheet + tamanho real!)
node pipeline/preview.mjs meu-video.html prev "0,60,160,300,470" 480 1080 1920

# 3. Renderize (FMT=jpeg é ~2x mais rápido que PNG)
FMT=jpeg PORT=9333 node pipeline/render.mjs meu-video.html frames 480 1080 1920

# 4. Monte o MP4
ffmpeg -framerate 60 -i frames/f%04d.jpg -i sfx.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k \
  -movflags +faststart meu-video.mp4
Vídeos longos: divida em 2 shards com o argumento de quadro inicial do render.mjs (ex.: quadros 0–1592 e 1593–3185, cada um com sua PORT). Máximo 2 shards em paralelo em máquinas com ~8GB de RAM.
As quatro gramáticas
O SKILL.md detalha cada uma, plano a plano:
Cinema/morph — abertura cinematográfica, objeto com squash & stretch, morphs de forma, elemento 3D, tipografia cinética.
App promo premium — telefone 3D com pull focus, números contando em pílulas de vidro, agregação em número gigante, CTA e logo reveal.
Cena contínua interativa — uma cena só sobre fundo fluido: cursor clica, prompt é digitado, a interface faz morph para o resultado, um comando muda a cor do mundo.
Kinetic type claro — fundo claro da marca, tipografia pesada como protagonista sincronizada com a fala, notificações empilhando com física, sistemas orbitais, UI real contando a história.
E três regras que atravessam todas: fundo nunca chapado (sempre vivo, com fluxo e parallax), um micro-evento a cada 0,5–1,5s e SFX em cada micro-evento.
Produzido com este sistema
TurtlePags (53s) — anúncio de gateway de pagamentos com narração sincronizada palavra por palavra, identidade real da marca (logo, paleta e fontes extraídas do site), gramática kinetic type claro.
Feito com Muse (14s) — cena contínua interativa: cursor, prompt digitado, morphs e fundo que muda de cor por comando.
Kalo (15s) — promo de app de calorias: gramática app premium, fundo estúdio vivo e cena de escaneamento de refeição por IA.
iPhone 18 Pro (53s) — narração sincronizada com aparelho 3D construído em CSS puro.
Teste de loop (8s) — gramática cinema/morph em loop perfeito.
Licença
A definir pelo autor. Se a ideia é circulação aberta, MIT é uma boa opção para skills.
