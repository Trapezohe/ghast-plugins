#!/usr/bin/env python3
"""Audit declared connector auth against public, unauthenticated server metadata."""
import concurrent.futures
import datetime
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def fetch(url):
    if not url.startswith('https://') or any(c in url for c in '${}'):
        return {'url': url, 'error': 'Not a fixed public HTTPS URL'}
    try:
        response = urllib.request.urlopen(urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'Ghast-Connector-Auth-Audit/1.0'}), timeout=6)
    except urllib.error.HTTPError as error:
        response = error
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        return {'url': url, 'error': str(error)}
    with response:
        body = response.read(256 * 1024) if "json" in response.headers.get("Content-Type", "") else b""
        result = {'url': url, 'status': response.code}
        challenge = response.headers.get('WWW-Authenticate')
        if challenge: result['challenge'] = challenge
        try:
            data = json.loads(body)
            if isinstance(data, dict):
                result['metadata'] = {key: data[key] for key in ['resource', 'authorization_servers', 'issuer', 'authorization_endpoint', 'token_endpoint', 'registration_endpoint', 'client_id_metadata_document_supported', 'code_challenge_methods_supported'] if key in data}
        except (ValueError, UnicodeDecodeError):
            pass
        return result

def inspect(url):
    first = fetch(url)
    evidence = [first]
    match = re.search(r'resource_metadata="([^"]+)"', first.get('challenge', ''))
    origin = urllib.parse.urlsplit(url)
    protected_url = match.group(1) if match else f'{origin.scheme}://{origin.netloc}/.well-known/oauth-protected-resource{origin.path.rstrip("/")}'
    protected = fetch(protected_url)
    evidence.append(protected)
    servers = protected.get('metadata', {}).get('authorization_servers', [])
    if servers and isinstance(servers[0], str):
        issuer = urllib.parse.urlsplit(servers[0])
        auth_url = f'{issuer.scheme}://{issuer.netloc}/.well-known/oauth-authorization-server{issuer.path.rstrip("/")}'
    else:
        auth_url = f'{origin.scheme}://{origin.netloc}/.well-known/oauth-authorization-server'
    auth = fetch(auth_url)
    evidence.append(auth)
    metadata = auth.get('metadata', {})
    oauth = bool(metadata.get('authorization_endpoint') or servers)
    return {'oauthAdvertised': oauth, 'dynamicRegistration': bool(metadata.get('registration_endpoint')), 'clientMetadataDocument': metadata.get('client_id_metadata_document_supported') is True, 'evidence': evidence}

def main():
    records = []
    for path in sorted((ROOT/'plugins').glob('*/mcp.json')):
        manifest = json.loads((path.parent/'plugin.json').read_text())
        extensions = manifest.get('extensions', {}).get('ai.trapezohe.ghast', {}).get('mcpServerExtensions', {})
        for name, config in json.loads(path.read_text()).get('mcpServers', {}).items():
            extra = extensions.get(name, {})
            credential_keys = set(re.findall(r'\$VAULT:([\w-]+)', json.dumps([extra.get('credentialHeaders', {}), extra.get('credentialEnv', {})])))
            required_credentials = sorted(credential_keys - set(extra.get('optionalCredentials', [])))
            records.append({'requiredCredentials': required_credentials, 'plugin': path.parent.name, 'server': name, 'url': config.get('url'), 'transport': 'remote' if config.get('url') else 'local', 'manualCredentials': bool(extra.get('credentialHeaders') or extra.get('credentialEnv')), 'clientRequired': bool(extra.get('oauthClientRequired')), 'oauthRequired': bool(extra.get('oauthRequired'))})
    urls = sorted({r['url'] for r in records if r['url']})
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(inspect, url): url for url in urls}
        results = {}
        for future in concurrent.futures.as_completed(futures):
            results[futures[future]] = future.result()
            if len(results) % 25 == 0: print(f"Checked {len(results)}/{len(urls)} remote URLs", flush=True)
    for row in records:
        if row['url']:
            row.update(results[row['url']])
            row['review'] = 'oauth-advertised-with-required-credentials' if row['oauthAdvertised'] and row['requiredCredentials'] else 'oauth-advertised' if row['oauthAdvertised'] else 'official-documentation-review-required'
        else: row['review'] = 'local-runtime-authentication'
    report = {'checkedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'scope': 'All packaged MCP definitions; no credentials, token exchange or tool execution. Missing discovery metadata does not prove OAuth is unsupported.', 'servers': records}
    target = ROOT/'maintenance/connector-auth-audit.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f'Audited {len(records)} services / {len(urls)} remote URLs: {target}')

if __name__ == '__main__': main()
