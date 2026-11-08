// The Code page's editor, drawn by Lory: the program drawn/edit.co, built
// for the web (drawn/edit_web/, served at /edit/), mounted in the widget's
// element by the page as `widget['editor', props = map[text = …, mode =
// 'cell' | 'file'], on = map[change = …, save = …, run = …, whole = …]]`.
//
// The page and the program speak as edit.co says: the module gives the
// program `props` then the text to edit, `ask` for the text as it is now,
// and `blur` when the keyboard went elsewhere; the program prints `@rows`,
// `@edit`, `@text`, `@save`, `@run`, `@all` and `@focus`. What the editor
// sends the page: `change` (the text, 400 ms after the last edit, and at
// once when a press lands elsewhere — so a handler the press reaches reads
// the latest text), `save` (Ctrl+S or Cmd+S), `run` (Ctrl+Enter) and
// `whole` (Ctrl+Shift+Enter: every cell, or the file), each with the text.
//
// One editor is shown at a time (the cell or the file being edited), and
// its WebGL context is kept: an editor whose element left the page waits
// in a pool for the next mount, so a cell edited after another needs no
// new module, no new context.
'use strict';

const LOADER = '/edit/crow.js';
const MODULE = '/edit/edit.wasm';
const LINE = 19;   // a line's height in CSS pixels, as editor.co draws it
const PAD = 6;     // the editor's padding
const FEWEST = 4;  // a cell's editor shows at least this many lines…
const MOST = 40;   // …and grows to this many before it scrolls

let loading = null;
const pool = [];
let focused = null;

// crow.js, loaded once: a classic script that declares `Crow`
function loaded() {
  if (loading) return loading;
  loading = new Promise((ok, no) => {
    if (typeof Crow !== 'undefined') return ok();
    const s = document.createElement('script');
    s.src = LOADER;
    s.onload = () => ok();
    s.onerror = () => no(new Error('the editor\'s loader ' + LOADER + ' did not load'));
    document.head.appendChild(s);
  });
  return loading;
}

// an editor: its canvas and page, the element it is in, how to reach the
// page's handlers, the text as the program last had it, and an edit not
// yet sent
async function instance() {
  if (pool.length) return pool.pop();
  await loaded();
  const canvas = document.createElement('canvas');
  canvas.className = 'editor-canvas';
  const inst = { canvas, page: null, el: null, send: null, known: null, rows: 1, mode: 'cell', pending: false, timer: 0, active: false, answer: null };
  inst.page = await Crow.start({ canvas, module: MODULE, manual: true, said: (kind, text) => heard(inst, kind, text) });
  return inst;
}

function tell(inst, event, text) {
  clearTimeout(inst.timer);
  inst.pending = false;
  inst.known = text;
  if (inst.send) inst.send(event, text);
}

// the text as it is now, asked of the program and answered in the same
// frame, sent as a change
function flush(inst) {
  if (!inst.pending || !inst.page || !inst.active) return;
  clearTimeout(inst.timer);
  inst.answer = null;
  inst.page.give({ type: 'ask' });
  inst.page.step(performance.now());
  if (inst.answer !== null) tell(inst, 'change', inst.answer);
}

function sized(inst, rows) {
  inst.rows = rows;
  if (inst.mode === 'cell') {
    const shown = Math.max(FEWEST, Math.min(MOST, rows));
    inst.canvas.style.height = (shown * LINE + 2 * PAD) + 'px';
  } else {
    inst.canvas.style.height = '';
  }
}

function focusing(inst, on) {
  if (on) {
    if (focused && focused !== inst) {
      flush(focused);
      focused.page.give({ type: 'blur' });
    }
    focused = inst;
  } else if (focused === inst) {
    focused = null;
  }
}

// what the program printed
function heard(inst, kind, text) {
  if (kind !== 'log') {
    if (kind === 'error' || kind === 'stopped') console.error('editor: ' + text);
    return;
  }
  const at = text.indexOf(' ');
  const word = at < 0 ? text : text.slice(0, at);
  const rest = at < 0 ? '' : text.slice(at + 1);
  switch (word) {
    case '@rows': sized(inst, Number(rest)); break;
    case '@edit':
      inst.pending = true;
      clearTimeout(inst.timer);
      inst.timer = setTimeout(() => flush(inst), 400);
      break;
    case '@text': inst.answer = JSON.parse(rest); break;
    case '@save': tell(inst, 'save', JSON.parse(rest)); break;
    case '@run': tell(inst, 'run', JSON.parse(rest)); break;
    case '@all': tell(inst, 'whole', JSON.parse(rest)); break;
    case '@focus': focusing(inst, rest === '1'); break;
    default: break;
  }
}

// the props applied: the mode sizes the canvas, and a text the program
// does not have is given it (one it reported itself is not: the page
// echoing a change back must not move the caret)
function apply(inst, props) {
  inst.mode = props.mode === 'file' ? 'file' : 'cell';
  inst.canvas.className = 'editor-canvas editor-' + inst.mode;
  sized(inst, inst.rows);
  const text = typeof props.text === 'string' ? props.text : '';
  if (text !== inst.known) {
    clearTimeout(inst.timer);
    inst.pending = false;
    inst.known = text;
    inst.page.give({ type: 'props' });
    inst.page.give({ type: 'text', text });
  }
}

// a frame a screen refresh: the program draws when something happened
function loop(inst) {
  requestAnimationFrame((t) => {
    if (!inst.active) return;
    if (!inst.el || !inst.el.isConnected) {
      release(inst);
      return;
    }
    inst.page.step(t);
    loop(inst);
  });
}

function attach(inst, holder) {
  inst.el = holder.el;
  inst.send = holder.send;
  inst.active = true;
  holder.el.appendChild(inst.canvas);
  apply(inst, holder.props);
  loop(inst);
}

// an editor whose element left the page: back in the pool, its keyboard
// let go (the page moved on — a save or a cancel took the element — so an
// edit not yet sent is not sent)
function release(inst) {
  inst.active = false;
  clearTimeout(inst.timer);
  inst.pending = false;
  if (focused === inst) focused = null;
  inst.page.give({ type: 'blur' });
  inst.canvas.remove();
  inst.el = null;
  inst.send = null;
  inst.known = null;
  pool.push(inst);
}

export function mount(el, props, send) {
  const holder = { el, props, send };
  el.__editor = holder;
  instance().then((inst) => {
    if (!el.isConnected) {
      pool.push(inst);
      return;
    }
    holder.inst = inst;
    attach(inst, holder);
  }).catch((e) => {
    el.textContent = 'the editor did not load: ' + (e && e.message ? e.message : e);
  });
}

export function update(el, props) {
  const holder = el.__editor;
  if (!holder) return;
  holder.props = props;
  if (holder.inst && holder.inst.active) apply(holder.inst, props);
}

// ---- the page's keys and presses, once ----

// whether an element is an editor's: its canvas, or the hidden text field
// crow.js types through (a textarea it puts under the body, invisible)
function ours(t) {
  if (!t || !t.tagName) return false;
  if (t.tagName === 'CANVAS' && t.classList.contains('editor-canvas')) return true;
  return t.tagName === 'TEXTAREA' && t.parentElement === document.body && t.style.opacity === '0';
}

// crow.js listens for keys on the window, for every editor made: a key
// typed anywhere else on the page — a field, a button — never reaches
// them (it would stop a Backspace or a Tab there)
document.addEventListener('keydown', (e) => { if (!ours(e.target)) e.stopPropagation(); });
document.addEventListener('keyup', (e) => { if (!ours(e.target)) e.stopPropagation(); });

// Ctrl+S, Ctrl+Enter and Ctrl+Shift+Enter in an editor are the editor's
// (the page's own shortcuts leave a key whose default is prevented alone,
// and the browser does not save the page)
window.addEventListener('keydown', (e) => {
  if (!focused || !ours(e.target)) return;
  if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S' || e.key === 'Enter')) e.preventDefault();
}, true);

// a paste goes to the editor with the keyboard as typed text
document.addEventListener('paste', (e) => {
  if (!focused || !ours(e.target)) return;
  const words = (e.clipboardData || window.clipboardData).getData('text');
  if (words) focused.page.give({ type: 'text', text: words });
  e.preventDefault();
});

// a press anywhere but an editor takes the keyboard from it, its latest
// text sent first: a Run or Save the press reaches reads it
document.addEventListener('pointerdown', (e) => {
  if (!focused || ours(e.target)) return;
  const was = focused;
  focused = null;
  flush(was);
  was.page.give({ type: 'blur' });
}, true);
