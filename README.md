# Patate Merge 🥔

Simulation brainrot infinie : des patates tombent, fusionnent, parlent et montent les 14 échelons
jusqu'à la Patate suprême. Le tout dans une fausse interface TikTok verticale.

**Jouer :** https://vtndenis.github.io/patate-merge/

## Ce que ça fait

- Boucle automatique : l'IA lâche les patates toute seule, il n'y a rien à faire.
- 14 paliers, de « la Patate brute » à « la Super Patate » (portugaise, bretonne, chef, italienne,
  cosmonaute, influenceuse, ninja, musicale, volante, Cosmopatate, Super Patate).
- Voix par personnage : 27 répliques générées (edge-tts) + **5 répliques découpées dans le reel
  de la trend** (`instagram.com/reel/DfQKWy8gR14`, @louis.rsnt) pour ninja, musicale, volante,
  Cosmopatate et Super Patate.
- Effet ralenti progressif : plus la patate monte, plus la voix traîne et s'assombrit
  (`playbackRate` 1.12 → 0.70 + filtre passe-bas + écho sur les hauts paliers).
- Musique : boucle synthétisée (`gen_music.py` → `audio/music_loop.mp3`), lue en `<audio loop>`.
  Voix et musique passent par HTMLAudioElement (compatible iOS), les effets par WebAudio quand il est dispo.
- Physique de fusion type Suika dans un **bocal circulaire** (les patates roulent le long de la paroi),
  comptoir, frise de progression, sous-titres.
- Épisodes : quand la Patate suprême apparaît (ou quand ça déborde), l'écran coupe et ça repart.

## Détails

- Un seul fichier `index.html`, aucune dépendance, fonctionne hors ligne.
- Les patates sont dessinées en SVG (silhouette générée par graine, visage, accessoires).
- Le son démarre au clic sur « Lancer » (politique d'autoplay des navigateurs).
- `window.BRAINROT` expose l'état et des aides de test (`stats`, `forceTier`, `speak`, `Voice`).
- `python gen_voices.py` régénère les répliques TTS dans `audio/` à partir des lignes de `index.html`
  (source unique ; les paliers 9-13 utilisent les clips réels), puis `git push` met le site à jour.
- Les 5 clips `audio/real_*.mp3` viennent d'un reel d'octobre/novembre 2026 : usage hommage / personnel,
  ils restent la propriété de leur auteur.
