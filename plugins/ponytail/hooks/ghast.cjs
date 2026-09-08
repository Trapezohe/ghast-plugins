// Ghast adapter. Rules and mode filtering are unchanged author-provided MIT source.
const fs = require('node:fs');
const path = require('node:path');
const { filterSkillBodyForMode } = require('../upstream/hooks/ponytail-instructions');
const { isDeactivationCommand } = require('../upstream/hooks/ponytail-config');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  const event = JSON.parse(input);
  const statePath = path.join(process.env.PLUGIN_DATA, 'mode.json');
  let mode = fs.existsSync(statePath) ? JSON.parse(fs.readFileSync(statePath, 'utf8')) : 'full';
  const prompt = String(event.prompt ?? '').trim();
  if (event.hook_event_name === 'UserPromptSubmit') {
    const command = prompt.match(/^[/@$]ponytail(?::ponytail)?(?:\s+(lite|full|ultra|off))?\s*$/i);
    if (command) mode = command[1]?.toLowerCase() ?? (mode === 'off' ? 'full' : mode);
    if (isDeactivationCommand(prompt)) mode = 'off';
  }
  if (event.hook_event_name !== 'SubagentStart') fs.writeFileSync(statePath, JSON.stringify(mode));
  const context = event.hook_event_name === 'SessionStart' || mode === 'off' ? '' :
    'PONYTAIL MODE ACTIVE — level: ' + mode + '\n\n' +
    filterSkillBodyForMode(fs.readFileSync(path.join(__dirname, '../rules/ponytail.md'), 'utf8'), mode);
  process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:event.hook_event_name,additionalContext:context}}));
});
