#!/usr/bin/env node
/**
 * puppeteer-pdf.js - HTMLをA4 PDFに変換
 *
 * 使用方法:
 *   node puppeteer-pdf.js input.html output.pdf
 *
 * インストール:
 *   npm install puppeteer
 */

const puppeteer = require('puppeteer');
const path = require('path');

async function htmlToPdf(inputPath, outputPath) {
  const absolutePath = path.resolve(inputPath);

  console.log('Launching browser...');
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  console.log(`Loading: ${absolutePath}`);
  await page.goto(`file://${absolutePath}`, {
    waitUntil: 'networkidle0',
    timeout: 30000
  });

  // Chart.jsの描画完了を待機
  await page.waitForTimeout(1000);

  console.log('Generating PDF...');
  await page.pdf({
    path: outputPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '0',
      bottom: '0',
      left: '0',
      right: '0'
    },
    preferCSSPageSize: true
  });

  await browser.close();
  console.log(`Done: ${outputPath}`);
}

// CLI
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node puppeteer-pdf.js <input.html> <output.pdf>');
  process.exit(1);
}

htmlToPdf(args[0], args[1]).catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
