/**
 * Genera los PNGs de ícono para electron-builder desde el SVG fuente.
 * Requiere: npm install --save-dev sharp
 * Uso: node scripts/generate-icons.js
 */

const sharp = require('sharp')
const path = require('path')
const fs = require('fs')

const srcSvg = path.join(__dirname, '../build/nomi-icon.svg')
const iconsDir = path.join(__dirname, '../build/icons')
const buildDir = path.join(__dirname, '../build')

if (!fs.existsSync(iconsDir)) fs.mkdirSync(iconsDir, { recursive: true })

const sizes = [16, 32, 64, 128, 256, 512]

async function run() {
  // Genera cada tamaño en build/icons/
  for (const size of sizes) {
    const out = path.join(iconsDir, `nomi-icon-${size}.png`)
    await sharp(srcSvg).resize(size, size).png().toFile(out)
    console.log(`✓ nomi-icon-${size}.png`)
  }

  // build/icon.png = 512x512 (usado en mac + main.js)
  const iconOut = path.join(buildDir, 'icon.png')
  await sharp(srcSvg).resize(512, 512).png().toFile(iconOut)
  console.log('✓ build/icon.png')

  console.log('\nIconos generados correctamente.')
}

run().catch(console.error)
