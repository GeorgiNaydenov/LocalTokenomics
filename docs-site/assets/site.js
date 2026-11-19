(function () {
  var PB = window.PB, root = document.body.dataset.root || '', page = document.body.dataset.page || '';
  var el = function (t, a, kids) { var e = document.createElement(t); for (var k in (a || {})) e.setAttribute(k, a[k]); [].concat(kids || []).forEach(function (c) { e.append(c && c.nodeType ? c : document.createTextNode(c == null ? '' : c)); }); return e; };
  document.getElementById('project').textContent = PB.project;
  // navigation: the same layered tree on every page, opened at the current page
  var nav = document.getElementById('nav');
  PB.tree.forEach(function (top) {
    var here = top.layers.some(function (l) { return l.groups.some(function (g) { return g.pages.some(function (p) { return p.href === page; }); }); });
    var d = el('details', here ? { open: '' } : {}, [el('summary', {}, [el('strong', {}, top.title), top.togaf ? el('small', { class: 'muted' }, '  ' + top.togaf) : ''])]);
    top.layers.forEach(function (l) {
      var box = l.nested || top.layers.length > 1 ? el('details', { class: 'sub' }, [el('summary', {}, l.title)]) : d;
      l.groups.forEach(function (g) {
        var ul = el('ul', {}, g.pages.map(function (p) { var a = el('a', { href: root + p.href }, p.title); if (p.href === page) a.setAttribute('aria-current', 'page'); return el('li', {}, a); }));
        var open = g.pages.some(function (p) { return p.href === page; });
        box.append(el('details', open ? { open: '' } : {}, [el('summary', {}, g.name + ' (' + g.pages.length + ')'), ul]));
        if (open && box !== d) box.setAttribute('open', '');
      });
      if (box !== d) d.append(box);
    });
    nav.append(d);
  });
  // links panel: what this note links to and what links to it
  var rail = document.getElementById('rail'), L = PB.links[page];
  var list = function (title, items) { if (!items || !items.length) return; rail.append(el('h3', {}, title + ' (' + items.length + ')'), el('ul', {}, items.map(function (i) { return el('li', {}, el('a', { href: root + i.href }, i.title)); }))); };
  if (L) { list('Links to', L.out); list('Linked from', L.back); if (!L.out.length && !L.back.length) rail.append(el('p', { class: 'muted' }, 'This note has no links to or from other notes.')); } else rail.style.display = 'none';
  // search over titles, headings and tags
  var q = document.getElementById('q'), box = document.getElementById('results');
  q.addEventListener('input', function () {
    var s = q.value.trim().toLowerCase(); box.innerHTML = '';
    if (s.length < 2) { box.style.display = 'none'; return; }
    var hits = PB.search.filter(function (r) { return (r.t + ' ' + r.x + ' ' + r.g.join(' ')).toLowerCase().indexOf(s) >= 0; }).slice(0, 25);
    hits.forEach(function (r) { box.append(el('a', { href: root + r.h }, [r.t, el('br'), el('small', {}, r.p)])); });
    if (!hits.length) box.append(el('p', { class: 'muted', style: 'padding:.5rem' }, 'Nothing found.'));
    box.style.display = 'block';
  });
  document.addEventListener('click', function (e) { if (!box.contains(e.target) && e.target !== q) box.style.display = 'none'; });
  // knowledge graph page
  if (document.body.dataset.kind === 'graph') {
    var C = { strategy: '#f5deaa', business: '#fff2cc', application: '#dae8fc', data: '#d5e8d4', infrastructure: '#d5e8d4', operations: '#d5e8d4', security: '#e1d5e7', requirements: '#e1d5e7', risks: '#f8cecc', decisions: '#ffe6cc', releases: '#ffe6cc', governance: '#ffe6cc', change: '#ffe6cc', other: '#f5f5f5' };
    var nodes = PB.graph.nodes, edges = PB.graph.edges, W = 1300, H = Math.max(520, Math.min(900, 260 + nodes.length * 6)), idx = {}, P = [];
    nodes.forEach(function (n, i) { idx[n.id] = i; var a = i / nodes.length * 6.283; P.push({ x: W / 2 + Math.cos(a) * W * .35, y: H / 2 + Math.sin(a) * H * .35, vx: 0, vy: 0 }); });
    var ls = edges.map(function (e) { return [idx[e.from], idx[e.to]]; }).filter(function (p) { return p[0] != null && p[1] != null && p[0] !== p[1]; });
    for (var it = 0; it < 300; it++) {
      var cool = 1 - it / 300;
      for (var i = 0; i < P.length; i++) for (var j = i + 1; j < P.length; j++) { var dx = P[i].x - P[j].x, dy = P[i].y - P[j].y, d2 = dx * dx + dy * dy + .01, f = 9000 / d2, d = Math.sqrt(d2); dx /= d; dy /= d; P[i].vx += dx * f; P[i].vy += dy * f; P[j].vx -= dx * f; P[j].vy -= dy * f; }
      ls.forEach(function (l) { var a = P[l[0]], b = P[l[1]], dx = b.x - a.x, dy = b.y - a.y, d = Math.sqrt(dx * dx + dy * dy) + .01, f = (d - 120) * .02; a.vx += dx / d * f; a.vy += dy / d * f; b.vx -= dx / d * f; b.vy -= dy / d * f; });
      P.forEach(function (p) { p.vx += (W / 2 - p.x) * .012; p.vy += (H / 2 - p.y) * .012; p.x = Math.min(W - 60, Math.max(60, p.x + p.vx * .5 * cool)); p.y = Math.min(H - 40, Math.max(30, p.y + p.vy * .5 * cool)); p.vx *= .6; p.vy *= .6; });
    }
    var NS = 'http://www.w3.org/2000/svg', s = document.createElementNS(NS, 'svg'), mk = function (n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; };
    s.setAttribute('viewBox', '0 0 ' + W + ' ' + H); s.setAttribute('style', 'width:100%;height:auto;display:block');
    var lines = ls.map(function (l) { var ln = mk('line', { x1: P[l[0]].x, y1: P[l[0]].y, x2: P[l[1]].x, y2: P[l[1]].y, stroke: '#9aa5ad', 'stroke-width': 1.1 }); s.append(ln); return [l, ln]; });
    var circles = nodes.map(function (n, i) {
      var g = mk('g', { transform: 'translate(' + P[i].x + ',' + P[i].y + ')', style: 'cursor:pointer', tabindex: 0 });
      var deg = ls.filter(function (l) { return l[0] === i || l[1] === i; }).length;
      g.append(mk('circle', { r: 6 + Math.min(10, deg * 1.5), fill: C[n.layer] || '#f5f5f5', stroke: '#222', 'stroke-width': 1.2 }));
      var t = mk('text', { y: 20, 'text-anchor': 'middle' }); t.textContent = n.label.length > 26 ? n.label.slice(0, 25) + '…' : n.label; g.append(t);
      g.addEventListener('click', function () { location.href = n.id; });
      g.addEventListener('mouseenter', function () { circles.forEach(function (c, k) { var near = k === i || ls.some(function (l) { return (l[0] === i && l[1] === k) || (l[1] === i && l[0] === k); }); c.style.opacity = near ? 1 : .2; }); lines.forEach(function (x) { x[1].style.opacity = (x[0][0] === i || x[0][1] === i) ? 1 : .1; }); });
      g.addEventListener('mouseleave', function () { circles.forEach(function (c) { c.style.opacity = 1; }); lines.forEach(function (x) { x[1].style.opacity = 1; }); });
      s.append(g); return g;
    });
    document.getElementById('graph').append(s);
  }
})();
