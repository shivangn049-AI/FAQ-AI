const FAQS = [
  { q: 'How do I reset my password?', a: 'You can reset your password by clicking the Forgot Password link on the login page and following the email instructions.' },
  { q: 'What is your refund policy?', a: 'We offer a full refund within 30 days of purchase if the product is unused and in its original packaging.' },
  { q: 'How can I contact support?', a: 'You can reach our support team by emailing support@example.com or using the contact form on our website.' },
  { q: 'Do you offer a free trial?', a: 'Yes, we provide a 14-day free trial for new users so they can explore the platform before upgrading.' },
  { q: 'How do I update my billing information?', a: 'Billing details can be updated from the Account Settings page under the Billing section.' }
];

const CONFIDENCE_THRESHOLD = 0.15;
const FALLBACK_ANSWER = "I'm not confident I have a good answer for that yet. Could you rephrase, or contact support@example.com for help?";

const messagesEl = document.getElementById('messages');
const composer = document.getElementById('composer');
const input = document.getElementById('userInput');
const faqList = document.getElementById('faqList');
document.getElementById('thresholdValue').textContent = CONFIDENCE_THRESHOLD.toFixed(2) + ' cosine';

FAQS.forEach((faq) => {
  const li = document.createElement('li');
  li.textContent = faq.q;
  li.tabIndex = 0;
  li.addEventListener('click', () => sendMessage(faq.q));
  faqList.appendChild(li);
});

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function appendUserMessage(text) {
  const wrap = document.createElement('div');
  wrap.className = 'msg user';
  wrap.innerHTML = '<div class="msg-bubble"></div>';
  wrap.querySelector('.msg-bubble').textContent = text;
  messagesEl.appendChild(wrap);
  scrollToBottom();
}

function appendTypingIndicator() {
  const wrap = document.createElement('div');
  wrap.className = 'msg bot typing';
  wrap.id = 'typingIndicator';
  wrap.innerHTML = '<div class="msg-bubble">matching…</div>';
  messagesEl.appendChild(wrap);
  scrollToBottom();
}

function removeTypingIndicator() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}

function appendBotMessage(reply, confidence = 0, matched = false) {
  const pct = Math.max(0, Math.min(1, confidence)) * 100;
  const low = !matched;

  const wrap = document.createElement('div');
  wrap.className = 'msg bot';
  wrap.innerHTML = `
    <div class="msg-block">
      <div class="msg-bubble"></div>
      <div class="confidence">
        <span class="confidence-label">match</span>
        <div class="confidence-track"><div class="confidence-fill ${low ? 'low' : ''}" style="width:0%"></div></div>
        <span class="confidence-score">${confidence.toFixed(2)}</span>
      </div>
    </div>`;
  wrap.querySelector('.msg-bubble').textContent = reply;
  messagesEl.appendChild(wrap);

  requestAnimationFrame(() => {
    wrap.querySelector('.confidence-fill').style.width = pct + '%';
  });
  scrollToBottom();
}

async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  appendUserMessage(trimmed);
  input.value = '';
  appendTypingIndicator();

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: trimmed })
    });

    const data = await response.json();
    removeTypingIndicator();
    const confidence = Number(data.confidence ?? 0);
    appendBotMessage(data.reply || FALLBACK_ANSWER, confidence, confidence >= CONFIDENCE_THRESHOLD);
  } catch (error) {
    removeTypingIndicator();
    appendBotMessage(FALLBACK_ANSWER, 0, false);
  }
}

composer.addEventListener('submit', (event) => {
  event.preventDefault();
  sendMessage(input.value);
});
