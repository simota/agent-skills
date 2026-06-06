# Bundle Size Analysis

## Analysis Tools

**webpack-bundle-analyzer:**
```bash
# Install
npm install --save-dev webpack-bundle-analyzer

# Add to webpack config
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin()
  ]
};

# Or run standalone
npx webpack-bundle-analyzer stats.json
```

**source-map-explorer:**
```bash
# Install
npm install --save-dev source-map-explorer

# Build with source maps
npm run build

# Analyze
npx source-map-explorer 'build/static/js/*.js'
```

**bundlephobia (online):**
```bash
# Check package size before installing
npx bundlephobia moment
# minified: 72.1kB, gzipped: 25.3kB

npx bundlephobia date-fns
# minified: 6.9kB (tree-shaken), gzipped: 2.5kB
```

## Bundle Size Budget

```json
// package.json
{
  "bundlesize": [
    {
      "path": "./build/static/js/main.*.js",
      "maxSize": "200 kB"
    },
    {
      "path": "./build/static/js/*.chunk.js",
      "maxSize": "100 kB"
    }
  ]
}
```

## Size Optimization Strategies

| Issue | Solution |
|-------|----------|
| Large moment.js | Replace with date-fns (tree-shakeable) or Intl API |
| Full lodash import | Import specific: `import debounce from 'lodash/debounce'` |
| Unused exports | Enable tree-shaking, use ES modules |
| Large icons | Use SVG sprites or icon fonts |
| Multiple chart libraries | Standardize on one |
| Polyfills for modern browsers | Use differential serving |

## Vite/Rollup Visualization

```javascript
// vite.config.js
import { visualizer } from 'rollup-plugin-visualizer';

export default {
  plugins: [
    visualizer({
      filename: 'dist/stats.html',
      open: true,
      gzipSize: true,
    }),
  ],
};
```
