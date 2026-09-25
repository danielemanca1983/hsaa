'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function element() {
  return { listeners: {}, addEventListener(type, fn) { this.listeners[type] = fn; },
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    querySelectorAll() { return []; }, contains() { return false; }, getAttribute() { return 'false'; }, setAttribute() {}, focus() {} };
}
function form(values, organisation, valid = true) {
  const f = element(); f.values = values; f.dataset = { organisation };
  f.reportValidity = () => valid; f.status = { textContent: '' };
  f.querySelector = () => f.status; return f;
}
const school = form({ name: 'A & B', school: 'School + Academy', competition: 'Nine a side League — Girls', date: '2026-09-15', score: 'A 2 – 1 B' }, 'School');
const district = form({ name: 'Reporter', school: 'Hackney', competition: 'Kay Trophy', date: '2026-09-15', score: 'Hackney 3 – 2 District B' }, 'District');
const invalid = form({}, 'School', false);
const memberValues = { name: 'Player', email: 'player+alumni@example.com', mobile: '0123456789', season: '1981–82', manager: 'Manager', category: 'Senior — 18 and over (£10 annually)', teammate1: 'One', teammate2: 'Two', 'contact-teammates': 'Yes', 'teammate-emails': 'one@example.com; two@example.com', 'annual-event': 'Yes' };
const member = form(memberValues);
const menu = element(), nav = element(), doc = element();
doc.documentElement = element();
doc.querySelector = selector => selector === '.menu-toggle' ? menu : selector === '#main-nav' ? nav : null;
doc.querySelectorAll = selector => selector === '.result-form' ? [school, district, invalid] : selector === '.membership-form' ? [member] : [];
const window = { location: { href: '' } };
vm.runInNewContext(fs.readFileSync('dist/js/main.js', 'utf8'), {
  document: doc, window, FormData: class { constructor(f) { this.values = f.values; } get(key) { return this.values[key]; } }, encodeURIComponent
});
function submit(f) { let prevented = false; f.listeners.submit({ preventDefault() { prevented = true; } }); assert.ok(prevented); return new URL(window.location.href); }
let mail = submit(school);
assert.equal(mail.protocol, 'mailto:'); assert.equal(mail.pathname, 'info@hsaa.org.uk');
assert.ok(mail.searchParams.get('body').includes('Name: A & B'));
assert.ok(mail.searchParams.get('body').includes('School: School + Academy'));
assert.ok(mail.searchParams.get('body').includes('A 2 – 1 B'));
mail = submit(district); assert.ok(mail.searchParams.get('body').includes('District: Hackney'));
assert.equal(mail.searchParams.get('subject'), 'HSAA result: Kay Trophy');
const prior = window.location.href; submit(invalid); assert.equal(window.location.href, prior);
mail = submit(member); assert.equal(mail.searchParams.get('subject'), 'HSAA Alumni Network membership');
for (const value of Object.values(memberValues)) assert.ok(mail.searchParams.get('body').includes(value), value);
assert.ok(member.status.textContent.includes('has not sent or stored'));
console.log('Email behavior checks passed: school and district scope, invalid forms, encoded values and all alumni membership fields.');
