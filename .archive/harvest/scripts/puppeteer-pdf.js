#!/usr/bin/env node
/**
 * puppeteer-pdf.js - HTMLをA4 PDFに変換
 * Usage: node puppeteer-pdf.js input.html output.pdf
 * Install: npm install puppeteer
 */

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

async function htmlToPdf(inputPath, outputPath) {
  const absolutePath = path.resolve(inputPath);
  if (!fs.statSync(absolutePath).isFile()) throw new Error('Input must be a file');
  if (fs.existsSync(outputPath)) {
    const input = fs.statSync(absolutePath);
    const output = fs.statSync(outputPath);
    if (input.dev === output.dev && input.ino === output.ino) {
      throw new Error('Input and output must be different files');
    }
  }
  const puppeteer = require('puppeteer');
  console.log('Launching browser...');
  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage();
    console.log(`Loading: ${absolutePath}`);
    await page.goto(pathToFileURL(absolutePath).href, {
      waitUntil: 'networkidle0',
      timeout: 30000
    });

    // Finish fonts and Chart.js animations before printing. This works with
    // current Puppeteer, which no longer exposes page.waitForTimeout().
    await page.evaluate(async () => {
      await document.fonts.ready;
      const requiredCharts = document.querySelectorAll('canvas[data-chartjs]');
      if (requiredCharts.length && typeof Chart === 'undefined') {
        throw new Error('Chart.js failed to load; required report charts are missing');
      }
      requiredCharts.forEach(canvas => {
        if (!Chart.getChart(canvas)) {
          throw new Error(`Required chart was not initialized: ${canvas.id}`);
        }
      });
      if (typeof Chart !== 'undefined') {
        Object.values(Chart.instances).forEach(chart => {
          chart.stop();
          chart.update('none');
        });
      }
    });

    console.log('Generating PDF...');
    await page.pdf({
      path: outputPath,
      format: 'A4',
      printBackground: true,
      margin: { top: '0', bottom: '0', left: '0', right: '0' },
      preferCSSPageSize: true
    });
    console.log(`Done: ${outputPath}`);
  } finally {
    await browser.close();
  }
}

const args = process.argv.slice(2);
if (args.length !== 2) {
  console.error('Usage: node puppeteer-pdf.js <input.html> <output.pdf>');
  process.exitCode = 1;
} else {
  htmlToPdf(args[0], args[1]).catch(err => {
    console.error('Error:', err.message);
    process.exitCode = 1;
  });
}
