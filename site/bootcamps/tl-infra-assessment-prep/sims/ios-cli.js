/* ============================================================================
 * ios-cli.js — shared IOS-style CLI engine for hands-on network simulations.
 * Vanilla JavaScript. Zero dependencies. Runs in browsers and in Node.js.
 *
 *   const sw = new IOSDevice({ hostname: 'SW1', type: 'switch',
 *                              interfaces: ['fa0/1','fa0/2','fa0/24'] });
 *   sw.exec('enable');
 *   sw.exec('configure terminal');
 *   sw.exec('vlan 10');
 *   sw.getState();   // JSON snapshot for topology renderers / graders
 *
 * Modes: user (>) , privileged (#), config, config-if, config-vlan,
 *        config-dhcp, config-isakmp, config-crypto-map, config-ipsec-profile.
 * PC devices ('pc') get a tiny end-host CLI: ping, ipconfig.
 * ========================================================================== */
(function (root) {
'use strict';

/* ------------------------------ regex helpers --------------------------- */
function A(word, minLen) {           // abbreviation-tolerant keyword fragment
  minLen = minLen || 1;
  var parts = [];
  for (var i = minLen; i <= word.length; i++) parts.push(word.slice(0, i));
  return '(?:' + parts.join('|') + ')';
}
function P() {                        // full-command pattern from fragments
  return new RegExp('^' + Array.prototype.join.call(arguments, '\\s+') + '$', 'i');
}
var IP  = '(\\d{1,3}(?:\\.\\d{1,3}){3})';
var NUM = '(\\d+)';
var WORD = '(\\S+)';
var REST = '(.+)';
var IFR = '([A-Za-z]+\\s*\\d[\\d/.]*)';   // raw interface token: fa0/1, Gi0/0.10
var VLANLIST = '([\\d,\\-]+)';

function prefixRes(re) {              // proper-prefix patterns (for % Incomplete)
  var parts = re.source.split(/\\s\+/);
  var out = [];
  for (var i = 1; i < parts.length; i++) {
    var body = parts.slice(0, i).join('\\s+').replace(/^\^/, '').replace(/\$$/, '');
    out.push(new RegExp('^' + body + '$', 'i'));
  }
  return out;
}

/* --------------------------- interface name utils ------------------------ */
function canonIface(raw) {
  var s = String(raw).toLowerCase().replace(/\s+/g, '');
  var m;
  if ((m = s.match(/^(fa|fastethernet)(\d+\/\d+(?:\.\d+)?)$/))) return 'fa' + m[2];
  if ((m = s.match(/^(gi|gigabitethernet)(\d+\/\d+(?:\.\d+)?)$/))) return 'gi' + m[2];
  if ((m = s.match(/^(eth|ethernet)(\d+\/\d+(?:\.\d+)?)$/))) return 'eth' + m[2];
  if ((m = s.match(/^(s|serial)(\d+\/\d+\/\d+)$/))) return 's' + m[2];
  if ((m = s.match(/^vlan(\d+)$/))) return 'vlan' + m[1];
  if ((m = s.match(/^(lo|loopback)(\d+)$/))) return 'lo' + m[1];
  if ((m = s.match(/^(tu|tunnel)(\d+)$/))) return 'tu' + m[1];
  return null;
}
function displayIface(c) {
  var m;
  if ((m = c.match(/^fa(.+)$/))) return 'Fa' + m[1];
  if ((m = c.match(/^gi(.+)$/))) return 'Gi' + m[1];
  if ((m = c.match(/^eth(.+)$/))) return 'Eth' + m[1];
  if ((m = c.match(/^s(.+)$/))) return 'Serial' + m[1];
  if ((m = c.match(/^vlan(\d+)$/))) return 'Vlan' + m[1];
  if ((m = c.match(/^lo(\d+)$/))) return 'Loopback' + m[1];
  if ((m = c.match(/^tu(\d+)$/))) return 'Tunnel' + m[1];
  return c;
}
function fullIface(c) {
  var m;
  if ((m = c.match(/^fa(.+)$/))) return 'FastEthernet' + m[1];
  if ((m = c.match(/^gi(.+)$/))) return 'GigabitEthernet' + m[1];
  if ((m = c.match(/^eth(.+)$/))) return 'Ethernet' + m[1];
  if ((m = c.match(/^s(.+)$/))) return 'Serial' + m[1];
  if ((m = c.match(/^vlan(\d+)$/))) return 'Vlan' + m[1];
  if ((m = c.match(/^lo(\d+)$/))) return 'Loopback' + m[1];
  if ((m = c.match(/^tu(\d+)$/))) return 'Tunnel' + m[1];
  return c;
}

/* -------------------------------- IP utils ------------------------------- */
function ipToInt(ip) {
  var p = String(ip).split('.').map(Number);
  return (((p[0] * 256 + p[1]) * 256 + p[2]) * 256 + p[3]) >>> 0;
}
function intToIp(n) {
  n = n >>> 0;
  return [ (n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255 ].join('.');
}
function maskToPrefix(mask) {
  var x = ipToInt(mask), p = 0;
  while (x) { p += x & 1; x >>>= 1; }
  return p;
}
function networkOf(ip, mask) { return intToIp(ipToInt(ip) & ipToInt(mask)); }
function inSubnet(ip, net, mask) {
  return networkOf(ip, mask) === networkOf(net, mask);
}
function validIp(ip) {
  var p = String(ip).split('.');
  return p.length === 4 && p.every(function (o) { return /^\d{1,3}$/.test(o) && +o <= 255; });
}
function pad(s, n) { s = String(s); while (s.length < n) s += ' '; return s; }
function parseVlanList(s) {
  var out = [];
  String(s).split(',').forEach(function (p) {
    var m = p.match(/^(\d+)-(\d+)$/);
    if (m) { for (var i = +m[1]; i <= +m[2]; i++) out.push(i); }
    else if (/^\d+$/.test(p)) out.push(+p);
  });
  return out;
}
function compressVlanList(a) {
  a = a.slice().sort(function (x, y) { return x - y; });
  if (!a.length) return 'none';
  var out = [], s = a[0], p = a[0];
  for (var i = 1; i <= a.length; i++) {
    if (a[i] === p + 1) { p = a[i]; continue; }
    out.push(s === p ? '' + s : s + '-' + p); s = a[i]; p = a[i];
  }
  return out.join(',');
}
function badToken(input, tokIdx) {   // % Invalid input detected, caret at token
  var toks = input.split(' '), pos = 0;
  for (var i = 0; i < tokIdx && i < toks.length; i++) pos += toks[i].length + 1;
  return new Array(pos + 1).join(' ') + '^\n% Invalid input detected at \'^\' marker.';
}

/* ================================ IOSDevice ============================== */
function IOSDevice(opts) {
  opts = opts || {};
  this.type = opts.type || 'switch';                 // switch | router | pc
  this.hostname = opts.hostname ||
    (this.type === 'router' ? 'Router' : this.type === 'pc' ? 'PC' : 'Switch');
  this.modeStack = ['user'];
  this.vlans = { 1: { name: 'default' } };
  this.ifaces = {};
  var self = this;
  (opts.interfaces || []).forEach(function (n) {
    var c = canonIface(n);
    if (c) self.ifaces[c] = self._newIface(c);
  });
  this.routes = [];                                  // {net,mask,nh}
  this.dhcpPools = {};                               // name -> {network,mask,routers[],dns[]}
  this.dhcpExcluded = [];
  this.dhcpBindings = [];                            // {ip,client}
  this.natRules = [];                                // {acl,iface,overload}
  this.natTranslations = [];                         // {pro,insideGlobal,insideLocal,outsideLocal,outsideGlobal}
  this.acls = {};                                    // num -> [{net,wc}|{proto,src,srcWc,dst,dstWc}]
  this.isakmp = {};                                  // policy -> {encryption,hash,auth,group,lifetime}
  this.tsets = {};                                   // name -> {transforms[]}
  this.ipsecProfiles = {};                           // name -> {ts}
  this.cmaps = {};                                   // name -> {seq,peer,ts,acl}
  this.vpn = { ike: 'down', ipsec: 'down', encaps: 0, decaps: 0,
               map: '', localAddr: '', localIdent: '', remoteIdent: '' };
  this.ipconfig = null;                              // PCs: {ip,mask,gateway,dns}
  this.pingResolver = null;                          // fn(ip) -> truthy ok
  this.ctx = {};                                     // {iface,vlan,pool,policy,cmap,profile}
}

IOSDevice.prototype._newIface = function (c) {
  var isSub = c.indexOf('.') >= 0, isVirt = /^(vlan|lo|tu)/.test(c);
  var shutdown = this.type === 'router' ? (!isSub && !isVirt) : false;
  return {
    shutdown: shutdown,
    mode: (this.type === 'switch' && !isVirt) ? 'access' : null,
    accessVlan: 1, nativeVlan: 1, trunkAllowed: null,
    ip: null, mask: null, encap: null,
    natInside: false, natOutside: false,
    desc: null, cryptoMap: null,
    tunSrc: null, tunDst: null, tunMode: null, tunProfile: null
  };
};

IOSDevice.prototype.mode = function () {
  return this.modeStack[this.modeStack.length - 1];
};

IOSDevice.prototype.prompt = function () {
  var h = this.hostname, m = this.mode();
  if (this.type === 'pc') return h + '>';
  switch (m) {
    case 'user': return h + '>';
    case 'enable': return h + '#';
    case 'config': return h + '(config)#';
    case 'config-if': return h + '(config-if)#';
    case 'config-vlan': return h + '(config-vlan)#';
    case 'config-dhcp': return h + '(config-dhcp)#';
    case 'config-isakmp': return h + '(config-isakmp)#';
    case 'config-cmap': return h + '(config-crypto-map)#';
    case 'config-profile': return h + '(config-ipsec-profile)#';
  }
  return h + '#';
};

IOSDevice.prototype.ifaceStatus = function (c) {
  var f = this.ifaces[c];
  if (!f) return { status: 'down', protocol: 'down' };
  if (f.shutdown) return { status: 'administratively down', protocol: 'down' };
  if (c.indexOf('.') >= 0 && !f.encap) return { status: 'up', protocol: 'down' };
  return { status: 'up', protocol: 'up' };
};

IOSDevice.prototype.exec = function (raw) {
  var input = String(raw == null ? '' : raw).replace(/,\s*/g, ',').trim().replace(/\s+/g, ' ');
  if (!input) return '';
  if (this.type === 'pc') return this._execPc(input);
  if (input === '?') return this._help();
  var dm = /^do\s+(.+)$/i.exec(input);               // "do show ..." in config modes
  if (dm && this.mode().indexOf('config') === 0) {
    var keep = this.modeStack.slice();
    this.modeStack = ['enable'];
    var out = this._dispatch(dm[1]);
    this.modeStack = keep;
    return out;
  }
  return this._dispatch(input);
};

IOSDevice.prototype._dispatch = function (input) {
  var mode = this.mode(), i, j, k, m;
  var cands = [];
  for (i = 0; i < CMDS.length; i++) if (CMDS[i].m.indexOf(mode) >= 0) cands.push(CMDS[i]);
  for (i = 0; i < cands.length; i++) {               // full match
    m = cands[i].re.exec(input);
    if (m) return cands[i].run(this, m, input);
  }
  for (i = 0; i < cands.length; i++) {               // incomplete
    var prefs = cands[i]._prefs || (cands[i]._prefs = prefixRes(cands[i].re));
    for (j = 0; j < prefs.length; j++) if (prefs[j].test(input)) return '% Incomplete command.';
  }
  return invalidCaret(input, cands);                 // invalid, with caret
};

function invalidCaret(input, cands) {
  var toks = input.split(' '), pos = 0, caret = input.length, i, j, k;
  for (i = 1; i <= toks.length; i++) {
    var part = toks.slice(0, i).join(' '), ok = false;
    for (j = 0; j < cands.length && !ok; j++) {
      if (cands[j].re.test(part)) { ok = true; break; }
      var prefs = cands[j]._prefs || (cands[j]._prefs = prefixRes(cands[j].re));
      for (k = 0; k < prefs.length; k++) if (prefs[k].test(part)) { ok = true; break; }
    }
    if (!ok) { caret = input.indexOf(toks[i - 1], pos); break; }
    pos = input.indexOf(toks[i - 1], pos) + toks[i - 1].length;
  }
  return new Array(caret + 1).join(' ') + '^\n% Invalid input detected at \'^\' marker.';
}

IOSDevice.prototype._help = function () {
  var mode = this.mode(), lines = [''], seen = {};
  CMDS.forEach(function (c) {
    if (c.m.indexOf(mode) < 0 || !c.h || seen[c.h]) return;
    seen[c.h] = 1; lines.push('  ' + c.h);
  });
  lines.push('');
  return lines.join('\n');
};

/* ------------------------------- PC mini-CLI ----------------------------- */
IOSDevice.prototype._execPc = function (input) {
  var m;
  if (input === '?') return '\n  ping <ip>      Send ICMP echo requests\n  ipconfig       Show IP configuration\n  exit           Close the terminal\n';
  if (/^exit$/i.test(input)) return '';
  if ((m = /^ping\s+(\d{1,3}(?:\.\d{1,3}){3})$/i.exec(input))) {
    var ok = this.pingResolver ? !!this.pingResolver(m[1]) : false;
    var s = '\nPinging ' + m[1] + ' with 32 bytes of data:\n';
    for (var i = 0; i < 4; i++) s += ok ? 'Reply from ' + m[1] + ': bytes=32 time<1ms TTL=128\n'
                                       : 'Request timed out.\n';
    s += ok ? '\nPing statistics for ' + m[1] + ':\n    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),\n'
            : '\nPing statistics for ' + m[1] + ':\n    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),\n';
    return s;
  }
  if (/^ipconfig$/i.test(input)) {
    if (!this.ipconfig || !this.ipconfig.ip)
      return '\nWindows IP Configuration\n\nEthernet adapter Local Area Connection:\n   Media State . . . . . . . . . . . : Media disconnected\n';
    var c = this.ipconfig;
    return '\nWindows IP Configuration\n\nEthernet adapter Local Area Connection:\n' +
      '   IPv4 Address. . . . . . . . . . . : ' + c.ip + '\n' +
      '   Subnet Mask . . . . . . . . . . . : ' + (c.mask || '') + '\n' +
      '   Default Gateway . . . . . . . . . : ' + (c.gateway || '') + '\n';
  }
  return '\n\'' + input.split(' ')[0] + '\' is not recognized as an internal or external command.\n';
};

/* ------------------------------ page helpers ----------------------------- */
IOSDevice.prototype.setIp = function (o) {           // PCs: assign address
  this.ipconfig = { ip: o.ip || null, mask: o.mask || null,
                    gateway: o.gateway || null, dns: o.dns || null };
};
IOSDevice.prototype.addDhcpBinding = function (b) { this.dhcpBindings.push(b); };
IOSDevice.prototype.addNatTranslation = function (t) { this.natTranslations.push(t); };
IOSDevice.prototype.setVpn = function (o) {
  for (var k in o) this.vpn[k] = o[k];
};

IOSDevice.prototype.getState = function () {
  var ifs = {}, self = this;
  Object.keys(this.ifaces).forEach(function (c) {
    var f = self.ifaces[c], sp = self.ifaceStatus(c);
    ifs[c] = { display: displayIface(c), mode: f.mode, accessVlan: f.accessVlan,
      nativeVlan: f.nativeVlan, trunkAllowed: f.trunkAllowed ? f.trunkAllowed.slice() : null,
      ip: f.ip, mask: f.mask, shutdown: f.shutdown, status: sp.status, protocol: sp.protocol,
      encap: f.encap, natInside: f.natInside, natOutside: f.natOutside, desc: f.desc,
      cryptoMap: f.cryptoMap, tunSrc: f.tunSrc, tunDst: f.tunDst,
      tunMode: f.tunMode, tunProfile: f.tunProfile };
  });
  return {
    hostname: this.hostname, type: this.type, mode: this.mode(),
    vlans: JSON.parse(JSON.stringify(this.vlans)),
    interfaces: ifs,
    routes: this.routes.slice(),
    dhcpPools: JSON.parse(JSON.stringify(this.dhcpPools)),
    dhcpExcluded: this.dhcpExcluded.slice(),
    dhcpBindings: this.dhcpBindings.slice(),
    natRules: this.natRules.slice(),
    natTranslations: this.natTranslations.slice(),
    acls: JSON.parse(JSON.stringify(this.acls)),
    isakmp: JSON.parse(JSON.stringify(this.isakmp)),
    transformSets: JSON.parse(JSON.stringify(this.tsets)),
    ipsecProfiles: JSON.parse(JSON.stringify(this.ipsecProfiles)),
    cryptoMaps: JSON.parse(JSON.stringify(this.cmaps)),
    vpn: JSON.parse(JSON.stringify(this.vpn)),
    ipconfig: this.ipconfig ? JSON.parse(JSON.stringify(this.ipconfig)) : null
  };
};

/* ============================ command registry =========================== */
/* m: modes that accept the command. run(dev, match, input) -> output string. */
var U  = ['user'];
var E2 = ['enable'];
var UE = ['user', 'enable'];
var C  = ['config'];
var CI = ['config-if'];
var CV = ['config-vlan'];
var CD = ['config-dhcp'];
var CK = ['config-isakmp'];
var CM = ['config-cmap'];
var CP = ['config-profile'];
var CX = ['config', 'config-if', 'config-vlan', 'config-dhcp',
          'config-isakmp', 'config-cmap', 'config-profile'];

function needRouter(dev, input, idx) {
  if (dev.type !== 'router') return badToken(input, idx == null ? 0 : idx);
  return null;
}
function needSwitch(dev, input) {
  if (dev.type !== 'switch') return badToken(input, 0);
  return null;
}
function curIf(dev, input) {
  var c = dev.ctx.iface, f = dev.ifaces[c];
  if (!f) return null;
  return { c: c, f: f };
}

var CMDS = [
/* ------------------------------- user EXEC ------------------------------ */
{ m: U, re: P(A('enable')), h: 'enable                  Enter privileged EXEC mode',
  run: function (dev) { dev.modeStack = ['enable']; return ''; } },
{ m: U, re: P(A('disable')), h: 'disable                 Leave privileged EXEC mode',
  run: function () { return ''; } },
{ m: U, re: P(A('exit')), h: 'exit                    Exit the CLI session',
  run: function () { return ''; } },

/* ---------------------------- privileged EXEC ---------------------------- */
{ m: E2, re: P(A('enable')), h: 'enable                  Enter privileged EXEC mode',
  run: function () { return ''; } },
{ m: E2, re: P(A('disable')), h: 'disable                 Return to user EXEC mode',
  run: function (dev) { dev.modeStack = ['user']; return ''; } },
{ m: E2, re: P(A('exit')), h: 'exit                    Leave privileged EXEC mode',
  run: function (dev) { dev.modeStack = ['user']; return ''; } },
{ m: E2, re: P(A('configure'), A('terminal')), h: 'configure terminal      Enter global configuration mode',
  run: function (dev) {
    dev.modeStack.push('config');
    return 'Enter configuration commands, one per line.  End with CNTL/Z.';
  } },
{ m: E2, re: P(A('write'), A('memory')), h: 'write memory            Save running config to NVRAM',
  run: function () { return 'Building configuration...\n[OK]'; } },
{ m: E2, re: P(A('copy'), A('running-config'), A('startup-config')),
  h: 'copy running-config startup-config   Save running config',
  run: function () { return 'Destination filename [startup-config]?\nBuilding configuration...\n[OK]'; } },

/* --------------------------------- ping ---------------------------------- */
{ m: UE, re: P(A('ping'), IP), h: 'ping <ip>               Send ICMP echo requests',
  run: function (dev, m) {
    var ip = m[1], ok;
    if (dev.pingResolver) { try { ok = !!dev.pingResolver(ip); } catch (e) { ok = false; } }
    else {
      ok = false;
      var st = dev.getState();
      Object.keys(st.interfaces).forEach(function (c) {
        var f = st.interfaces[c];
        if (f.ip === ip) ok = true;
        else if (f.ip && f.mask && f.protocol === 'up' && inSubnet(ip, f.ip, f.mask)) ok = true;
      });
    }
    var s = 'Type escape sequence to abort.\nSending 5, 100-byte ICMP Echos to ' + ip + ', timeout is 2 seconds:\n';
    s += ok ? '!!!!!\nSuccess rate is 100 percent (5/5), round-trip min/avg/max = 1/1/4 ms'
            : '.....\nSuccess rate is 0 percent (0/5)';
    return s;
  } },

/* ------------------------------- show (L2) -------------------------------- */
{ m: UE, re: P(A('show'), A('vlan'), A('brief')), h: 'show vlan brief         VLAN database summary',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    return showVlanBrief(dev);
  } },
{ m: UE, re: P(A('show'), A('interfaces'), A('trunk')), h: 'show interfaces trunk   Trunking interfaces',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    return showInterfacesTrunk(dev);
  } },
{ m: UE, re: P(A('show'), A('interfaces'), A('status')), h: 'show interfaces status  Port status summary',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    return showInterfacesStatus(dev);
  } },
{ m: UE, re: P(A('show'), A('interfaces'), IFR), h: 'show interfaces <if>    Interface detail',
  run: function (dev, m, input) {
    var c = canonIface(m[1]);
    if (!c || !dev.ifaces[c]) return badToken(input, 2);
    return showOneInterface(dev, c);
  } },

/* ------------------------------- show (L3) -------------------------------- */
{ m: UE, re: P(A('show'), A('ip'), A('interface'), A('brief')), h: 'show ip interface brief  IP / line status summary',
  run: function (dev) { return showIpIntBrief(dev); } },
{ m: UE, re: P(A('show'), A('ip'), A('route')), h: 'show ip route           Routing table',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showIpRoute(dev);
  } },
{ m: UE, re: P(A('show'), A('running-config')), h: 'show running-config     Current configuration',
  run: function (dev) { return showRunning(dev); } },
{ m: UE, re: P(A('show'), A('ip'), A('dhcp'), A('binding')), h: 'show ip dhcp binding    DHCP leases',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showDhcpBinding(dev);
  } },
{ m: UE, re: P(A('show'), A('ip'), A('dhcp'), A('pool')), h: 'show ip dhcp pool       DHCP pool statistics',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showDhcpPool(dev);
  } },
{ m: UE, re: P(A('show'), A('ip'), A('nat'), A('translations')), h: 'show ip nat translations   Active NAT entries',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showNatTranslations(dev);
  } },
{ m: UE, re: P(A('show'), A('access-lists')), h: 'show access-lists       Access control lists',
  run: function (dev) { return showAcls(dev); } },
{ m: UE, re: P(A('show'), A('ip'), A('access-lists')), h: 'show ip access-lists    Access control lists',
  run: function (dev) { return showAcls(dev); } },
{ m: UE, re: P(A('show'), A('crypto'), A('isakmp'), A('sa')), h: 'show crypto isakmp sa   IKE security associations',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showCryptoIsakmpSa(dev);
  } },
{ m: UE, re: P(A('show'), A('crypto'), A('ipsec'), A('sa')), h: 'show crypto ipsec sa    IPsec security associations',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showCryptoIpsecSa(dev);
  } },
{ m: UE, re: P(A('show'), A('crypto'), A('map')), h: 'show crypto map         Crypto map configuration',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    return showCryptoMap(dev);
  } },

/* ------------------------- config-mode navigation ------------------------- */
{ m: CX, re: P(A('end')), h: 'end                     Return to privileged EXEC',
  run: function (dev) { dev.modeStack = ['enable']; dev.ctx = {}; return ''; } },
{ m: CX, re: P(A('exit')), h: 'exit                    Exit one configuration level',
  run: function (dev) { dev.modeStack.pop(); dev.ctx = {}; return ''; } },

/* ------------------------------ global config ----------------------------- */
{ m: C, re: P(A('hostname'), WORD), h: 'hostname <name>         Set the device hostname',
  run: function (dev, m) { dev.hostname = m[1]; return ''; } },
{ m: C, re: P(A('vlan'), NUM), h: 'vlan <id>               Create/select a VLAN',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    var id = +m[1];
    if (id < 1 || id > 4094) return '% Invalid VLAN ID.';
    if (!dev.vlans[id]) dev.vlans[id] = { name: 'VLAN' + ('0000' + id).slice(-4) };
    dev.ctx.vlan = id;
    dev.modeStack.push('config-vlan');
    return '';
  } },
{ m: C, re: P(A('interface'), IFR), h: 'interface <type><num>   Select an interface',
  run: function (dev, m, input) {
    var c = canonIface(m[1]);
    if (!c) return badToken(input, 1);
    var isSub = c.indexOf('.') >= 0, base = c.split('.')[0];
    if (isSub) {
      if (!dev.ifaces[base]) return '% Sub-interface ' + displayIface(c) +
        ' requires existing interface ' + displayIface(base) + '.';
      if (!dev.ifaces[c]) dev.ifaces[c] = dev._newIface(c);
    } else if (/^vlan\d+$/.test(c)) {
      var e1 = needSwitch(dev, input); if (e1) return e1;
      if (!dev.ifaces[c]) dev.ifaces[c] = dev._newIface(c);
    } else if (/^(lo|tu)\d+$/.test(c)) {
      var e2 = needRouter(dev, input, 1); if (e2) return e2;
      if (!dev.ifaces[c]) dev.ifaces[c] = dev._newIface(c);
    } else {
      if (!dev.ifaces[c]) return '% Invalid interface ' + m[1].trim() + '.';
    }
    dev.ctx.iface = c;
    dev.modeStack.push('config-if');
    return '';
  } },
{ m: C, re: P(A('ip'), A('route'), IP, IP, IP), h: 'ip route <net> <mask> <next-hop>   Static route',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    if (!validIp(m[1]) || !validIp(m[2]) || !validIp(m[3])) return '% Invalid IP address.';
    dev.routes.push({ net: m[1], mask: m[2], nh: m[3] });
    return '';
  } },
{ m: C, re: P(A('no'), A('ip'), A('route'), IP, IP, IP), h: 'no ip route ...         Remove a static route',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 2); if (e) return e;
    dev.routes = dev.routes.filter(function (r) {
      return !(r.net === m[1] && r.mask === m[2] && r.nh === m[3]);
    });
    return '';
  } },
{ m: C, re: P(A('ip'), A('dhcp'), A('pool'), WORD), h: 'ip dhcp pool <name>     Create a DHCP pool',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    if (!dev.dhcpPools[m[1]]) dev.dhcpPools[m[1]] = { network: null, mask: null, routers: [], dns: [] };
    dev.ctx.pool = m[1];
    dev.modeStack.push('config-dhcp');
    return '';
  } },
{ m: C, re: P(A('ip'), A('dhcp'), A('excluded-address'), IP, IP), h: 'ip dhcp excluded-address <low> <high>',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    dev.dhcpExcluded.push(m[1] + ' ' + m[2]);
    return '';
  } },
{ m: C, re: P(A('ip'), A('dhcp'), A('excluded-address'), IP), h: 'ip dhcp excluded-address <ip>',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    dev.dhcpExcluded.push(m[1]);
    return '';
  } },
{ m: C, re: P(A('access-list'), NUM, A('permit'), IP, IP), h: 'access-list <n> permit <net> <wildcard>   Standard ACL',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var n = m[1];
    if (!dev.acls[n]) dev.acls[n] = [];
    dev.acls[n].push({ net: m[2], wc: m[3] });
    return '';
  } },
{ m: C, re: P(A('access-list'), NUM, A('permit'), A('ip'), IP, IP, IP, IP),
  h: 'access-list <n> permit ip <src> <wc> <dst> <wc>   Extended ACL',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var n = m[1];
    if (!dev.acls[n]) dev.acls[n] = [];
    dev.acls[n].push({ proto: 'ip', src: m[2], srcWc: m[3], dst: m[4], dstWc: m[5] });
    return '';
  } },
{ m: C, re: P(A('no'), A('access-list'), NUM), h: 'no access-list <n>      Remove an ACL',
  run: function (dev, m) { delete dev.acls[m[1]]; return ''; } },
{ m: C, re: P(A('ip'), A('nat'), A('inside'), A('source'), A('list'), NUM, A('interface'), IFR, A('overload')),
  h: 'ip nat inside source list <acl> interface <if> overload   PAT rule',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var c = canonIface(m[2]);
    if (!c || !dev.ifaces[c]) return badToken(input, 7);
    dev.natRules.push({ acl: m[1], iface: c, overload: true });
    return '';
  } },
{ m: C, re: P(A('no'), A('ip'), A('nat'), A('inside'), A('source'), A('list'), NUM),
  h: 'no ip nat inside source list <acl>   Remove NAT rule',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 2); if (e) return e;
    dev.natRules = dev.natRules.filter(function (r) { return r.acl !== m[1]; });
    return '';
  } },
{ m: C, re: P(A('crypto'), A('isakmp'), A('policy'), NUM), h: 'crypto isakmp policy <n>   IKE Phase 1 policy',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    if (!dev.isakmp[m[1]]) dev.isakmp[m[1]] = { encryption: null, hash: null, auth: null, group: null, lifetime: '86400' };
    dev.ctx.policy = m[1];
    dev.modeStack.push('config-isakmp');
    return '';
  } },
{ m: C, re: P(A('crypto'), A('ipsec'), A('transform-set'), WORD, REST),
  h: 'crypto ipsec transform-set <name> <transforms>   Phase 2 proposal',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    dev.tsets[m[1]] = { transforms: m[2].trim().split(/\s+/) };
    return '';
  } },
{ m: C, re: P(A('crypto'), A('ipsec'), A('profile'), WORD), h: 'crypto ipsec profile <name>   IPsec profile',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    if (!dev.ipsecProfiles[m[1]]) dev.ipsecProfiles[m[1]] = { ts: null };
    dev.ctx.profile = m[1];
    dev.modeStack.push('config-profile');
    return '';
  } },
{ m: C, re: P(A('crypto'), A('map'), WORD, NUM, A('ipsec-isakmp')), h: 'crypto map <name> <seq> ipsec-isakmp   Crypto map entry',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    dev.cmaps[m[1]] = { seq: +m[2], peer: null, ts: null, acl: null };
    dev.ctx.cmap = m[1];
    dev.modeStack.push('config-cmap');
    return '';
  } },
{ m: C, re: P(A('no'), A('crypto'), A('map'), WORD), h: 'no crypto map <name>   Remove a crypto map',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 2); if (e) return e;
    delete dev.cmaps[m[1]];
    return '';
  } },

/* ---------------------------- interface config ---------------------------- */
{ m: CI, re: P(A('description'), REST), h: 'description <text>      Interface description',
  run: function (dev, m) { var x = curIf(dev); if (x) x.f.desc = m[1].trim(); return ''; } },
{ m: CI, re: P(A('switchport'), A('mode'), '(' + A('access') + '|' + A('trunk') + ')'),
  h: 'switchport mode access|trunk   L2 port mode',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    var x = curIf(dev); if (!x) return '';
    x.f.mode = /^a/i.test(m[1]) ? 'access' : 'trunk';
    return '';
  } },
{ m: CI, re: P(A('switchport'), A('access'), A('vlan'), NUM), h: 'switchport access vlan <id>   Access VLAN',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    var x = curIf(dev); if (!x) return '';
    x.f.accessVlan = +m[1];
    return '';
  } },
{ m: CI, re: P(A('switchport'), A('trunk'), A('allowed'), A('vlan'), VLANLIST),
  h: 'switchport trunk allowed vlan <ids>   Trunk VLAN filter',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    var x = curIf(dev); if (!x) return '';
    x.f.trunkAllowed = parseVlanList(m[1]);
    return '';
  } },
{ m: CI, re: P(A('switchport'), A('trunk'), A('native'), A('vlan'), NUM), h: 'switchport trunk native vlan <id>',
  run: function (dev, m, input) {
    var e = needSwitch(dev, input); if (e) return e;
    var x = curIf(dev); if (!x) return '';
    x.f.nativeVlan = +m[1];
    return '';
  } },
{ m: CI, re: P(A('ip'), A('address'), IP, IP), h: 'ip address <ip> <mask>   Layer-3 address',
  run: function (dev, m, input) {
    var x = curIf(dev); if (!x) return '';
    if (dev.type === 'switch' && !/^vlan/.test(x.c))
      return '% IP addresses may not be configured on L2 links.';
    if (!validIp(m[1]) || !validIp(m[2])) return '% Invalid IP address.';
    x.f.ip = m[1]; x.f.mask = m[2];
    return '';
  } },
{ m: CI, re: P(A('no'), A('ip'), A('address')), h: 'no ip address           Remove Layer-3 address',
  run: function (dev) { var x = curIf(dev); if (x) { x.f.ip = null; x.f.mask = null; } return ''; } },
{ m: CI, re: P(A('shutdown')), h: 'shutdown                Administratively disable',
  run: function (dev) { var x = curIf(dev); if (x) x.f.shutdown = true; return ''; } },
{ m: CI, re: P(A('no'), A('shutdown')), h: 'no shutdown             Enable the interface',
  run: function (dev) { var x = curIf(dev); if (x) x.f.shutdown = false; return ''; } },
{ m: CI, re: P(A('encapsulation'), A('dot1Q'), NUM), h: 'encapsulation dot1Q <id>   802.1Q sub-interface VLAN',
  run: function (dev, m, input) {
    var x = curIf(dev); if (!x) return '';
    if (dev.type !== 'router' || x.c.indexOf('.') < 0)
      return '% Encapsulation is only configurable on router sub-interfaces.';
    x.f.encap = +m[1];
    return '';
  } },
{ m: CI, re: P(A('ip'), A('nat'), A('inside')), h: 'ip nat inside           NAT inside interface',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) { x.f.natInside = true; x.f.natOutside = false; }
    return '';
  } },
{ m: CI, re: P(A('ip'), A('nat'), A('outside')), h: 'ip nat outside          NAT outside interface',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) { x.f.natOutside = true; x.f.natInside = false; }
    return '';
  } },
{ m: CI, re: P(A('no'), A('ip'), A('nat'), A('inside')), h: 'no ip nat inside        Remove NAT inside role',
  run: function (dev) { var x = curIf(dev); if (x) x.f.natInside = false; return ''; } },
{ m: CI, re: P(A('no'), A('ip'), A('nat'), A('outside')), h: 'no ip nat outside       Remove NAT outside role',
  run: function (dev) { var x = curIf(dev); if (x) x.f.natOutside = false; return ''; } },
{ m: CI, re: P(A('tunnel'), A('source'), WORD), h: 'tunnel source <if|ip>   Tunnel source',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) x.f.tunSrc = m[1];
    return '';
  } },
{ m: CI, re: P(A('tunnel'), A('destination'), IP), h: 'tunnel destination <ip>   Tunnel destination',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) x.f.tunDst = m[1];
    return '';
  } },
{ m: CI, re: P(A('tunnel'), A('mode'), A('ipsec'), A('ipv4')), h: 'tunnel mode ipsec ipv4   IPsec tunnel mode',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) x.f.tunMode = 'ipsec ipv4';
    return '';
  } },
{ m: CI, re: P(A('tunnel'), A('protection'), A('ipsec'), A('profile'), WORD),
  h: 'tunnel protection ipsec profile <name>',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    var x = curIf(dev); if (x) x.f.tunProfile = m[1];
    return '';
  } },
{ m: CI, re: P(A('crypto'), A('map'), WORD), h: 'crypto map <name>       Apply crypto map to interface',
  run: function (dev, m, input) {
    var e = needRouter(dev, input, 1); if (e) return e;
    if (!dev.cmaps[m[1]]) return '% Crypto map ' + m[1] + ' is not defined.';
    var x = curIf(dev); if (x) x.f.cryptoMap = m[1];
    return '';
  } },
{ m: CI, re: P(A('no'), A('crypto'), A('map')), h: 'no crypto map          Remove crypto map from interface',
  run: function (dev) { var x = curIf(dev); if (x) x.f.cryptoMap = null; return ''; } },

/* ------------------------------ VLAN config ------------------------------- */
{ m: CV, re: P(A('name'), WORD), h: 'name <name>             VLAN name',
  run: function (dev, m) {
    if (dev.ctx.vlan && dev.vlans[dev.ctx.vlan]) dev.vlans[dev.ctx.vlan].name = m[1];
    return '';
  } },

/* ---------------------------- DHCP pool config ---------------------------- */
{ m: CD, re: P(A('network'), IP, IP), h: 'network <net> <mask>    Pool address range',
  run: function (dev, m, input) {
    if (!validIp(m[1]) || !validIp(m[2])) return '% Invalid IP address.';
    var p = dev.dhcpPools[dev.ctx.pool]; if (!p) return '';
    p.network = m[1]; p.mask = m[2];
    return '';
  } },
{ m: CD, re: P(A('default-router'), REST), h: 'default-router <ip>     Default gateway for clients',
  run: function (dev, m) {
    var p = dev.dhcpPools[dev.ctx.pool]; if (!p) return '';
    var ips = m[1].trim().split(/\s+/).filter(validIp);
    if (!ips.length) return '% Invalid IP address.';
    p.routers = ips.slice(0, 2);
    return '';
  } },
{ m: CD, re: P(A('dns-server'), REST), h: 'dns-server <ip>         DNS server(s) for clients',
  run: function (dev, m) {
    var p = dev.dhcpPools[dev.ctx.pool]; if (!p) return '';
    var ips = m[1].trim().split(/\s+/).filter(validIp);
    if (!ips.length) return '% Invalid IP address.';
    p.dns = ips.slice(0, 2);
    return '';
  } },
{ m: CD, re: P(A('domain-name'), WORD), h: 'domain-name <name>      Domain name for clients',
  run: function (dev, m) {
    var p = dev.dhcpPools[dev.ctx.pool]; if (p) p.domain = m[1];
    return '';
  } },

/* --------------------------- ISAKMP policy config -------------------------- */
{ m: CK, re: P(A('encryption'), '(aes|3des|des)'), h: 'encryption aes|3des|des   IKE encryption',
  run: function (dev, m) {
    var p = dev.isakmp[dev.ctx.policy]; if (p) p.encryption = m[1];
    return '';
  } },
{ m: CK, re: P(A('hash'), '(sha|md5)'), h: 'hash sha|md5             IKE integrity hash',
  run: function (dev, m) {
    var p = dev.isakmp[dev.ctx.policy]; if (p) p.hash = m[1];
    return '';
  } },
{ m: CK, re: P(A('authentication'), A('pre-share')), h: 'authentication pre-share   IKE authentication',
  run: function (dev, m) {
    var p = dev.isakmp[dev.ctx.policy]; if (p) p.auth = 'pre-share';
    return '';
  } },
{ m: CK, re: P(A('group'), NUM), h: 'group <n>               Diffie-Hellman group',
  run: function (dev, m) {
    var p = dev.isakmp[dev.ctx.policy]; if (p) p.group = m[1];
    return '';
  } },
{ m: CK, re: P(A('lifetime'), NUM), h: 'lifetime <secs>         IKE SA lifetime',
  run: function (dev, m) {
    var p = dev.isakmp[dev.ctx.policy]; if (p) p.lifetime = m[1];
    return '';
  } },

/* ---------------------------- crypto map config ---------------------------- */
{ m: CM, re: P(A('set'), A('peer'), IP), h: 'set peer <ip>           IPsec peer address',
  run: function (dev, m) {
    var cm = dev.cmaps[dev.ctx.cmap]; if (cm) cm.peer = m[1];
    return '';
  } },
{ m: CM, re: P(A('set'), A('transform-set'), WORD), h: 'set transform-set <name>   Phase 2 proposal',
  run: function (dev, m) {
    var cm = dev.cmaps[dev.ctx.cmap]; if (cm) cm.ts = m[1];
    return '';
  } },
{ m: CM, re: P(A('match'), A('address'), NUM), h: 'match address <acl>     Interesting-traffic ACL',
  run: function (dev, m) {
    var cm = dev.cmaps[dev.ctx.cmap]; if (cm) cm.acl = m[1];
    return '';
  } },

/* --------------------------- IPsec profile config -------------------------- */
{ m: CP, re: P(A('set'), A('transform-set'), WORD), h: 'set transform-set <name>   Phase 2 proposal',
  run: function (dev, m) {
    var pr = dev.ipsecProfiles[dev.ctx.profile]; if (pr) pr.ts = m[1];
    return '';
  } }
];

/* ============================ show renderers ============================= */
function showVlanBrief(dev) {
  var st = dev.getState(), L = [];
  L.push('VLAN Name                             Status    Ports');
  L.push('---- -------------------------------- --------- -------------------------------');
  Object.keys(st.vlans).map(Number).sort(function (a, b) { return a - b; }).forEach(function (id) {
    var ports = [];
    Object.keys(st.interfaces).forEach(function (c) {
      var f = st.interfaces[c];
      if (/^(vlan|lo|tu)/.test(c)) return;
      if (f.mode === 'access' && f.accessVlan === id) ports.push(f.display);
      else if (f.mode === 'trunk' && f.nativeVlan === id) ports.push(f.display);
    });
    L.push(pad(id, 4) + ' ' + pad(st.vlans[id].name, 32) + ' ' + pad('active', 9) + ' ' + ports.join(', '));
  });
  return L.join('\n');
}

function showInterfacesTrunk(dev) {
  var st = dev.getState(), L = [], trunks = [];
  Object.keys(st.interfaces).forEach(function (c) {
    if (st.interfaces[c].mode === 'trunk') trunks.push({ c: c, f: st.interfaces[c] });
  });
  L.push('Port        Mode             Encapsulation  Status        Native vlan');
  trunks.forEach(function (t) {
    L.push(pad(t.f.display, 12) + pad('on', 17) + pad('802.1q', 15) +
           pad(t.f.shutdown ? 'down' : 'trunking', 14) + t.f.nativeVlan);
  });
  L.push('', 'Port        Vlans allowed on trunk');
  trunks.forEach(function (t) {
    L.push(pad(t.f.display, 12) + (t.f.trunkAllowed ? compressVlanList(t.f.trunkAllowed) : '1-4094'));
  });
  L.push('', 'Port        Vlans allowed and active in management domain');
  trunks.forEach(function (t) {
    var allowed = t.f.trunkAllowed || Object.keys(st.vlans).map(Number);
    var active = allowed.filter(function (v) { return st.vlans[v]; });
    L.push(pad(t.f.display, 12) + compressVlanList(active));
  });
  L.push('', 'Port        Vlans in spanning tree forwarding state and not pruned');
  trunks.forEach(function (t) {
    var allowed2 = t.f.trunkAllowed || Object.keys(st.vlans).map(Number);
    var active2 = allowed2.filter(function (v) { return st.vlans[v]; });
    L.push(pad(t.f.display, 12) + compressVlanList(active2));
  });
  return L.join('\n');
}

function showInterfacesStatus(dev) {
  var st = dev.getState(), L = [];
  L.push('Port      Name               Status       Vlan       Duplex  Speed Type');
  Object.keys(st.interfaces).forEach(function (c) {
    if (/^(vlan|lo|tu)/.test(c) || c.indexOf('.') >= 0) return;
    var f = st.interfaces[c];
    var vlan = f.mode === 'trunk' ? 'trunk' : (f.mode === 'access' ? f.accessVlan : 'routed');
    L.push(pad(f.display, 10) + pad('', 19) + pad(f.shutdown ? 'disabled' : 'connected', 13) +
           pad(vlan, 11) + pad('a-full', 8) + pad('a-1000', 6) + '10/100/1000BaseTX');
  });
  return L.join('\n');
}

function showOneInterface(dev, c) {
  var st = dev.getState(), f = st.interfaces[c], raw = dev.ifaces[c];
  var L = [];
  L.push(fullIface(c) + ' is ' + f.status + ', line protocol is ' + f.protocol);
  L.push('  Hardware is ' + (dev.type === 'switch' ? 'Fast Ethernet' : 'Gigabit Ethernet') +
         ', address is aabb.cc00.0100');
  if (raw.desc) L.push('  Description: ' + raw.desc);
  if (f.ip) L.push('  Internet address is ' + f.ip + '/' + maskToPrefix(f.mask));
  if (f.encap) L.push('  Encapsulation 802.1Q Virtual LAN, Vlan ID ' + f.encap + '.');
  if (f.mode) L.push('  Switchport mode: ' + f.mode + (f.mode === 'access' ? ', access vlan ' + f.accessVlan : ''));
  L.push('  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec,');
  L.push('     reliability 255/255, txload 1/255, rxload 1/255');
  return L.join('\n');
}

function showIpIntBrief(dev) {
  var st = dev.getState(), L = [];
  L.push('Interface                  IP-Address      OK? Method Status                Protocol');
  Object.keys(st.interfaces).forEach(function (c) {
    var f = st.interfaces[c];
    L.push(pad(fullIface(c), 27) + pad(f.ip || 'unassigned', 16) + pad('YES', 4) +
           pad('manual', 7) + pad(f.status, 22) + f.protocol);
  });
  return L.join('\n');
}

function showIpRoute(dev) {
  var st = dev.getState(), L = [];
  L.push('Codes: C - connected, S - static, L - local');
  L.push('       * - candidate default');
  L.push('');
  L.push('Gateway of last resort is not set');
  L.push('');
  var rows = [];
  Object.keys(st.interfaces).forEach(function (c) {
    var f = st.interfaces[c];
    if (f.ip && f.mask && f.status === 'up' && f.protocol === 'up') {
      var net = networkOf(f.ip, f.mask), p = maskToPrefix(f.mask);
      rows.push({ net: net, p: p, line: 'C        ' + net + '/' + p + ' is directly connected, ' + fullIface(c) });
      rows.push({ net: f.ip, p: 32, line: 'L        ' + f.ip + '/32 is directly connected, ' + fullIface(c) });
    }
  });
  st.routes.forEach(function (r) {
    var p = maskToPrefix(r.mask);
    rows.push({ net: r.net, p: p, line: 'S        ' + r.net + '/' + p + ' [1/0] via ' + r.nh });
  });
  rows.sort(function (a, b) { return ipToInt(a.net) - ipToInt(b.net) || a.p - b.p; });
  if (!rows.length) L.push('% No routes installed.');
  rows.forEach(function (r) { L.push(r.line); });
  return L.join('\n');
}

function showRunning(dev) {
  var st = dev.getState(), L = [];
  L.push('Building configuration...', '');
  L.push('Current configuration : ' + JSON.stringify(st).length + ' bytes', '!', 'version 15.2', '!');
  L.push('hostname ' + st.hostname, '!');
  if (dev.type === 'switch') {
    Object.keys(st.vlans).map(Number).sort(function (a, b) { return a - b; }).forEach(function (id) {
      if (id === 1 && st.vlans[1].name === 'default') return;
      L.push('vlan ' + id, ' name ' + st.vlans[id].name, '!');
    });
  }
  Object.keys(st.interfaces).forEach(function (c) {
    var f = st.interfaces[c], raw = dev.ifaces[c];
    L.push('interface ' + fullIface(c));
    if (raw.desc) L.push(' description ' + raw.desc);
    if (dev.type === 'switch' && !/^vlan/.test(c)) {
      if (f.mode === 'trunk') {
        L.push(' switchport mode trunk');
        if (f.trunkAllowed) L.push(' switchport trunk allowed vlan ' + compressVlanList(f.trunkAllowed));
        if (f.nativeVlan !== 1) L.push(' switchport trunk native vlan ' + f.nativeVlan);
      } else if (f.mode === 'access' && f.accessVlan !== 1) {
        L.push(' switchport access vlan ' + f.accessVlan);
      }
    }
    if (f.encap) L.push(' encapsulation dot1Q ' + f.encap);
    if (f.ip) L.push(' ip address ' + f.ip + ' ' + f.mask);
    if (f.natInside) L.push(' ip nat inside');
    if (f.natOutside) L.push(' ip nat outside');
    if (f.cryptoMap) L.push(' crypto map ' + f.cryptoMap);
    if (f.tunSrc) L.push(' tunnel source ' + f.tunSrc);
    if (f.tunDst) L.push(' tunnel destination ' + f.tunDst);
    if (f.tunMode) L.push(' tunnel mode ' + f.tunMode);
    if (f.tunProfile) L.push(' tunnel protection ipsec profile ' + f.tunProfile);
    if (f.shutdown) L.push(' shutdown');
    L.push('!');
  });
  st.routes.forEach(function (r) { L.push('ip route ' + r.net + ' ' + r.mask + ' ' + r.nh); });
  if (st.routes.length) L.push('!');
  st.dhcpExcluded.forEach(function (x) { L.push('ip dhcp excluded-address ' + x); });
  if (st.dhcpExcluded.length) L.push('!');
  Object.keys(st.dhcpPools).forEach(function (n) {
    var p = st.dhcpPools[n];
    L.push('ip dhcp pool ' + n);
    if (p.network) L.push(' network ' + p.network + ' ' + p.mask);
    if (p.routers && p.routers.length) L.push(' default-router ' + p.routers.join(' '));
    if (p.dns && p.dns.length) L.push(' dns-server ' + p.dns.join(' '));
    L.push('!');
  });
  Object.keys(st.acls).forEach(function (n) {
    st.acls[n].forEach(function (e) {
      if (e.proto) L.push('access-list ' + n + ' permit ' + e.proto + ' ' + e.src + ' ' + e.srcWc + ' ' + e.dst + ' ' + e.dstWc);
      else L.push('access-list ' + n + ' permit ' + e.net + ' ' + e.wc);
    });
  });
  if (Object.keys(st.acls).length) L.push('!');
  st.natRules.forEach(function (r) {
    L.push('ip nat inside source list ' + r.acl + ' interface ' + fullIface(r.iface) + ' overload');
  });
  if (st.natRules.length) L.push('!');
  Object.keys(st.isakmp).forEach(function (n) {
    var p = st.isakmp[n];
    L.push('crypto isakmp policy ' + n);
    if (p.encryption) L.push(' encryption ' + p.encryption);
    if (p.hash) L.push(' hash ' + p.hash);
    if (p.auth) L.push(' authentication ' + p.auth);
    if (p.group) L.push(' group ' + p.group);
    if (p.lifetime) L.push(' lifetime ' + p.lifetime);
    L.push('!');
  });
  Object.keys(st.transformSets).forEach(function (n) {
    L.push('crypto ipsec transform-set ' + n + ' ' + st.transformSets[n].transforms.join(' '), '!');
  });
  Object.keys(st.ipsecProfiles).forEach(function (n) {
    L.push('crypto ipsec profile ' + n);
    if (st.ipsecProfiles[n].ts) L.push(' set transform-set ' + st.ipsecProfiles[n].ts);
    L.push('!');
  });
  Object.keys(st.cryptoMaps).forEach(function (n) {
    var cm = st.cryptoMaps[n];
    L.push('crypto map ' + n + ' ' + cm.seq + ' ipsec-isakmp');
    if (cm.peer) L.push(' set peer ' + cm.peer);
    if (cm.ts) L.push(' set transform-set ' + cm.ts);
    if (cm.acl) L.push(' match address ' + cm.acl);
    L.push('!');
  });
  L.push('end');
  return L.join('\n');
}

function showDhcpBinding(dev) {
  var L = ['Bindings from all pools not associated with VRF:',
           'IP address          Client-ID/            Lease expiration   Type',
           '                    Hardware address'];
  dev.dhcpBindings.forEach(function (b) {
    L.push(pad(b.ip, 20) + pad(b.client || '', 22) + pad('Infinite', 19) + 'Automatic');
  });
  if (!dev.dhcpBindings.length) L.push('(no bindings)');
  return L.join('\n');
}

function showDhcpPool(dev) {
  var st = dev.getState(), L = [];
  Object.keys(st.dhcpPools).forEach(function (n) {
    var p = st.dhcpPools[n];
    L.push('Pool ' + n + ' :');
    L.push(' Utilization mark (high/low)    : 100 / 0');
    L.push(' Subnet size (first/next)       : 0 / 0');
    L.push(' Total addresses                : ' + (p.mask ? Math.pow(2, 32 - maskToPrefix(p.mask)) - 2 : 0));
    L.push(' Leased addresses               : ' + st.dhcpBindings.length);
    L.push(' Excluded addresses             : ' + st.dhcpExcluded.length);
    L.push(' Pending event                  : none');
    L.push('');
  });
  if (!Object.keys(st.dhcpPools).length) L.push('% No DHCP pools configured.');
  return L.join('\n');
}

function showNatTranslations(dev) {
  var L = ['Pro Inside global         Inside local          Outside local         Outside global'];
  dev.natTranslations.forEach(function (t) {
    L.push(pad(t.pro || 'tcp', 4) + pad(t.insideGlobal, 22) + pad(t.insideLocal, 22) +
           pad(t.outsideLocal || '', 22) + (t.outsideGlobal || ''));
  });
  return L.join('\n');
}

function showAcls(dev) {
  var st = dev.getState(), L = [], n = 0;
  Object.keys(st.acls).forEach(function (num) {
    var ext = st.acls[num].some(function (e) { return e.proto; });
    L.push((ext ? 'Extended' : 'Standard') + ' IP access list ' + num);
    st.acls[num].forEach(function (e, i) {
      if (e.proto) L.push('    ' + ((i + 1) * 10) + ' permit ' + e.proto + ' ' + e.src + ' ' + e.srcWc + ' ' + e.dst + ' ' + e.dstWc);
      else L.push('    ' + ((i + 1) * 10) + ' permit ' + e.net + ', wildcard bits ' + e.wc);
    });
    n++;
  });
  if (!n) L.push('% No access lists configured.');
  return L.join('\n');
}

function showCryptoIsakmpSa(dev) {
  var st = dev.getState(), L = [];
  L.push('IPv4 Crypto ISAKMP SA');
  L.push(pad('dst', 18) + pad('src', 18) + pad('state', 15) + pad('conn-id', 10) + 'status');
  if (st.vpn.ike === 'up') {
    var peer = '', local = st.vpn.localAddr || '';
    Object.keys(st.cryptoMaps).forEach(function (n) { if (st.cryptoMaps[n].peer) peer = st.cryptoMaps[n].peer; });
    L.push(pad(peer, 18) + pad(local, 18) + pad('QM_IDLE', 15) + pad('1001', 10) + 'ACTIVE');
  }
  return L.join('\n');
}

function showCryptoIpsecSa(dev) {
  var st = dev.getState(), L = [];
  if (st.vpn.ipsec !== 'up') {
    L.push('interface: (no active IPsec SAs)');
    return L.join('\n');
  }
  var mapName = st.vpn.map, cm = st.cryptoMaps[mapName] || {};
  L.push('interface: ' + (st.vpn.iface || 'GigabitEthernet0/1'));
  if (mapName) L.push('    Crypto map tag: ' + mapName + ', local addr ' + st.vpn.localAddr);
  L.push('   protected vrf: (none)');
  L.push('   local  ident (addr/mask/prot/port): (' + st.vpn.localIdent + '/0/0)');
  L.push('   remote ident (addr/mask/prot/port): (' + st.vpn.remoteIdent + '/0/0)');
  L.push('   current_peer ' + (cm.peer || '') + ' port 500');
  L.push('     #pkts encaps: ' + st.vpn.encaps + ', #pkts encrypt: ' + st.vpn.encaps +
         ', #pkts digest: ' + st.vpn.encaps);
  L.push('     #pkts decaps: ' + st.vpn.decaps + ', #pkts decrypt: ' + st.vpn.decaps +
         ', #pkts verify: ' + st.vpn.decaps);
  return L.join('\n');
}

function showCryptoMap(dev) {
  var st = dev.getState(), L = [];
  Object.keys(st.cryptoMaps).forEach(function (n) {
    var cm = st.cryptoMaps[n];
    L.push('Crypto Map "' + n + '" ' + cm.seq + ' ipsec-isakmp');
    if (cm.peer) L.push('        Peer = ' + cm.peer);
    if (cm.acl) L.push('        Extended IP access list ' + cm.acl);
    L.push('        Current peer: ' + (cm.peer || 'none'));
    L.push('        Security association lifetime: 4608000 kilobytes/3600 seconds');
    if (cm.ts) L.push('        Transform sets={ ' + cm.ts + ', }');
    var ifs = [];
    Object.keys(st.interfaces).forEach(function (c) {
      if (st.interfaces[c].cryptoMap === n) ifs.push(st.interfaces[c].display);
    });
    if (ifs.length) L.push('        Interfaces using crypto map: ' + ifs.join(', '));
    L.push('');
  });
  if (!Object.keys(st.cryptoMaps).length) L.push('% No crypto maps configured.');
  return L.join('\n');
}

/* --------------------------------- export --------------------------------- */
root.IOSDevice = IOSDevice;
root.IOSCanonIface = canonIface;
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { IOSDevice: IOSDevice, canonIface: canonIface };
}
})(typeof window !== 'undefined' ? window : global);
