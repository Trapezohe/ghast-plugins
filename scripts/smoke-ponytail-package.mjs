// Run only in a disposable, read-only CI job: installed hook scripts are executable code.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const root=fs.mkdtempSync(path.join(os.tmpdir(),'ghast-package-smoke-'));
try {
 const plugin=path.join(root,'plugin'); fs.cpSync('plugins/ponytail',plugin,{recursive:true});
 const data=path.join(root,'session');fs.mkdirSync(data);
 const run=(hook_event_name,prompt='')=>{
  const r=spawnSync(process.execPath,[path.join(plugin,'hooks/ghast.cjs')],{input:JSON.stringify({hook_event_name,prompt}),encoding:'utf8',cwd:root,timeout:10000,env:{...process.env,NODE_OPTIONS:undefined,PLUGIN_ROOT:plugin,PLUGIN_DATA:data}});
  assert.equal(r.status,0,r.stderr);return JSON.parse(r.stdout).hookSpecificOutput.additionalContext;
 };
 run('SessionStart'); assert.match(run('UserPromptSubmit','Build a form'),/level: full/);
 assert.match(run('UserPromptSubmit','/ponytail lite'),/level: lite/);
 assert.match(run('SubagentStart'),/level: lite/);
 assert.equal(run('UserPromptSubmit','stop ponytail'),'');
 fs.rmSync(plugin,{recursive:true});assert(!fs.existsSync(plugin));
 console.log('Isolated Ponytail copy, hook modes, subagent inheritance and cleanup PASS (not Electron install or account authorization)');
} finally {fs.rmSync(root,{recursive:true,force:true});}
