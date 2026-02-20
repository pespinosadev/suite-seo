/**
 * topics-email.js — Módulo "Enviar Temas del Día"
 * Depende de: API_BASE, token, allTopics, escHtml (topics.html globals)
 */

/* ── Constantes ── */
const DEFAULT_RECIPIENTS = [
  'contenidos.seo@prensaiberica.es',
  'seo@prensaiberica.es',
];

const DISCOVER_URL = 'https://docs.google.com/spreadsheets/d/1X_SK5OgYyxPlAIfos_YRqvHOXQERi9qrf2iTp8lm1ZM/edit?gid=1228257343#gid=1228257343';

const CAT_COLORS = {
  COMUNES:              '#E06000',
  NACIONAL:             '#C00000',
  MADRID:               '#003C71',
  ANDALUCIA:            '#003C71',
  BALEARES:             '#003C71',
  CANARIAS:             '#003C71',
  'CV/MURCIA':          '#003C71',
  'ASTURIAS/GALICIA':   '#003C71',
  'EXTREMADURA/ZAMORA': '#003C71',
  'CATALUNA/ARAGON':    '#003C71',
  INTERNACIONAL:        '#1F5C99',
  ECONOMIA:             '#7030A0',
  DEPORTES:             '#375623',
  REVISTAS:             '#1F4E79',
  RECURRENTES:          '#555555',
};

const DEFAULT_CAT_COLOR = '#003C71';

/* ── Estado ── */
let emailRecipients = [];
let emailMsgInitialized = false;

/* ── Helpers ── */
function todayFormatted() {
  const d = new Date();
  return [
    String(d.getDate()).padStart(2, '0'),
    String(d.getMonth() + 1).padStart(2, '0'),
    d.getFullYear(),
  ].join('/');
}

/* ── Destinatarios ── */
function renderRecipientChips() {
  const el = document.getElementById('email-recipients-chips');
  el.innerHTML = emailRecipients.map((r, i) => `
    <span style="display:inline-flex;align-items:center;gap:.3rem;
      background:var(--primary);color:#fff;padding:.2rem .55rem;
      border-radius:4px;font-size:.75rem;font-weight:500;white-space:nowrap">
      ${escHtml(r)}
      <button onclick="removeEmailRecipient(${i})"
        style="background:none;border:none;color:#fff;cursor:pointer;
               padding:0;line-height:1;font-size:.9rem">×</button>
    </span>`).join('');

  const input = document.createElement('input');
  input.id = 'email-new-recipient';
  input.type = 'email';
  input.placeholder = emailRecipients.length ? '' : 'nuevo@email.com';
  input.style.cssText = [
    'border:none;outline:none;background:transparent',
    'font-size:.8rem;min-width:140px;flex:1;padding:.1rem .2rem',
    'color:var(--text-primary)',
  ].join(';');
  input.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      addEmailRecipient();
    } else if (e.key === 'Backspace' && input.value === '' && emailRecipients.length) {
      emailRecipients.pop();
      renderRecipientChips();
    }
  });
  el.appendChild(input);
}

function removeEmailRecipient(i) {
  emailRecipients.splice(i, 1);
  renderRecipientChips();
}

function addEmailRecipient() {
  const input = document.getElementById('email-new-recipient');
  const val = input.value.trim().replace(/,$/, '');
  if (!val || !val.includes('@')) return;
  if (!emailRecipients.includes(val)) {
    emailRecipients.push(val);
    renderRecipientChips();
  } else {
    input.value = '';
  }
}

/* ── Editor de mensaje ── */
function emailExecCmd(cmd) {
  document.getElementById('email-message').focus();
  document.execCommand(cmd);
}

function emailInsertLink() {
  const url = prompt('URL del enlace:');
  if (!url) return;
  const text = prompt('Texto del enlace (deja vacío para usar la URL):') || url;
  document.getElementById('email-message').focus();
  document.execCommand('insertHTML', false,
    `<a href="${url}" style="color:#1F5C99">${escHtml(text)}</a>`);
}

function emailInsertEmoji() {
  const emojis = ['😊','👍','🙌','✅','🔥','📰','📊','🎯','⚡','💡'];
  let picker = document.getElementById('email-emoji-picker');
  if (picker) { picker.remove(); return; }

  picker = document.createElement('div');
  picker.id = 'email-emoji-picker';
  picker.style.cssText = [
    'position:absolute;background:var(--bg-card);border:1px solid var(--border)',
    'border-radius:8px;padding:.4rem;display:flex;flex-wrap:wrap;gap:.2rem',
    'z-index:200;box-shadow:0 4px 16px rgba(0,0,0,.15)',
  ].join(';');

  emojis.forEach(e => {
    const btn = document.createElement('button');
    btn.textContent = e;
    btn.className = 'seo-btn seo-btn-icon';
    btn.style.fontSize = '1.1rem';
    btn.onclick = () => {
      document.getElementById('email-message').focus();
      document.execCommand('insertText', false, e);
      picker.remove();
    };
    picker.appendChild(btn);
  });

  const toolbar = document.getElementById('email-editor-toolbar');
  toolbar.style.position = 'relative';
  toolbar.appendChild(picker);
  setTimeout(() => document.addEventListener('click', function close(ev) {
    if (!picker.contains(ev.target)) { picker.remove(); document.removeEventListener('click', close); }
  }), 100);
}

/* ── Generación del HTML del correo ── */
function _topicsToCols(topics) {
  const n = topics.length <= 3 ? 1 : topics.length <= 6 ? 2 : 3;
  const size = Math.ceil(topics.length / n);
  const cols = [];
  for (let i = 0; i < topics.length; i += size) cols.push(topics.slice(i, i + size));
  return cols;
}

function generateEmailHtml() {
  const msgEl  = document.getElementById('email-message');
  const subjectVal = document.getElementById('email-subject').value.trim();

  // Agrupar topics por categoría, ordenar por display_order
  const grouped = {};
  const uncategorized = [];
  allTopics.forEach(t => {
    if (t.category) {
      const k = t.category.name;
      if (!grouped[k]) grouped[k] = { topics: [], order: t.category.display_order ?? 999 };
      grouped[k].topics.push(t);
    } else {
      uncategorized.push(t);
    }
  });

  const entries = Object.entries(grouped).sort((a, b) => a[1].order - b[1].order);
  if (uncategorized.length) entries.unshift(['RECURRENTES', { topics: uncategorized, order: 0 }]);

  // Filas de la tabla
  const rows = entries.map(([catName, catData]) => {
    const color = CAT_COLORS[catName] || DEFAULT_CAT_COLOR;
    const cols  = _topicsToCols(catData.topics);
    const colW  = Math.floor(640 / cols.length);
    const cells = cols.map(col =>
      `<td width="${colW}" valign="top" style="padding:6px 10px;font-size:12px;font-family:Arial,sans-serif;vertical-align:top">
        ${col.map(t => `• ${escHtml(t.title)}`).join('<br>')}
      </td>`
    ).join('');
    return `
      <tr>
        <td width="140" valign="middle"
          style="background:${color};color:#fff;font-weight:bold;font-size:12px;
                 text-transform:uppercase;padding:8px 10px;font-family:Arial,sans-serif;
                 vertical-align:middle">
          ${escHtml(catName)}
        </td>
        <td style="padding:0">
          <table width="100%" cellpadding="0" cellspacing="0" border="0"><tr>${cells}</tr></table>
        </td>
      </tr>`;
  }).join('');

  const topicsTable = `
    <table width="780" border="1" cellpadding="0" cellspacing="0"
      style="border-collapse:collapse;border:1px solid #ccc;width:100%">
      ${rows}
    </table>`;

  const signature = `
    <br>
    <p style="font-family:Arial,sans-serif;font-size:13px;margin:0 0 4px">
      <strong>Un saludo,</strong><br>
      <strong>Departamento SEO</strong>
    </p>
    <p style="font-family:Arial,sans-serif;font-size:13px;margin:0 0 12px;color:#333">
      Calle Santiago Ramon y Cajal, 41, planta 0, local 1,<br>
      03203 Elche Parque Industrial, Alicante
    </p>
    <div style="border-left:4px solid #003C71;padding-left:12px;
                font-size:10px;color:#666;font-family:Arial,sans-serif">
      <p style="margin:4px 0"><strong>CONFIDENCIALIDAD Y PROTECCIÓN DE DATOS</strong></p>
      <p style="margin:4px 0">
        Este mensaje y, en su caso, cualquier fichero anexo al mismo, puede contener
        información confidencial o legalmente protegida, siendo para uso exclusivo del
        destinatario. Queda expresamente prohibida su divulgación, copia o distribución a
        terceros sin la autorización expresa del remitente. Si ha recibido este mensaje por
        error, se ruega lo notifique al remitente y proceda inmediatamente al borrado del
        mensaje original y de todas sus copias. Muchas gracias por su colaboración.
      </p>
      <p style="margin:4px 0">
        Los datos personales derivados de su correspondencia, incluyendo sus datos de
        contacto, serán tratados por El Periódico de Catalunya, SLU, con finalidad exclusiva
        de gestionar sus comunicaciones y su actividad profesional. Puede ejercitar sus
        derechos de acceso, rectificación, supresión y portabilidad de sus datos, de
        limitación y oposición a su tratamiento, así como a no ser objeto de decisiones
        basadas únicamente en el tratamiento automatizado de sus datos, cuando proceda por
        correo electrónico a
        <a href="mailto:protecciondatos@prensaiberica.es">protecciondatos@prensaiberica.es</a>.
      </p>
      <p style="margin:4px 0">
        Puede obtener información adicional en
        <a href="https://www.prensaiberica.es/politica-de-privacidad-extendida/">
          https://www.prensaiberica.es/politica-de-privacidad-extendida/
        </a>
      </p>
    </div>`;

  return `
    <div style="max-width:820px;font-family:Arial,sans-serif">
      <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:18px">
        <tr>
          <td style="background:#003C71;color:#fff;font-size:20px;font-weight:bold;
                     text-align:center;padding:16px 24px;border-radius:4px">
            ${escHtml(subjectVal)}
          </td>
        </tr>
      </table>
      <div style="font-size:13px;font-family:Arial,sans-serif;margin-bottom:18px;line-height:1.6">
        ${msgEl.innerHTML}
      </div>
      ${topicsTable}
      ${signature}
    </div>`;
}

/* ── Vista previa ── */
function updateEmailPreview() {
  const html = generateEmailHtml();
  const wrap = document.getElementById('email-preview-wrap');
  wrap.innerHTML = '';
  const iframe = document.createElement('iframe');
  iframe.style.cssText = 'width:100%;border:none;display:block;min-height:300px';
  iframe.srcdoc = `<!DOCTYPE html><html><body style="margin:8px;padding:0">${html}</body></html>`;
  iframe.onload = () => {
    try {
      iframe.style.height = (iframe.contentDocument.body.scrollHeight + 16) + 'px';
    } catch (_) {}
  };
  wrap.appendChild(iframe);
}

/* ── Abrir modal ── */
function openSendEmailModal() {
  // Destinatarios — reset siempre a los por defecto
  emailRecipients = [...DEFAULT_RECIPIENTS];
  renderRecipientChips();

  // Asunto — fecha de hoy
  document.getElementById('email-subject').value =
    `Temas del día SEO - ${todayFormatted()}`;

  // Mensaje — inicializar solo la primera vez (conservar ediciones del usuario)
  if (!emailMsgInitialized) {
    document.getElementById('email-message').innerHTML =
      `Buenos días!! 😊<br><br>` +
      `En el siguiente mail os dejamos:<br>` +
      `1. Las tendencias del día<br>` +
      `2. Enlace actualizado al documento de Discover Snoop: ` +
      `<a href="${DISCOVER_URL}" style="color:#1F5C99">${DISCOVER_URL}</a>`;
    emailMsgInitialized = true;
  }

  document.getElementById('modal-send-email').classList.add('show');

  // Generar preview automáticamente al abrir
  setTimeout(updateEmailPreview, 50);
}

/* ── Enviar ── */
async function sendEmail() {
  if (!emailRecipients.length) {
    alert('Añade al menos un destinatario.');
    return;
  }
  const subject = document.getElementById('email-subject').value.trim();
  if (!subject) { alert('El asunto es obligatorio.'); return; }

  const htmlBody = generateEmailHtml();
  const btn = document.getElementById('btn-send-email');
  btn.disabled = true;
  btn.textContent = 'Enviando…';

  try {
    const res = await fetch(`${API_BASE}/api/topics/send`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ recipients: emailRecipients, subject, html_body: htmlBody }),
    });

    if (!res.ok) {
      const d = await res.json().catch(() => ({}));
      alert(d.detail || 'Error al enviar el correo.');
      return;
    }

    closeModal('modal-send-email');
    await fetchTopics();           // refresca lista (topics ya marcados como enviados)
  } catch (e) {
    console.error(e);
    alert('Error de red al enviar el correo.');
  } finally {
    btn.disabled = false;
    btn.textContent = '📧 Enviar Correo';
  }
}
