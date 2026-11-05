# Patate Merge 🥔

Simulation brainrot infinie : des patates tombent, fusionnent, parlent et montent les 14 échelons
jusqu'à la Patate suprême. Le tout dans une fausse interface TikTok verticale.

**Jouer :** https://vtndenis.github.io/patate-merge/

## Ce que ça fait

- Boucle automatique : l'IA lâche les patates toute seule, il n'y a rien à faire.
- 14 paliers, de « la Patate brute » à « la Patate suprême » (portugaise, bretonne, chef, italienne,
  cosmonaute, influenceuse, banquière, présidente, nucléaire, cosmique…).
- Voix par personnage pré-générées (edge-tts : Henri, Denise, Duarte en pt-PT, Diego en it-IT…),
  avec un effet ralenti progressif : plus la patate monte, plus la voix traîne et s'assombrit
  (`playbackRate` 1.12 → 0.70 + filtre passe-bas + écho sur les hauts paliers).
- Musique et effets sonores générés en WebAudio (aucun fichier audio externe).
- Physique de fusion type Suika, décor de bocal, comptoir, frise de progression, sous-titres.
- Épisodes : quand la Patate suprême apparaît (ou quand ça déborde), l'écran coupe et ça repart.

## Détails

- Un seul fichier `index.html`, aucune dépendance, fonctionne hors ligne.
- Les patates sont dessinées en SVG (silhouette générée par graine, visage, accessoires).
- Le son démarre au clic sur « Lancer » (politique d'autoplay des navigateurs).
- `window.BRAINROT` expose l'état et des aides de test (`stats`, `forceTier`, `speak`, `Voice`).
- `python gen_voices.py` régénère les 47 répliques dans `audio/` à partir des lignes de `index.html`
  (source unique), puis `git push` met le site à jour.
