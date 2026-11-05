# Fleur mon Jardin Hassen: digital business card

A one-page digital card built from the *Charte graphique Fleur mon Jardin, édition 2026*.

## Contents

```
index.html                     The page (HTML + CSS + a few lines of JS, no framework)
assets/logo_full.svg           Full logo, vector paths taken from the charter PDF
assets/symbol.svg              Arch + rose symbol
assets/petals.webp             Decorative petals (charter p. 12)
assets/rose.webp               Signature rose illustration (charter p. 13)
qr/fleur-mon-jardin-qr.svg     QR code, vector (use this one for print)
qr/fleur-mon-jardin-qr.png     QR code, 3000 × 3000 px
qr/fleur-mon-jardin-qr-carte.* Print-ready A5 card with logo, QR code and phone number (300 dpi)
tools/make_qr.py               Rebuilds the QR files for any URL
```

## Brand rules applied

| Charter rule | Used for |
|---|---|
| Vert jardin `#2B603F`, Rouge rose `#A11E36` (primary) | Logo, titles, icons, accents |
| Vert profond `#1F4A33` | Body text, QR modules |
| Crème `#FDF5E6` | Card background |
| Beige champagne `#E0C9A4` | Page background |
| Garamond Italic for titles and taglines | Headline, labels, signature (EB Garamond web font, falls back to Garamond) |
| Century Gothic for info and contact details | Eyebrows, phone number, sub-labels (falls back to Questrial, a close match) |
| The arch, "the garden gate" | Card shape, the four buttons, the QR centre |
| Petals come in from the corners, never on the logo | Top-right and bottom-left corners only |
| Rose illustration only on large formats, on a light background | Shown on screens wider than 960 px |
| The logo is never distorted or recoloured | Original vector logo, fixed aspect ratio |

## The live link

The site is hosted on Netlify at **https://fleur-mon-jardin-hassen.netlify.app**, deployed automatically from this repository's `main` branch. The QR code points to that address.

## Hosting it on your own domain (optional)

The folder is a plain static site, so any static host works.

**Netlify Drop (easiest, free):**
1. Go to https://app.netlify.com/drop.
2. Drag the whole `fleur-mon-jardin` folder onto the page.
3. You get a URL such as `https://fleur-mon-jardin.netlify.app`. You can rename it under *Site settings → Change site name*, or attach a domain like `fleurmonjardin.tn`.

**GitHub Pages:** push the folder to a repository, then go to *Settings → Pages → Deploy from branch → main / root*.

**Vercel:** run `npx vercel` inside the folder, or import the repository at vercel.com.

**After moving to a new URL, rebuild the QR code. Never print a code that points to a test address.**

```bash
pip install opencv-python        # also needs rsvg-convert (librsvg)
python3 tools/make_qr.py "https://your-final-url"
```

The script uses error-correction level H (30 %), which keeps the code readable with the logo in the centre.

## Print guidance

- Minimum printed size: 2.5 × 2.5 cm. On flags and the shop front, 8 cm or more.
- Keep the cream quiet zone around the code. Don't place it on a busy photo.
- Before a large print run, test-scan the printed proof with both an iPhone and an Android phone.

## Editing

All text is in `index.html`. All colours are CSS variables at the top of the `<style>` block.
