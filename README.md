Motion Frames
Uma skill que ensina o seu agente de IA a criar vídeos de motion design profissionais.
Vídeos verticais (1080x1920, 60fps) para TikTok, Reels e anúncios — com tipografia cinética, animações 3D, transições suaves e efeitos sonoros, tudo gerado por código.
Como funciona (versão simples)
A animação é uma página HTML. Para cada quadro do vídeo, uma função chamada renderFrame(n) calcula o que aparece na tela.
Um navegador sem tela fotografa a página quadro a quadro.
O ffmpeg junta as fotos e vira o MP4 final, com o som.
Como cada quadro é calculado por fórmula (nada de relógio, nada de sorteio), o resultado é sempre o mesmo — e dá pra sincronizar a animação com uma narração, palavra por palavra.
O que vem no pacote
motion-frames/
├── SKILL.md          → as regras e os estilos de vídeo (o "cérebro" da skill)
├── README.md         → este arquivo
└── pipeline/
    ├── template.html → página inicial com as funções de animação prontas
    ├── render.mjs    → fotografa os quadros
    ├── preview.mjs   → mostra alguns quadros antes de renderizar tudo
    └── sfx_kit.py    → cria os efeitos sonoros
Como instalar
Jeito 1 — como skill: copie a pasta motion-frames para ~/workspace/custom-skills/ do seu agente. Pronto, ele já sabe usar.
Jeito 2 — pelo chat: envie o zip da skill na conversa e peça: "usa essa skill para criar um vídeo sobre…". O agente lê, descompacta e faz o vídeo.
O que precisa ter no computador
Node.js 18+ e ffmpeg — para renderizar e montar o vídeo.
Um Chromium headless — para fotografar os quadros. Se não tiver: npx @puppeteer/browsers install chrome-headless-shell
Python 3 com numpy e scipy — para os efeitos sonoros: pip install numpy scipy
(Opcional) faster-whisper — só se o vídeo tiver narração para sincronizar: pip install faster-whisper
Como criar um vídeo
# 1. Comece do template e monte a sua cena
cp pipeline/template.html meu-video.html

# 2. Espie alguns quadros antes (evita surpresa depois)
node pipeline/preview.mjs meu-video.html prev "0,60,160,300,470" 480 1080 1920

# 3. Renderize todos os quadros
FMT=jpeg PORT=9333 node pipeline/render.mjs meu-video.html frames 480 1080 1920

# 4. Monte o vídeo final
ffmpeg -framerate 60 -i frames/f%04d.jpg -i sfx.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -movflags +faststart meu-video.mp4
Na prática, você não precisa rodar nada disso na mão: peça ao agente ("faz um vídeo de 15s sobre meu app") e ele usa a skill sozinho.
Os 4 estilos de vídeo
O SKILL.md explica cada um em detalhes:
Cinema/morph — abertura de cinema, objetos que se transformam um no outro, elemento 3D girando.
App premium — celular 3D flutuando, números contando, botão gigante de ação, logo no final.
Cena interativa — sem cortes: um cursor clica, um texto é digitado e a tela responde, como num produto de verdade.
Tipografia clara — fundo claro, palavras grandes seguindo a narração, notificações empilhando, ideal para anúncios falados.
Três regras valem para todos: o fundo nunca é uma cor chapada (ele se mexe e tem profundidade), acontece alguma coisa a cada 0,5–1,5s e cada animação tem seu sonzinho.
Vídeos feitos com esta skill
TurtlePags (53s) — anúncio de gateway de pagamentos, com a narração sincronizada palavra por palavra e a identidade visual real da marca.
Feito com Muse (14s) — cena interativa: cursor clica, prompt é digitado e o fundo muda de cor por comando.
Kalo (15s) — propaganda de app de calorias, com celular 3D e escaneamento de refeição por IA.
iPhone 18 Pro (53s) — narração sincronizada com um celular 3D feito só com CSS.
Licença
A definir pelo autor. Para circulação aberta, MIT é uma boa escolha.
