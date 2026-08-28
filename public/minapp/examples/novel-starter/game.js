'use strict';

const SAVE_KEY = 'novel_progress';
const SCENES = {
  start: {
    speaker: 'レン',
    text: 'なあ、今日ちょっとだけ寄り道していかない？',
    choices: [
      { label: '「いいよ」', to: 'yes' },
      { label: '「また今度」', to: 'no' },
    ],
  },
  yes: {
    speaker: 'レン',
    text: 'よかった。見せたい場所があるんだ。',
    choices: [],
  },
  no: {
    speaker: 'レン',
    text: 'そっか。じゃあ、また明日。',
    choices: [],
  },
};

let currentScene = 'start';

const speaker = document.getElementById('speaker');
const text = document.getElementById('text');
const choices = document.getElementById('choices');
const saveStatus = document.getElementById('save-status');

function hasMinAppState() {
  return Boolean(
    window.minapp &&
    window.minapp.version === 1 &&
    window.minapp.state &&
    typeof window.minapp.state.get === 'function' &&
    typeof window.minapp.state.set === 'function' &&
    typeof window.minapp.state.delete === 'function'
  );
}

function render(sceneId) {
  const scene = SCENES[sceneId];
  currentScene = sceneId;
  speaker.textContent = scene.speaker;
  text.textContent = scene.text;
  choices.replaceChildren();

  for (const item of scene.choices) {
    const button = document.createElement('button');
    button.textContent = item.label;
    button.addEventListener('click', async () => {
      render(item.to);
      await saveProgress();
    });
    choices.appendChild(button);
  }
}

async function saveProgress() {
  if (!hasMinAppState()) {
    saveStatus.textContent = 'この環境はセーブなし';
    return;
  }
  await window.minapp.state.set(SAVE_KEY, { scene: currentScene });
  saveStatus.textContent = 'セーブしました';
}

async function restoreProgress() {
  if (!hasMinAppState()) {
    saveStatus.textContent = 'この環境はセーブなし';
    return;
  }
  try {
    const saved = await window.minapp.state.get(SAVE_KEY);
    if (saved && SCENES[saved.scene]) render(saved.scene);
    saveStatus.textContent = 'つづきから';
  } catch (error) {
    if (error && error.code === 'state_not_found') {
      saveStatus.textContent = 'はじめから';
      return;
    }
    throw error;
  }
}

window.addEventListener('minappready', restoreProgress);
render('start');
if (hasMinAppState()) restoreProgress();
else saveStatus.textContent = 'この環境はセーブなし';
