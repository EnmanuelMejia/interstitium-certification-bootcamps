import json, re, sys

def check(slug):
    d = json.load(open('content/%s.json' % slug))
    f = json.load(open('content/%s/fragments/extended.json' % slug))
    domains = set(x['id'] for x in d['domains'])
    existing = set(x['id'] for x in d.get('labs', []))
    seen = set()
    errs = []
    kinds = set()
    for lab in f['labs_add']:
        if lab['id'] in existing: errs.append('lab collides with existing: '+lab['id'])
        if lab['id'] in seen: errs.append('dup id: '+lab['id'])
        seen.add(lab['id'])
        for c in lab['checks']:
            try: re.compile(c['command_pattern'])
            except Exception as e: errs.append('bad regex %s: %s' % (lab['id'], e))
    for sim in f['simulations']:
        if sim['id'] in seen: errs.append('dup id: '+sim['id'])
        seen.add(sim['id']); kinds.add(sim['kind'])
        if sim['domain_id'] not in domains: errs.append('bad domain %s in %s' % (sim['domain_id'], sim['id']))
        if sim['kind'] not in ('troubleshoot','branching','ordering','config-check'):
            errs.append('bad kind %s in %s' % (sim['kind'], sim['id']))
    for cs in f['consoleSims']:
        if cs['id'] in seen: errs.append('dup id: '+cs['id'])
        seen.add(cs['id'])
        if cs['domain_id'] not in domains: errs.append('bad domain %s in %s' % (cs['domain_id'], cs['id']))
    for m in f['terminalMissions']:
        if m['id'] in seen: errs.append('dup id: '+m['id'])
        seen.add(m['id'])
        if m['domain_id'] not in domains: errs.append('bad domain %s in %s' % (m['domain_id'], m['id']))
        for c in m['checks']:
            try: re.compile(c['command_pattern'])
            except Exception as e: errs.append('bad regex %s: %s' % (m['id'], e))
    status = 'OK' if not errs else 'ERRORS'
    print('%s labs=%d sims=%d(kinds=%d) consoles=%d missions=%d %s' % (
        slug, len(f['labs_add']), len(f['simulations']), len(kinds),
        len(f['consoleSims']), len(f['terminalMissions']), status))
    for e in errs: print('    ' + e)
    return not errs

ok = True
for slug in sys.argv[1:]:
    ok = check(slug) and ok
sys.exit(0 if ok else 1)
