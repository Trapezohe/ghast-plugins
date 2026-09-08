#!/usr/bin/env python3
"""Check official upstreams and prepare explicitly mapped updates; never run downloaded code."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'maintenance/upstreams.json'
STATE = ROOT / 'maintenance/observed.json'
MAX_BYTES = 12 * 1024 * 1024


def read_json(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')


def github_repo(url):
    p = urllib.parse.urlsplit(url or '')
    parts = p.path.strip('/').split('/')
    if p.hostname == 'github.com' and len(parts) >= 2:
        return '/'.join(parts[:2]).removesuffix('.git')
    return None


def inventory():
    previous = read_json(SOURCES) if SOURCES.exists() else {}
    records = {}
    for manifest in sorted((ROOT / 'plugins').glob('*/plugin.json')):
        m = read_json(manifest)
        g = m.get('extensions', {}).get('ai.trapezohe.ghast', {})
        urls = list(dict.fromkeys(u for u in [g.get('officialConnectorSource'), m.get('repository'), m.get('homepage')] if isinstance(u, str)))
        repositories = list(dict.fromkeys(r for u in urls if (r := github_repo(u))))
        monitors = []
        for i, repository in enumerate(repositories):
            revision = g.get('upstreamRevision') if i == 0 else None
            monitors.append({'kind': 'github', 'repository': repository, 'ref': 'HEAD',
                             'packagedRevision': revision if re.fullmatch(r'[0-9a-f]{40}', revision or '') else None})
        config = manifest.parent / 'mcp.json'
        for name, server in (read_json(config).get('mcpServers', {}) if config.exists() else {}).items():
            url = server.get('url', '')
            if url.startswith('https://') and not any(c in url for c in '${}'):
                monitors.append({'kind': 'endpoint', 'server': name, 'url': url})
            command = server.get('command')
            args = server.get('args', [])
            if command in ('npx', 'uvx'):
                package = next((x for x in args if isinstance(x, str) and not x.startswith('-')), '')
                if command == 'npx' and re.fullmatch(r'(?:@[\w.-]+/)?[\w.-]+(?:@[\w.^~*+-]+)?', package):
                    name, sep, version = package.rpartition('@')
                    if not sep or not name: name, version = package, None
                    monitors.append({'kind': 'npm', 'package': name, 'packagedVersion': version})
                elif command == 'uvx' and re.fullmatch(r'[\w.-]+(?:==[\w.+-]+)?', package):
                    name, _, version = package.partition('==')
                    monitors.append({'kind': 'pypi', 'package': name, 'packagedVersion': version or None})
        records[m['name']] = {'provenance': urls, 'monitors': monitors,
                              'update': previous.get(m['name'], {}).get('update'),
                              'policy': 'mapped-pr' if previous.get(m['name'], {}).get('update') else 'review-required'}
    return records


class Redirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        new = urllib.parse.urlsplit(newurl)
        if new.scheme != 'https' or (req.has_header('Authorization') and new.hostname != 'api.github.com'):
            raise ValueError('Unexpected upstream redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, *, endpoint=False):
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Upstreams must use public HTTPS URLs without credentials')
    if parsed.hostname == 'api.github.com' and os.environ.get('GHAST_GH_API') == '1':
        return subprocess.run(['gh', 'api', parsed.path.lstrip('/')], check=True, capture_output=True, timeout=30).stdout
    headers = {'User-Agent': 'Ghast-upstream-maintenance', 'Accept': 'application/json'}
    if parsed.hostname == 'api.github.com' and os.environ.get('GH_TOKEN'):
        headers['Authorization'] = 'Bearer ' + os.environ['GH_TOKEN']
    try:
        with urllib.request.build_opener(Redirects()).open(urllib.request.Request(url, headers=headers), timeout=20) as response:
            if endpoint: return {'status': 'reachable', 'http': response.status}
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES: raise ValueError('Upstream file exceeds download limit')
            return data
    except urllib.error.HTTPError as error:
        if endpoint and error.code in (400, 401, 403, 405, 406):
            return {'status': 'auth-or-protocol-required', 'http': error.code}
        raise


def inspect(monitor):
    kind = monitor['kind']
    if kind == 'github':
        repo = monitor['repository']
        data = json.loads(fetch(f'https://api.github.com/repos/{repo}/commits/{urllib.parse.quote(monitor["ref"], safe="")}'))
        return {'revision': data['sha']}
    if kind == 'npm':
        package = urllib.parse.quote(monitor['package'], safe='')
        return {'version': json.loads(fetch(f'https://registry.npmjs.org/{package}/latest'))['version']}
    if kind == 'pypi':
        return {'version': json.loads(fetch(f'https://pypi.org/pypi/{monitor["package"]}/json'))['info']['version']}
    if kind == 'endpoint': return fetch(monitor['url'], endpoint=True)
    raise ValueError(f'Unknown monitor kind: {kind}')


def monitor_key(monitor):
    return json.dumps({k: v for k, v in monitor.items() if not k.startswith('packaged') and k != 'server'}, sort_keys=True)


def check(sources):
    old = read_json(STATE) if STATE.exists() else {}
    unique = {monitor_key(m): m for s in sources.values() for m in s['monitors']}
    observations = {}
    def run(pair):
        key, monitor = pair
        try: return key, inspect(monitor)
        except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
            return key, {'error': str(error)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(run, pair) for pair in unique.items()]
        for count, future in enumerate(concurrent.futures.as_completed(futures), 1):
            key, value = future.result()
            observations[key] = value
            if count % 50 == 0: print(f'Checked {count}/{len(unique)} sources', flush=True)
    report = {}
    for plugin, source in sources.items():
        items = []
        for m in source['monitors']:
            key = monitor_key(m)
            value = observations[key]
            packaged = m.get('packagedRevision') or m.get('packagedVersion')
            latest = value.get('revision') or value.get('version')
            baseline = old.get(key)
            state = 'error' if 'error' in value else 'unchanged'
            if state != 'error':
                if baseline is None: state = 'baseline'
                elif baseline != value: state = 'changed'
                if latest and packaged and packaged != 'latest' and latest != packaged: state = 'update-available'
            items.append({'monitor': m, 'result': value, 'state': state})
        report[plugin] = {'policy': source['policy'], 'checks': items,
                          'coverage': 'monitored' if items else 'manual-source-review'}
    return report, observations


def safe_relative(value):
    p = PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or '\\' in value or value == '.':
        raise ValueError(f'Unsafe mapped path: {value}')
    return value


def apply_updates(sources, report):
    applied = []
    for name, source in sources.items():
        update = source.get('update')
        if not update: continue
        result = next(x for x in report[name]['checks'] if x['monitor'].get('repository') == update['repository'])
        revision = result['result'].get('revision')
        manifest_path = ROOT / 'plugins' / name / 'plugin.json'
        manifest = read_json(manifest_path)
        g = manifest['extensions']['ai.trapezohe.ghast']
        if not revision or revision == g.get('upstreamRevision'): continue
        if not re.fullmatch(r'[0-9a-f]{40}', revision): raise ValueError('Invalid upstream revision')
        match = re.fullmatch(r'(.+-ghast\.)(\d+)', manifest['version'])
        if not match: raise ValueError(f'{name}: unsupported version format')
        files = []
        plugin_root = manifest_path.parent.resolve()
        for src, dst in update['files'].items():
            safe_relative(src); safe_relative(dst)
            if dst in ('plugin.json', 'mcp.json') or dst.startswith('ai.trapezohe.ghast/'):
                raise ValueError('Adapters and permission metadata cannot be overwritten')
            target = plugin_root / dst
            if not target.resolve().is_relative_to(plugin_root): raise ValueError('Mapped symlink escapes plugin')
            before = target.read_bytes()
            if hashlib.sha256(before).hexdigest() != update['hashes'][dst]:
                raise ValueError(f'{name}/{dst}: local overlay changed; mapping needs review')
            after = fetch(f'https://raw.githubusercontent.com/{update["repository"]}/{revision}/{urllib.parse.quote(src, safe="/")}')
            files.append((target, before, after))
        changed = [str(p.relative_to(ROOT)) for p, before, after in files if before != after]
        for target, _, data in files:
            target.write_bytes(data)
            update['hashes'][str(target.relative_to(plugin_root))] = hashlib.sha256(data).hexdigest()
        previous_revision = g.get('upstreamRevision')
        readme = plugin_root / 'README.md'
        if previous_revision and readme.exists():
            readme.write_text(readme.read_text().replace(previous_revision, revision))
        g['upstreamRevision'] = revision
        manifest['version'] = match[1] + str(int(match[2]) + 1)
        write_json(manifest_path, manifest)
        for m in source['monitors']:
            if m.get('repository') == update['repository']: m['packagedRevision'] = revision
        applied.append({'plugin': name, 'revision': revision, 'files': changed, 'review': 'required'})
    return applied


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', action='store_true')
    parser.add_argument('--validate', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--plugin', action='append')
    parser.add_argument('--output', type=Path, default=ROOT / 'maintenance-report.json')
    args = parser.parse_args()
    if args.inventory:
        write_json(SOURCES, inventory()); return
    sources = read_json(SOURCES)
    if args.validate:
        expected = inventory()
        if sources != expected: raise ValueError('Source inventory is stale; run --inventory')
        for name, source in sources.items():
            update = source.get('update')
            if update:
                if update['repository'] not in [m.get('repository') for m in source['monitors']]: raise ValueError('Unmonitored mapping source')
                for src, dst in update['files'].items():
                    safe_relative(src); safe_relative(dst)
                    target = ROOT / 'plugins' / name / dst
                    if hashlib.sha256(target.read_bytes()).hexdigest() != update['hashes'][dst]: raise ValueError(f'Mapping hash mismatch: {target}')
        print(f'validated {len(sources)} upstream records'); return
    selected = {k: v for k, v in sources.items() if not args.plugin or k in args.plugin}
    if not selected: raise ValueError('No matching plugins')
    report, observations = check(selected)
    applied = apply_updates(selected, report) if args.apply else []
    write_json(args.output, {'plugins': report, 'applied': applied})
    if args.apply:
        state = read_json(STATE) if STATE.exists() else {}
        # Failed checks never replace the last successful observation.
        state.update({k: v for k, v in observations.items() if 'error' not in v})
        write_json(STATE, state)
        write_json(SOURCES, sources)
    errors = sum('error' in r for r in observations.values())
    print(f'checked {len(selected)} plugins / {len(observations)} distinct sources; {errors} errors; {len(applied)} mapped updates')
    if errors: raise SystemExit(1)


if __name__ == '__main__':
    main()
