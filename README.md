<div align="center">

<img src="assets/banner.svg" alt="GlitchGlam" width="100%">

</div>

<img src="assets/divider.svg" alt="" width="100%">

| | Demo | Made with | What happens |
|---|---|---|---|
| 🐦 | [**magpie-season**](https://github.com/GlitchGlam/magpie-season) | JavaScript, CSS | A magpie swoops on over-claims. |
| 🚂 | [**off-the-rails**](https://github.com/GlitchGlam/off-the-rails) | Ruby | A choo choo keeps breaking down. Fix it. |
| 🚨 | **no-em-dash-club** | Go | A rainbow siren for em dashes. *Soon.* |
| 🌱 | **note-garden** | Rust | A garden grown from your notes. *Soon.* |

<img src="assets/divider.svg" alt="" width="100%">

<details>
<summary><b>🔧 How was this banner made?</b></summary>

<br>

One SVG file and a little CSS. No JavaScript, and nothing loads from another website.

- **The glitch** is three copies of the word. The cyan and pink ones sit just behind the real one,
  then slip sideways and get sliced with `clip-path: inset()` for a split second.
- **The glow** is an SVG `feGaussianBlur` under the text.
- **The scanlines** are a tiny repeating pattern, and the sweep is a gradient moving down.
- **Motion is optional.** Every animation sits inside `@media (prefers-reduced-motion: no-preference)`,
  so if your device asks for less motion the banner stays still.

</details>
