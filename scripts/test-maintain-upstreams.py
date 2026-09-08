#!/usr/bin/env python3
"""Small offline regression: provenance, update boundaries and failed-check retention."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile

spec = importlib.util.spec_from_file_location('maintenance', Path(__file__).with_name('maintain-upstreams.py'))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
assert m.github_repo('https://github.com/owner/project/tree/main/plugins') == 'owner/project'
assert m.github_repo('https://github.com.evil.test/owner/project') is None
for bad in ('../escape', '/tmp/escape', 'a/../../b', 'a\\b'):
    try: m.safe_relative(bad)
    except ValueError: pass
    else: raise AssertionError(bad)
with tempfile.TemporaryDirectory() as tmp:
    m.ROOT = Path(tmp).resolve(); m.STATE = m.ROOT / 'state.json'
    root = m.ROOT / 'plugins/demo'; root.mkdir(parents=True)
    manifest = {'name':'demo','version':'1.0-ghast.1','description':'English', 'extensions':{'ai.trapezohe.ghast':{'upstreamRevision':'a'*40,'descriptions':{'en':'English','zh-CN':'中文'}}}}
    m.write_json(root/'plugin.json', manifest); (root/'rule.md').write_bytes(b'old'); (root/'mcp.json').write_text('{"preserve":true}')
    monitor={'kind':'github','repository':'owner/repo','ref':'HEAD','packagedRevision':'a'*40}
    sources={'demo':{'policy':'mapped-pr','monitors':[monitor], 'update':{'repository':'owner/repo','files':{'upstream.md':'rule.md'},'hashes':{'rule.md':hashlib.sha256(b'old').hexdigest()}}}}
    m.inspect=lambda _: {'revision':'b'*40}
    report, observations=m.check(sources); assert report['demo']['checks'][0]['state']=='update-available'
    m.fetch=lambda url: b'new'
    applied=m.apply_updates(sources,report); assert len(applied)==1
    updated=m.read_json(root/'plugin.json')
    assert updated['version']=='1.0-ghast.2' and updated['description']==manifest['description']
    assert updated['extensions']['ai.trapezohe.ghast']['descriptions']==manifest['extensions']['ai.trapezohe.ghast']['descriptions']
    assert (root/'mcp.json').read_text()=='{"preserve":true}' and (root/'rule.md').read_bytes()==b'new'
    assert m.apply_updates(sources,report)==[]
    m.write_json(m.STATE,observations)
    report,_=m.check(sources); assert report['demo']['checks'][0]['state']=='unchanged'
    m.inspect=lambda _: (_ for _ in ()).throw(OSError('offline'))
    report,_=m.check(sources); assert report['demo']['checks'][0]['state']=='error'
    assert m.read_json(m.STATE)==observations
    # Local Ghast edits must stop an upstream overwrite.
    (root/'rule.md').write_bytes(b'local edit')
    report['demo']['checks'][0]['result']={'revision':'c'*40}
    try: m.apply_updates(sources,report)
    except ValueError as e: assert 'local overlay changed' in str(e)
    else: raise AssertionError('Local changes overwritten')
    assert (root/'rule.md').read_bytes()==b'local edit'
print('maintenance boundaries, idempotency, localized overlays and error reporting PASS')
