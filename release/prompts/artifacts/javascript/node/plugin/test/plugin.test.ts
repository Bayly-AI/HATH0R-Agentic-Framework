import { test, describe } from 'node:test';
import assert from 'node:assert';
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { Hath0rClient } from '../src/client.ts';
import { Hath0rAgenticPlugin } from '../src/index.ts';

describe('hath0r-cli-node-plugin Node Package Suite', () => {
  test('package.json exists and contains correct name and version', () => {
    const pkgPath = resolve(process.cwd(), 'package.json');
    assert.strictEqual(existsSync(pkgPath), true, 'package.json must exist');
    const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
    assert.strictEqual(pkg.name, 'hath0r-cli-node-plugin');
    assert.strictEqual(pkg.version, '0.3.0');
  });

  test('Hath0rClient initializes and resolves CLI path', () => {
    const client = new Hath0rClient();
    assert.ok(client.cliPath, 'CLI path should be resolved');
    assert.ok(client.workspaceDir, 'Workspace directory should be resolved');
  });

  test('Hath0rAgenticPlugin wraps tool function cleanly', async () => {
    const plugin = new Hath0rAgenticPlugin({ cliPath: 'echo' });
    let executed = false;
    const result = await plugin.wrapTool('developer', 'testTool', async () => {
      executed = true;
      return 'plugin_success';
    });
    assert.strictEqual(executed, true);
    assert.strictEqual(result, 'plugin_success');
  });

  test('expressGateMiddleware returns function handler', () => {
    const plugin = new Hath0rAgenticPlugin({ cliPath: 'echo' });
    const middleware = plugin.expressGateMiddleware();
    assert.strictEqual(typeof middleware, 'function');
  });
});
