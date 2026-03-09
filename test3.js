const child_process = require('child_process');
const p = child_process.spawn('npm', ['start'], {
  cwd: './frontend',
  env: { ...process.env, FORCE_COLOR: '1' },
  stdio: 'inherit'
});
setTimeout(() => {
  p.kill();
}, 5000);
