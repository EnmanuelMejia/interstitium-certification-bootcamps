#!/usr/bin/env python3
"""Worker 3 (resources): per-bootcamp resource packs for the Enterprise CBT upgrade.

Reads content/<slug>.json, mines lessons[] for terms/definitions, and writes
content/<slug>/fragments/resources.json = {"resources": {cheatsheet, glossary, links, checklist}}.

- cheatsheet: 3-6 sections mined from the bootcamp's own concepts/pitfalls/walkthroughs/scenario whys
- glossary: 12-25 terms w/ definitions drawn from the bootcamp's own sentences
- links: 4-8 curated official links; EVERY url curl-verified HTTP 200 (dropped otherwise)
- checklist: 8-12 items, generic readiness + 2-4 bootcamp-specific from domain names

Original content only. Never edits content/<slug>.json. Does not touch engine/ or templates/.
"""
import json, os, re, glob, subprocess
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.expanduser('~/workspace/cert-bootcamps')
CONTENT = os.path.join(ROOT, 'content')
RESDIR = os.path.join(ROOT, 'resources')
os.makedirs(RESDIR, exist_ok=True)
LOG = os.path.join(RESDIR, 'link-check.log')

UA = 'Mozilla/5.0 (compatible; ILB-linkcheck/1.0)'

# ---------------------------------------------------------------- link pool --
# (label, url, note). Curated official/vendor/standards references only.
CATS = {
'aws': [
 ("AWS certification portal","https://aws.amazon.com/certification","Official certification info and exam guides"),
 ("AWS documentation","https://docs.aws.amazon.com/","Official service documentation"),
 ("AWS Well-Architected Framework","https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html","Official architecture best practices"),
 ("AWS Architecture Center","https://aws.amazon.com/architecture/","Official AWS architecture guidance"),
 ("AWS whitepapers","https://aws.amazon.com/whitepapers/","Official AWS whitepapers"),
],
'azure': [
 ("Microsoft Learn — Azure","https://learn.microsoft.com/en-us/azure/","Official Azure documentation"),
 ("Microsoft certifications","https://learn.microsoft.com/en-us/certifications/","Official certification paths and exam pages"),
 ("Azure status and architecture","https://azure.microsoft.com/en-us/","Official Azure product pages"),
],
'k8s': [
 ("Kubernetes documentation","https://kubernetes.io/docs/home/","Official Kubernetes docs"),
 ("Kubernetes API reference","https://kubernetes.io/docs/reference/","Official API reference"),
 ("Cloud Native Computing Foundation","https://www.cncf.io/","Cloud-native project home"),
],
'docker': [
 ("Docker documentation","https://docs.docker.com/","Official Docker docs"),
 ("Docker get-started guide","https://docs.docker.com/get-started/","Official Docker getting-started"),
 ("Docker Engine reference","https://docs.docker.com/engine/","Official Docker Engine docs"),
 ("Docker Hub","https://hub.docker.com/","Official image registry"),
],
'terraform': [
 ("Terraform documentation","https://developer.hashicorp.com/terraform/docs","Official Terraform docs"),
 ("Terraform tutorials","https://developer.hashicorp.com/terraform/tutorials","Official Terraform tutorials"),
 ("Terraform Registry","https://registry.terraform.io/","Official provider/module registry"),
],
'vault': [
 ("Vault documentation","https://developer.hashicorp.com/vault/docs","Official Vault docs"),
 ("Vault tutorials","https://developer.hashicorp.com/vault/tutorials","Official Vault tutorials"),
 ("Consul documentation","https://developer.hashicorp.com/consul/docs","Official Consul docs"),
],
'python': [
 ("Python 3 documentation","https://docs.python.org/3/","Official Python docs"),
 ("Python tutorial","https://docs.python.org/3/tutorial/","Official Python tutorial"),
 ("Python standard library","https://docs.python.org/3/library/","Official standard library reference"),
],
'datalibs': [
 ("pandas documentation","https://pandas.pydata.org/docs/","Official pandas docs"),
 ("NumPy documentation","https://numpy.org/doc/","Official NumPy docs"),
 ("scikit-learn documentation","https://scikit-learn.org/stable/","Official scikit-learn docs"),
 ("Apache Spark documentation","https://spark.apache.org/docs/latest/","Official Spark docs"),
],
'aidocs': [
 ("OpenAI API documentation","https://platform.openai.com/docs","Official OpenAI API docs"),
 ("Anthropic API documentation","https://docs.anthropic.com/en/docs","Official Anthropic API docs"),
 ("Hugging Face documentation","https://huggingface.co/docs","Official Hugging Face docs"),
 ("PyTorch documentation","https://pytorch.org/docs/stable/index.html","Official PyTorch docs"),
],
'java': [
 ("Java documentation","https://docs.oracle.com/en/java/","Official Java docs"),
 ("Spring","https://spring.io","Official Spring home"),
 ("Spring guides","https://spring.io/guides","Official Spring getting-started guides"),
 ("Spring Framework reference","https://docs.spring.io/spring-framework/reference/","Official Spring Framework reference"),
 ("dev.java","https://dev.java/","Official Java developer portal"),
],
'cpp': [
 ("ISO C++","https://isocpp.org","Official C++ standards committee site"),
 ("cppreference","https://en.cppreference.com/w/","Community C++ reference"),
 ("WG21 — C++ standards committee","https://www.open-std.org/jtc1/sc22/wg21/","Official C++ standards working group"),
 ("Microsoft Learn — C++","https://learn.microsoft.com/en-us/cpp/","Official Microsoft C++ docs"),
 ("GNU C manual","https://www.gnu.org/software/gnu-c-manual/","GNU C language manual"),
 ("Open Standards — WG14 (C)","https://www.open-std.org/jtc1/sc22/wg14/","Official C standards working group"),
],
'dotnet': [
 ("Microsoft Learn — .NET","https://learn.microsoft.com/en-us/dotnet/","Official .NET docs"),
 ("C# documentation","https://learn.microsoft.com/en-us/dotnet/csharp/","Official C# docs"),
 (".NET home","https://dotnet.microsoft.com/","Official .NET site"),
 ("ASP.NET Core docs","https://learn.microsoft.com/en-us/aspnet/core/","Official ASP.NET Core docs"),
],
'web': [
 ("MDN Web Docs","https://developer.mozilla.org/en-US/docs/Web","Authoritative web platform reference"),
 ("React documentation","https://react.dev","Official React docs"),
 ("Django documentation","https://docs.djangoproject.com/","Official Django docs"),
 ("Node.js API docs","https://nodejs.org/docs/latest/api/","Official Node.js API reference"),
],
'data': [
 ("PostgreSQL documentation","https://www.postgresql.org/docs/","Official PostgreSQL docs"),
 ("PostgreSQL tutorial","https://www.postgresql.org/docs/current/tutorial.html","Official PostgreSQL tutorial"),
 ("Microsoft Learn — SQL","https://learn.microsoft.com/en-us/sql/","Official SQL Server docs"),
 ("SQL Server documentation","https://learn.microsoft.com/en-us/sql/sql-server/","Official SQL Server reference"),
 ("SQLite documentation","https://sqlite.org/docs.html","Official SQLite docs"),
],
'mongodb': [
 ("MongoDB documentation","https://www.mongodb.com/docs/","Official MongoDB docs"),
 ("MongoDB manual","https://www.mongodb.com/docs/manual/","Official MongoDB server manual"),
 ("MongoDB Atlas docs","https://www.mongodb.com/docs/atlas/","Official Atlas documentation"),
 ("MongoDB basics","https://www.mongodb.com/basics","Official MongoDB concept guides"),
 ("MongoDB University","https://university.mongodb.com","Official MongoDB training"),
],
'oracle': [
 ("Oracle Database documentation","https://docs.oracle.com/en/database/","Official Oracle Database docs"),
 ("Oracle Database 23ai docs","https://docs.oracle.com/en/database/oracle/oracle-database/","Official Oracle Database reference"),
 ("Oracle Database product page","https://www.oracle.com/database/","Official Oracle Database page"),
 ("Oracle Database technologies","https://www.oracle.com/database/technologies/","Official Oracle Database technology pages"),
 ("Oracle education","https://education.oracle.com","Official Oracle training and certification"),
],
'git': [
 ("Git documentation","https://git-scm.com/doc","Official Git docs"),
 ("GitHub Docs","https://docs.github.com/en","Official GitHub docs"),
 ("GitHub Codespaces docs","https://docs.github.com/en/codespaces","Official Codespaces docs"),
 ("VS Code documentation","https://code.visualstudio.com/docs","Official VS Code docs"),
 ("JetBrains IDEs","https://www.jetbrains.com/ides/","Official JetBrains IDE pages"),
],
'devops': [
 ("Google SRE book","https://sre.google/sre-book/table-of-contents/","Google's Site Reliability Engineering book"),
 ("OpenTelemetry documentation","https://opentelemetry.io/docs/","Official OpenTelemetry docs"),
],
'linux': [
 ("Linux man pages","https://man7.org/linux/man-pages/","Authoritative Linux man pages"),
 ("kernel.org documentation","https://www.kernel.org/doc/html/latest/","Official kernel docs"),
 ("The Linux Documentation Project","https://tldp.org/","Community Linux guides and HOWTOs"),
],
'lpi': [
 ("Linux Professional Institute","https://www.lpi.org","Official LPI certification home"),
],
'redhat': [
 ("Red Hat training and certification","https://www.redhat.com/en/services/training-and-certification","Official Red Hat training"),
 ("Red Hat documentation","https://docs.redhat.com/en","Official Red Hat docs"),
],
'comptia': [
 ("CompTIA","https://www.comptia.org","Official CompTIA certification home"),
],
'network': [
 ("RFC 791 — Internet Protocol (IPv4)","https://www.rfc-editor.org/rfc/rfc791.txt","Official IETF standard"),
 ("RFC 793 — Transmission Control Protocol","https://www.rfc-editor.org/rfc/rfc793.txt","Official IETF standard"),
 ("RFC 1035 — Domain Names (DNS)","https://www.rfc-editor.org/rfc/rfc1035.txt","Official IETF standard"),
 ("RFC 1918 — Private address allocation","https://www.rfc-editor.org/rfc/rfc1918.txt","Official IETF standard"),
 ("RFC 8446 — TLS 1.3","https://www.rfc-editor.org/rfc/rfc8446.txt","Official IETF standard"),
 ("RFC 2131 — DHCP","https://www.rfc-editor.org/rfc/rfc2131.txt","Official IETF standard"),
],
'security': [
 ("NIST SP 800-53 Rev. 5","https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final","Official NIST security controls catalog"),
 ("NIST Cybersecurity Framework","https://www.nist.gov/cyberframework","Official NIST CSF"),
 ("OWASP Top Ten","https://owasp.org/www-project-top-ten/","OWASP's top web application risks"),
 ("MITRE ATT&CK","https://attack.mitre.org/","MITRE's adversary tactics knowledge base"),
 ("FIPS 197 — Advanced Encryption Standard","https://csrc.nist.gov/pubs/fips/197/final","Official NIST AES standard"),
 ("CISA","https://www.cisa.gov/","Cybersecurity and Infrastructure Security Agency"),
 ("ISC2","https://www.isc2.org","Official ISC2 certification home"),
 ("ISACA","https://www.isaca.org","Official ISACA certification home"),
 ("NIST National Vulnerability Database","https://nvd.nist.gov/","Official CVE database"),
 ("Center for Internet Security","https://www.cisecurity.org/","CIS benchmarks and controls"),
],
'cybermil': [
 ("DoD Cyber Exchange","https://public.cyber.mil","Official DoD cyber resources"),
],
'nice': [
 ("NIST NICE Framework","https://www.nist.gov/itl/applied-cybersecurity/nice","Official NICE workforce framework"),
],
'blockchain': [
 ("Bitcoin developer documentation","https://developer.bitcoin.org/","Official Bitcoin developer docs"),
 ("Ethereum developer documentation","https://ethereum.org/en/developers/docs/","Official Ethereum developer docs"),
 ("NIST IR 8202 — Blockchain Technology Overview","https://csrc.nist.gov/pubs/ir/8202/final","Official NIST blockchain overview"),
 ("ISO 20022","https://www.iso20022.org/","Official ISO 20022 financial messaging standard"),
 ("XRPL documentation","https://xrpl.org/docs.html","Official XRP Ledger docs"),
 ("Stellar developers","https://developers.stellar.org/","Official Stellar developer docs"),
],
'career': [
 ("BLS Occupational Outlook Handbook","https://www.bls.gov/ooh/","Official U.S. labor market and salary data"),
 ("O*NET OnLine","https://www.onetonline.org/","Official U.S. Department of Labor occupation database"),
 ("CareerOneStop","https://www.careeronestop.org/","U.S. Department of Labor career resource"),
 ("My Next Move","https://www.mynextmove.org/","U.S. Department of Labor career explorer"),
 ("Apprenticeship.gov","https://www.apprenticeship.gov/","Official U.S. apprenticeship programs"),
],
'math': [
 ("NIST Digital Library of Mathematical Functions","https://dlmf.nist.gov/","Official NIST math reference"),
 ("Khan Academy — Math","https://www.khanacademy.org/math","Free math courses and practice"),
 ("Wolfram MathWorld","https://mathworld.wolfram.com/","Authoritative math encyclopedia"),
 ("American Mathematical Society","https://www.ams.org/","Professional mathematics society"),
 ("MIT OpenCourseWare","https://ocw.mit.edu/","Free MIT course materials"),
],
'hermetica': [
 ("Project Gutenberg","https://www.gutenberg.org/","Free public-domain texts, incl. Hermetic writings"),
 ("Project Gutenberg — Hermetic search","https://www.gutenberg.org/ebooks/search/?query=hermetic","Public-domain Hermetic texts on Gutenberg"),
 ("Stanford Encyclopedia of Philosophy","https://plato.stanford.edu/","Peer-reviewed philosophy reference"),
 ("Internet Encyclopedia of Philosophy","https://www.iep.utm.edu/","Peer-reviewed philosophy reference"),
 ("Perseus Digital Library","https://www.perseus.tufts.edu/","Tufts classical texts collection"),
 ("MIT Classics","https://classics.mit.edu/","Public-domain classical translations"),
],
'creative': [
 ("p5.js reference","https://p5js.org/reference/","Official p5.js reference"),
 ("MDN Canvas API","https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API","Authoritative Canvas API reference"),
 ("three.js documentation","https://threejs.org/docs/","Official three.js docs"),
],
'cloud': [
 ("Oracle Cloud documentation","https://docs.oracle.com/en-us/iaas/Content/home.htm","Official Oracle Cloud docs"),
 ("Oracle Cloud home","https://www.oracle.com/cloud/","Official Oracle Cloud page"),
],
'dsa': [
 ("Python TimeComplexity wiki","https://wiki.python.org/moin/TimeComplexity","Official Python wiki on algorithm complexity"),
 ("Big-O Cheat Sheet","https://www.bigocheatsheet.com/","Well-known complexity reference"),
 ("VisuAlgo","https://visualgo.net/en","Algorithm visualization reference"),
],
}

def slug_cats(slug):
    s = slug; cats = []
    if s.startswith('aws'): cats += ['aws']
    if s.startswith('az-') or s in ('azure-developer','m365','ms-fundamentals','sc-200','sc-300'): cats += ['azure']
    if s in ('cka','ckad','k8s-associate','openshift'): cats += ['k8s']
    if s == 'openshift': cats += ['redhat']
    if s == 'docker': cats += ['docker']
    if s == 'terraform': cats += ['terraform']
    if s == 'vault-consul': cats += ['vault']
    if s in ('python','dsa','datascience-ml','nvidia-ai','llm-engineering'): cats += ['python']
    if s == 'dsa': cats += ['dsa']
    if s == 'datascience-ml': cats += ['datalibs']
    if s in ('llm-engineering','ai-product','nvidia-ai'): cats += ['aidocs']
    if s in ('java','spring'): cats += ['java']
    if s in ('c-lang','cpp'): cats += ['cpp']
    if s == 'dotnet': cats += ['dotnet']
    if s in ('python-web','fullstack','react-frontend','creative-code'): cats += ['web']
    if s == 'creative-code': cats += ['creative']
    if s in ('sql','oracle-sql','dp-203','data-engineering','data-analyst','aws-data'): cats += ['data']
    if s in ('mongodb','aws-data'): cats += ['mongodb']
    if s in ('oracle-db','oracle-oci','oracle-sql'): cats += ['oracle']
    if s == 'oracle-oci': cats += ['cloud']
    if s in ('git-devops','ides-tooling'): cats += ['git']
    if s in ('git-devops','sre-platform','aws-soa','aws-dop'): cats += ['devops']
    if s in ('linux-essentials','rhcsa','rhce','systems-cs','sre-platform'): cats += ['linux']
    if s == 'systems-cs': cats += ['network']
    if s == 'linux-essentials': cats += ['lpi']
    if s in ('rhcsa','rhce'): cats += ['redhat']
    if s in ('comptia-core','comptia-infra'): cats += ['comptia','linux','network']
    if s == 'comptia-cyber': cats += ['comptia','security']
    if s in ('cissp','cism','pentest','soc-analyst','zerotrust','dod-8140','nice-framework','aws-scs','hackers-arise','nsa-codebreaker','sc-200','sc-300'): cats += ['security']
    if s == 'az-700': cats += ['network']
    if s == 'dod-8140': cats += ['cybermil']
    if s == 'nice-framework': cats += ['nice']
    if s == 'blockchain-dev': cats += ['blockchain']
    if s == 'career-launch': cats += ['career']
    if s == 'math-tech': cats += ['math']
    if s == 'hermetica': cats += ['hermetica']
    # dedupe preserving order
    seen = set(); out = []
    for c in cats:
        if c not in seen: seen.add(c); out.append(c)
    return out

# ------------------------------------------------------------- url checking --
def check_url(url):
    last = 'ERR'
    for _ in range(2):
        try:
            p = subprocess.run(
                ['curl','-sIL','--max-time','25','-o','/dev/null',
                 '-w','%{http_code}','-A',UA,url],
                capture_output=True, text=True, timeout=45)
            code = (p.stdout or '').strip().split()[0] if p.stdout.strip() else 'EMPTY'
            if code == '200':
                return True, code
            last = code
        except Exception:
            last = 'EXC'
    return False, last

def verify_all(urls):
    results = {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        for url, (ok, code) in zip(urls, ex.map(check_url, urls)):
            results[url] = (ok, code)
    return results

# ------------------------------------------------------------ text mining ----
STRIP_PREFIX = re.compile(r'^(Key|Note|Remember)\s*:\s*', re.I)
WARN_PREFIX = re.compile(r'^(Common trap|Pitfall|Watch out|Trap)\s*:\s*(.+)$', re.I | re.S)

def clean(s):
    return re.sub(r'\s+', ' ', s or '').strip()

def sentences_from(d):
    """(sentence, lesson_idx|None, domain_id) — deduped, min length."""
    pool = []
    for i, l in enumerate(d.get('lessons', [])):
        for c in l.get('concepts', []): pool.append((clean(c), i, l.get('domain_id')))
        for c in l.get('pitfalls', []): pool.append((clean(c), i, l.get('domain_id')))
        ex = l.get('example') or {}
        if ex.get('walkthrough'): pool.append((clean(ex['walkthrough']), i, l.get('domain_id')))
    for dm in d.get('domains', []):
        for sc in dm.get('scenarios', []):
            if sc.get('why'): pool.append((clean(sc['why']), None, dm.get('id')))
            if sc.get('hint'): pool.append((clean(sc['hint']), None, dm.get('id')))
    seen = set(); out = []
    for s, i, dd in pool:
        k = s.lower()
        if len(s) >= 25 and k not in seen:
            seen.add(k); out.append((s, i, dd))
    return out

def to_item(s):
    """'term — definition' mined from one of the bootcamp's own sentences."""
    s = clean(s)
    mw = WARN_PREFIX.match(s)
    if mw:
        # NEVER strip a trap warning into a recommendation — keep the warning label.
        rest = clean(mw.group(2))
        if len(rest) > 260: rest = rest[:257].rstrip() + '…'
        return 'Common trap — ' + rest
    s = STRIP_PREFIX.sub('', s).strip()
    term = dfn = None
    m = re.match(r'^(.{3,70}?)\s*:\s*(.{10,})$', s)
    if m:
        term, dfn = m.group(1).strip(), m.group(2).strip()
    else:
        parts = re.split(r'\s+[—–]\s+', s, maxsplit=1)
        if len(parts) == 2 and 2 < len(parts[0]) < 70:
            term, dfn = parts[0].strip(), parts[1].strip()
        else:
            m2 = re.match(
                r'^([A-Z][\w .,&/()+\'-]{1,55}?)\s+'
                r'(is|are|means|mean|refers to|provides|provide|enables|enable|'
                r'requires|require|uses|use|supports|support|defines|define|'
                r'creates|create|manages|manage|controls|control)\b[,\s]*(.{10,})$', s)
            if m2:
                term = m2.group(1).strip()
                dfn = (m2.group(2) + ' ' + m2.group(3)).strip()
            else:
                m3 = re.match(r'^[`"\']?([A-Z][\w.+-]*(?:\s+[A-Z][\w.+-]*){0,2}|[A-Z]{2,7}|`[^`]+`)', s)
                if m3:
                    term = m3.group(1).strip('`').strip()
                    dfn = s
                else:
                    m4 = re.match(r'^([a-z][a-z0-9\s,\'-]{2,40}?)(?=[\s,.]|$)', s)
                    if m4:
                        term = m4.group(1).strip().capitalize()
                        dfn = s
                    else:
                        term, dfn = 'Key point', s
    if len(dfn) > 260: dfn = dfn[:257].rstrip() + '…'
    if len(term) > 70: term = term[:67].rstrip() + '…'
    return term + ' — ' + dfn

def clean_title(t):
    t = clean(t)
    if 'concept' in t.lower():
        t = re.split(r'\s+[—–-]\s+', t)[0]
    return t

def build_cheatsheet(d, pool):
    lessons = d.get('lessons', [])
    why_pool = [s for (s, i, dd) in pool if i is None]
    sections = []
    wi = [0]
    def take(n):
        out = []
        while len(out) < n and wi[0] < len(why_pool):
            out.append(why_pool[wi[0]]); wi[0] += 1
        return out
    groups = []
    if len(lessons) <= 6:
        groups = [[l] for l in lessons]
    else:
        groups = [[l] for l in lessons[:5]] + [lessons[5:]]
    for g in groups:
        heading = clean_title(g[0]['title']) if len(g) == 1 else 'More core topics'
        items = []
        for l in g:
            li = lessons.index(l)
            for (s, i, dd) in pool:
                if i != li: continue
                if not re.match(r'^[A-Z0-9`"\'(]', clean(s)): continue  # drop fragments
                items.append(to_item(s))
        while len(items) < 4:
            extra = [s for s in take(4 - len(items)) if re.match(r'^[A-Z0-9`"\'(]', clean(s))]
            if not extra: break
            items += [to_item(s) for s in extra]
        items = items[:10]
        if len(items) >= 3:
            sections.append({'heading': heading, 'items': items})
    sections = sections[:6]
    return {'title': d.get('title', '') + ' — Cheat Sheet', 'sections': sections}

# --------------------------------------------------------------- glossary ----
CAP = re.compile(r'\b([A-Z][A-Za-z0-9+.#/-]*(?:\s+[A-Z][A-Za-z0-9+.#/-]*){0,2})\b')
ACR = re.compile(r'(?<![\w-])([A-Z]{2,7})\b')
BT = re.compile(r'`([^`]{2,60})`')
STOPW = {'The','This','This','That','These','Those','When','Where','Which','While','With','From',
 'Your','Their','There','Here','Each','Every','Both','Most','Many','Some','Such','What','Always',
 'Never','Before','After','During','Under','Over','Common','Key','Note','Remember','First','Second',
 'Third','Next','Then','Also','Well','Even','Just','Only','Like','Using','Based','Make','Take','Give',
 'Keep','Check','For','And','But','Its','It','They','Them','You','We','One','Two','All','Any','New',
 'Old','Good','Bad','True','False','Yes','No','Try','See','Let',
 # uppercase common words that slip through the acronym matcher
 'IS','IT','AS','AT','BE','DO','IF','IN','OF','ON','OR','TO','UP','AN','AM','BY','SO','US','MY',
 'HE','ME','WHETHER','READ','WHICH','WHEN','WHERE','WHILE','WITH','FROM','YOUR','THEIR','THERE',
 'WHETHER','READ'}
# title-case common words that slip through the capitalized-phrase matcher
STOPW |= {'Whether', 'Read'}
CMDW = {'kubectl','docker','git','aws','az','terraform','pip','npm','python','python3','systemctl',
 'chmod','chown','ssh','openssl','nmap','sqlcmd','psql','mongosh','mongo','vault','consul','curl',
 'grep','sed','awk','helm','ansible','jq','gcc','java','javac','node','dotnet','gcloud','oci'}

def build_glossary(d, pool):
    freq = {}; casing = {}; hits = {}
    nsent = len(pool)
    for (s, i, dd) in pool:
        cands = set()
        for m in BT.finditer(s):
            t = m.group(1).strip()
            if t: cands.add((t, 'bt'))
        for m in ACR.finditer(s):
            t = m.group(1)
            if t not in STOPW: cands.add((t, 'acr'))
        for m in CAP.finditer(s):
            t = m.group(1).strip()
            words = t.split()
            if not words or words[0] in STOPW: continue
            if len(t) < 3: continue
            if all(w in STOPW for w in words): continue
            cands.add((t, 'cap'))
        for w in CMDW:
            if re.search(r'\b' + re.escape(w) + r'\b', s):
                cands.add((w, 'cmd'))
        for t, kind in cands:
            k = t.lower()
            freq[k] = freq.get(k, 0) + 1
            if len(t) > len(casing.get(k, '')): casing[k] = t
            hits.setdefault(k, []).append((s, kind))
    def score(t, s, kind):
        pat = r'\b' + re.escape(t) + r'\b'
        sc = 0
        if kind == 'bt' or re.search(pat + r'\s*:', s): sc += 3
        if re.search(pat + r'.{0,50}?\b(is|are|means?|refers to|stands for|provides?|enables?|requires?|uses?|supports?|defines?)\b', s, re.I): sc += 3
        if s.lower().find(t.lower()) <= 40: sc += 1
        return sc
    # term qualifies only if some sentence actually defines/presents it
    qualified = []
    for k, f in freq.items():
        if len(k) <= 1 or k == 'key point': continue
        if f > max(3, nsent * 0.6): continue  # ultra-generic
        kind0 = hits[k][0][1]
        best = max(((score(casing[k], s, kd), s) for s, kd in hits[k]), key=lambda x: x[0])
        sc, s = best
        multi = (' ' in k) or ('-' in k)
        need = 1 if (multi or kind0 in ('acr', 'cmd', 'bt')) else 3
        if sc >= need:
            qualified.append((f, sc, k, s))
    qualified.sort(key=lambda x: (-x[0], -x[1], len(x[2])))
    glossary = []
    for f, sc, k, s in qualified[:25]:
        s = STRIP_PREFIX.sub('', s).strip()
        parts = re.split(r'(?<=[.!?])\s+', s)
        dfn = ' '.join(parts[:2]).strip()
        if len(dfn) < 30: continue
        if len(dfn) > 240: dfn = dfn[:237].rstrip() + '…'
        if dfn.lower().rstrip('.') == k: continue
        glossary.append({'term': casing[k], 'def': dfn})
    # fallback: recycle cheatsheet term/def pairs (accurate by construction)
    if len(glossary) < 12:
        seen_terms = {g['term'].lower() for g in glossary}
        for (s, i, dd) in pool:
            if len(glossary) >= 14: break
            it = to_item(s)
            if ' — ' not in it: continue
            term, dfn = it.split(' — ', 1)
            if term.lower() in seen_terms or term.lower().startswith('common trap'): continue
            if len(dfn) < 30: continue
            seen_terms.add(term.lower())
            glossary.append({'term': term, 'def': dfn})
    return glossary[:25]

# ------------------------------------------------------------------ links ----
def build_links(d, verified):
    links = []; seen = set()
    def add(label, url, note):
        if url in seen: return
        ok, code = verified.get(url, (False, 'UNCHECKED'))
        if ok:
            links.append({'label': label, 'url': url, 'note': note})
            seen.add(url)
    v = d.get('vendor') or {}
    vdocs = (v.get('docs') or '').strip()
    if vdocs:
        add(v.get('name', 'Vendor') + ' — official site', vdocs,
            'Official vendor documentation and certification information')
    for cat in slug_cats(d.get('slug', '')):
        for label, url, note in CATS.get(cat, []):
            if len(links) >= 8: break
            add(label, url, note)
        if len(links) >= 8: break
    return links

# --------------------------------------------------------------- checklist ---
MODE = {'career-launch':'interview','math-tech':'study','hermetica':'study',
        'creative-code':'study','nsa-codebreaker':'challenge','hackers-arise':'challenge',
        'ai-product':'project','blockchain-dev':'project'}

GENERIC = {
'exam': [
 "Get 7–8 hours of sleep the night before — fatigue destroys recall faster than any topic gap.",
 "Bring valid government-issued photo ID and arrive at the test center 30 minutes early.",
 "Eat a real meal beforehand; bring water and a light snack if the center allows them.",
 "Read every question twice before scanning the answer choices.",
 "Flag uncertain questions and move on — return with fresh eyes at the end.",
 "Eliminate the obviously wrong answers first, then compare the survivors.",
 "Budget your time: answer steadily and keep a 10–15 minute review buffer.",
 "Re-run your weakest-domain drill until mastery is at least 80%.",
],
'interview': [
 "Research the company: mission, recent news, and the interviewers' backgrounds.",
 "Prepare 3–5 STAR stories (Situation, Task, Action, Result) in 60–90 seconds each.",
 "Rehearse 'tell me about yourself' and 'why this role' out loud, not just in your head.",
 "Prepare 3 smart questions to ask the interviewer about the team and the work.",
 "Charge your devices; test camera, mic, and meeting link for virtual interviews.",
 "Lay out professional attire the night before; plan to arrive 15 minutes early.",
 "Bring printed copies of your tailored resume and a notepad.",
 "Know your market salary range and your walk-away number before you walk in.",
 "Send a thank-you email within 24 hours referencing something specific from the conversation.",
],
'study': [
 "Set a 90-minute focused block; silence notifications and close unrelated tabs.",
 "Warm up by re-reading yesterday's notes before starting new material.",
 "Work every example by hand or in the sandbox — never just read them.",
 "Write each key term and formula in your own words in a notebook.",
 "After each domain, close the material and recite the core ideas aloud.",
 "Redo the problems you missed until you can solve them cold.",
 "Take a 10-minute break every 50 minutes — spaced effort beats cramming.",
 "End the session by listing the three ideas you are least sure about, and drill those first next time.",
],
'challenge': [
 "Sleep 7–8 hours — puzzle speed collapses under fatigue.",
 "Set up your workspace: notes app, scratch paper, and the bootcamp terminal ready.",
 "Read each challenge prompt fully before touching the keyboard.",
 "Work methodically: enumerate possibilities before guessing.",
 "When stuck for 15 minutes, switch challenges and return with fresh eyes.",
 "Document every solved technique in your own words — it compounds.",
 "Time-box each challenge; bank the easy wins first.",
 "Re-run your weakest-domain drill until mastery is at least 80%.",
],
'project': [
 "Define 'done' for the session: one working feature or one fixed bug.",
 "Read the relevant docs section before writing code.",
 "Commit early and often with clear commit messages.",
 "Test each change in the sandbox before moving on.",
 "When stuck for 30 minutes, explain the problem aloud or re-read the walkthrough.",
 "Review the domain glossary terms you used today — can you define each one?",
 "End the session with a short note: what worked, and what is next.",
 "Re-run your weakest-domain drill until mastery is at least 80%.",
],
}

DOMAIN_SPECIFIC = {
'exam': [
 "For {d}: restate the 'why' behind each scenario answer in your own words — if you can't explain it, you don't own it.",
 "Redo one {d} lab from scratch without looking at the steps.",
 "Recite the key {d} terms from the glossary aloud from memory.",
],
'interview': [
 "Review your {d} notes: positioning, gaps, and your value story.",
 "Prepare one story that shows {d} strength with a measurable result.",
],
'study': [
 "Spend extra time on {d}: teach its core ideas back in plain language.",
 "Re-derive the key {d} results from scratch without peeking.",
],
'challenge': [
 "Replay the {d} challenges until your solve time drops.",
 "Write up your {d} solutions as if teaching a teammate.",
],
'project': [
 "Build one small thing that exercises {d} end to end.",
 "Refactor yesterday's {d} work using a glossary term you just learned.",
],
}

def build_checklist(d):
    mode = MODE.get(d.get('slug', ''), 'exam')
    items = list(GENERIC[mode])
    doms = [dm.get('name', '') for dm in d.get('domains', []) if dm.get('name')]
    tpl = DOMAIN_SPECIFIC[mode]
    for j, dm in enumerate(doms[:3]):
        if len(items) >= 12: break
        items.append(tpl[j % len(tpl)].format(d=dm))
    return items[:12]

# -------------------------------------------------------------------- main ----
def main():
    files = sorted(glob.glob(os.path.join(CONTENT, '*.json')))
    print('bootcamps found:', len(files), flush=True)

    # 1) collect every URL we might include, verify once
    urls = set()
    for f in files:
        d = json.load(open(f))
        v = (d.get('vendor') or {}).get('docs', '').strip()
        if v: urls.add(v)
        for cat in slug_cats(d.get('slug', '')):
            for _l, u, _n in CATS.get(cat, []):
                urls.add(u)
    urls = sorted(urls)
    print('unique urls to verify:', len(urls), flush=True)
    verified = verify_all(urls)

    log_lines = []
    for u in urls:
        ok, code = verified[u]
        log_lines.append('%s %s %s' % ('PASS' if ok else 'DROP', code, u))
    with open(LOG, 'w') as fh:
        fh.write('# link check %s — curl -sIL, HTTP 200 required\n' % __import__('datetime').datetime.now().isoformat())
        fh.write('\n'.join(log_lines) + '\n')
    npass = sum(1 for v in verified.values() if v[0])
    print('verified 200: %d / %d (see resources/link-check.log)' % (npass, len(urls)), flush=True)

    # 2) generate fragments
    report = []
    thin = []
    for f in files:
        slug = os.path.basename(f)[:-5]
        d = json.load(open(f))
        pool = sentences_from(d)
        cheatsheet = build_cheatsheet(d, pool)
        glossary = build_glossary(d, pool)
        links = build_links(d, verified)
        checklist = build_checklist(d)
        frag = {'resources': {'cheatsheet': cheatsheet, 'glossary': glossary,
                              'links': links, 'checklist': checklist}}
        fragdir = os.path.join(CONTENT, slug, 'fragments')
        os.makedirs(fragdir, exist_ok=True)
        out = os.path.join(fragdir, 'resources.json')
        with open(out, 'w') as fh:
            json.dump(frag, fh, indent=1, ensure_ascii=False)
            fh.write('\n')
        nsec = len(cheatsheet['sections'])
        nitems = sum(len(s['items']) for s in cheatsheet['sections'])
        report.append((slug, nsec, nitems, len(glossary), len(links), len(checklist)))
        reasons = []
        if nsec < 3: reasons.append('cheatsheet sections=%d' % nsec)
        if len(glossary) < 12: reasons.append('glossary=%d' % len(glossary))
        if len(links) < 4: reasons.append('links=%d' % len(links))
        if len(checklist) < 8: reasons.append('checklist=%d' % len(checklist))
        if reasons: thin.append((slug, '; '.join(reasons)))

    # 3) validate: every fragment parses and matches schema shape
    bad = []
    for f in files:
        slug = os.path.basename(f)[:-5]
        p = os.path.join(CONTENT, slug, 'fragments', 'resources.json')
        try:
            r = json.load(open(p))['resources']
            assert isinstance(r['cheatsheet']['sections'], list)
            assert all(isinstance(s['items'], list) and s['items'] for s in r['cheatsheet']['sections'])
            assert isinstance(r['glossary'], list) and all('term' in g and 'def' in g for g in r['glossary'])
            assert isinstance(r['links'], list) and all('label' in x and 'url' in x for x in r['links'])
            assert isinstance(r['checklist'], list) and all(isinstance(x, str) for x in r['checklist'])
        except Exception as e:
            bad.append((slug, str(e)))

    print('\n%-22s %4s %5s %4s %5s %5s' % ('slug', 'secs', 'items', 'glos', 'links', 'check'))
    for slug, nsec, nitems, ng, nl, nc in report:
        print('%-22s %4d %5d %4d %5d %5d' % (slug, nsec, nitems, ng, nl, nc))
    print('\nTHIN PACKS (%d):' % len(thin))
    for slug, why in thin: print(' -', slug, ':', why)
    print('VALIDATION FAILURES (%d):' % len(bad))
    for slug, why in bad: print(' -', slug, ':', why)
    # confirm 100% of included URLs were 200 at generation time
    inc = set()
    for f in files:
        slug = os.path.basename(f)[:-5]
        r = json.load(open(os.path.join(CONTENT, slug, 'fragments', 'resources.json')))['resources']
        for x in r['links']: inc.add(x['url'])
    notok = [u for u in inc if not verified.get(u, (False,))[0]]
    print('included urls: %d, all verified-200: %s' % (len(inc), 'YES' if not notok else 'NO -> %s' % notok))

if __name__ == '__main__':
    main()
