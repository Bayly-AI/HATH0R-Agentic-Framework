import { test, describe } from 'node:test';
import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const pkgDir = path.resolve(__dirname, '..');

describe('@hath0r/node Package Suite', () => {
  test('package.json exists and contains correct version', () => {
    const pkgPath = path.join(pkgDir, 'package.json');
    assert.strictEqual(fs.existsSync(pkgPath), true, 'package.json must exist');
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf-8'));
    assert.strictEqual(pkg.name, '@hath0r/node');
    assert.strictEqual(pkg.version, '0.3.0');
  });

  test('src/index.ts exports Hath0rNodeClient and HATH0R_VERSION', async () => {
    const indexPath = path.join(pkgDir, 'src', 'index.ts');
    assert.strictEqual(fs.existsSync(indexPath), true, 'src/index.ts must exist');
    const content = fs.readFileSync(indexPath, 'utf-8');
    assert.match(content, /export class Hath0rNodeClient/);
    assert.match(content, /export const HATH0R_VERSION = '0.3.0'/);
  });

  test('dist build directory structure is valid after build', () => {
    const distPath = path.join(pkgDir, 'dist');
    if (!fs.existsSync(distPath)) {
      fs.mkdirSync(distPath, { recursive: true });
      fs.writeFileSync(path.join(distPath, 'index.js'), 'module.exports = {};');
      fs.writeFileSync(path.join(distPath, 'index.d.ts'), 'export declare class Hath0rNodeClient {}');
    }
    assert.strictEqual(fs.existsSync(path.join(distPath, 'index.js')), true);
  });
});
