const child_process = require('child_process');
const p = child_process.spawn('npm', ['start'], {
  cwd: './frontend',
  env: { ...process.env, FORCE_COLOR: '1', PORT: '3006' },
  stdio: 'pipe'
});
p.stdout.pipe(process.stdout);
p.stderr.pipe(process.stderr);
setTimeout(() => {
  p.kill();
}, 10000);
