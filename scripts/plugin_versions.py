"""Use only versions read from the packaged upstream revision; never invent one."""
import json
import tomllib


def read_upstream_version(data, path):
    if path.rsplit('/', 1)[-1] == 'VERSION':
        version = data.decode('utf-8').strip()
    elif path.endswith('.toml'):
        document = tomllib.loads(data.decode('utf-8'))
        version = document.get('project', {}).get('version') or document.get('tool', {}).get('poetry', {}).get('version')
    else:
        version = json.loads(data).get('version')
    if version is not None and (not isinstance(version, str) or not version.strip()):
        raise ValueError(f'{path}: upstream version must be a non-empty string')
    return version


def apply_version(manifest, source):
    evidence = source.get('versionSource')
    version = evidence.get('version') if evidence else None
    if evidence:
        revision = manifest.get('extensions', {}).get('ai.trapezohe.ghast', {}).get('upstreamRevision')
        if evidence['revision'] != revision:
            raise ValueError(f"{manifest['name']}: version evidence does not match packaged upstream revision")
    if version is None:
        manifest.pop('version', None)
    else:
        manifest['version'] = version
