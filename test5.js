const child_process = require('child_process');
const p = child_process.spawn('npm', ['start'], {
  cwd: './frontend',
  env: { ...process.env, FORCE_COLOR: '1', PORT: '3007' },
  stdio: 'pipe'
});
p.stdout.on('data', d => process.stdout.write(d));
p.stderr.on('data', d => process.stderr.write(d));
setTimeout(() => {
  p.kill();
  process.exit(0);
}, 20000);
