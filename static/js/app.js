/**
 * SpamShield AI - Frontend Application Logic
 * Integrates real-time classification, probability visualization, token highlighting,
 * history management, theme toggling, and ML evaluation reporting.
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const themeToggle = document.getElementById("themeToggle");
  const themeIconSun = document.getElementById("themeIconSun");
  const themeIconMoon = document.getElementById("themeIconMoon");
  const mobileMenuBtn = document.getElementById("mobileMenuBtn");
  const navLinks = document.getElementById("navLinks");
  const statusPill = document.getElementById("statusPill");
  const statusText = document.getElementById("statusText");

  // Detector Elements
  const messageInput = document.getElementById("messageInput");
  const charCount = document.getElementById("charCount");
  const wordCount = document.getElementById("wordCount");
  const btnClear = document.getElementById("btnClear");
  const btnPaste = document.getElementById("btnPaste");
  const btnAnalyze = document.getElementById("btnAnalyze");
  const scanProgressWrap = document.getElementById("scanProgressWrap");
  const scanStatusSubtext = document.getElementById("scanStatusSubtext");

  // Result Elements
  const resultCard = document.getElementById("resultCard");
  const verdictIcon = document.getElementById("verdictIcon");
  const verdictTitle = document.getElementById("verdictTitle");
  const verdictTag = document.getElementById("verdictTag");
  const confidenceVal = document.getElementById("confidenceVal");
  const probSpamText = document.getElementById("probSpamText");
  const probNormalText = document.getElementById("probNormalText");
  const probBarSpam = document.getElementById("probBarSpam");
  const probBarNormal = document.getElementById("probBarNormal");
  const highlightBox = document.getElementById("highlightBox");
  const reasonsList = document.getElementById("reasonsList");
  const recList = document.getElementById("recList");
  const linksDetailsCard = document.getElementById("linksDetailsCard");
  const linksList = document.getElementById("linksList");
  const disclaimerText = document.getElementById("disclaimerText");

  // History Elements
  const historyList = document.getElementById("historyList");
  const emptyHistoryState = document.getElementById("emptyHistoryState");
  const btnClearHistory = document.getElementById("btnClearHistory");
  const filterBtns = document.querySelectorAll(".filter-btn");

  // Modal Elements
  const modelModal = document.getElementById("modelModal");
  const btnViewModelReport = document.getElementById("btnViewModelReport");
  const btnCloseModelModal = document.getElementById("btnCloseModelModal");
  const modelModalBody = document.getElementById("modelModalBody");

  const historyModal = document.getElementById("historyModal");
  const btnCloseHistoryModal = document.getElementById("btnCloseHistoryModal");
  const historyModalBody = document.getElementById("historyModalBody");

  // Contact Form
  const contactForm = document.getElementById("contactForm");

  // Preset Sample Data
  const samplePresets = {
    lottery: "CONGRATULATIONS! You have won a $1,000 Walmart Gift Card! Claim your prize now: http://claim-cards.biz/win",
    bank: "CHASE BANK ALERT: Your debit card has been suspended due to suspicious activity. Verify identity at https://chase-secure-reactivate.com",
    parcel: "USPS ALERT: Your parcel #US948123 could not be delivered due to incomplete address. Pay $1.99 redelivery fee at https://usps-track-parcel.vip",
    crypto: "Exclusive Bitcoin Alert: AI trading bot generated +420% profit this week! Join VIP Telegram free: https://t.me/crypto-signals-vip",
    friend: "Hey Alex, are we still on for lunch at Chipotle around 12:30? Let me know when you're heading out!",
    meeting: "Hi team, please find attached the revised project schedule for Q4. Let's discuss in our standup tomorrow."
  };

  // State
  let currentFilter = "all";
  let historyCache = [];

  // =========================================================================
  // 1. Theme Management (Dark / Light)
  // =========================================================================
  const savedTheme = localStorage.getItem("spamshield_theme") || "dark";
  applyTheme(savedTheme);

  themeToggle.addEventListener("click", () => {
    const currentTheme = document.documentElement.getAttribute("data-theme") || "dark";
    const nextTheme = currentTheme === "dark" ? "light" : "dark";
    applyTheme(nextTheme);
    localStorage.setItem("spamshield_theme", nextTheme);
    showToast(`Switched to ${nextTheme} theme`);
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    if (theme === "dark") {
      themeIconSun.style.display = "none";
      themeIconMoon.style.display = "block";
    } else {
      themeIconSun.style.display = "block";
      themeIconMoon.style.display = "none";
    }
  }

  // =========================================================================
  // 2. Mobile Menu & Navigation Active Link Handling
  // =========================================================================
  mobileMenuBtn.addEventListener("click", () => {
    navLinks.classList.toggle("mobile-open");
  });

  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
      document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
      link.classList.add("active");
      navLinks.classList.remove("mobile-open");
    });
  });

  // =========================================================================
  // 3. Textarea Counters & Preset Loading
  // =========================================================================
  function updateCounters() {
    const text = messageInput.value;
    charCount.textContent = text.length.toLocaleString();
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    wordCount.textContent = words.toLocaleString();
  }

  messageInput.addEventListener("input", updateCounters);

  // Preset sample chips
  document.querySelectorAll(".preset-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      const sampleKey = chip.getAttribute("data-sample");
      if (samplePresets[sampleKey]) {
        messageInput.value = samplePresets[sampleKey];
        updateCounters();
        messageInput.focus();
        showToast("Preset sample loaded into scanner");
      }
    });
  });

  // Clear button
  btnClear.addEventListener("click", () => {
    messageInput.value = "";
    updateCounters();
    resultCard.style.display = "none";
    messageInput.focus();
  });

  // Paste button
  btnPaste.addEventListener("click", async () => {
    try {
      if (navigator.clipboard && navigator.clipboard.readText) {
        const text = await navigator.clipboard.readText();
        messageInput.value = text;
        updateCounters();
        showToast("Pasted text from clipboard");
      } else {
        showToast("Clipboard access not supported in this browser", "error");
      }
    } catch (err) {
      showToast("Clipboard permission denied or unavailable", "error");
    }
  });

  // =========================================================================
  // 4. Main Detection Engine (AJAX Analysis)
  // =========================================================================
  btnAnalyze.addEventListener("click", runDetection);

  // Also support Ctrl+Enter in textarea
  messageInput.addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      runDetection();
    }
  });

  async function runDetection() {
    const message = messageInput.value.trim();

    if (!message) {
      showToast("Please enter or paste a message to analyze.", "error");
      messageInput.focus();
      return;
    }

    // Show Scanning State with animated step messages
    resultCard.style.display = "none";
    scanProgressWrap.style.display = "block";
    btnAnalyze.disabled = true;

    const scanSteps = [
      "Tokenizing and standardizing message text...",
      "Extracting TF-IDF n-gram feature vectors...",
      "Executing Machine Learning probabilistic classifier...",
      "Synthesizing threat explainability report..."
    ];

    let stepIdx = 0;
    const stepInterval = setInterval(() => {
      stepIdx = (stepIdx + 1) % scanSteps.length;
      scanStatusSubtext.textContent = scanSteps[stepIdx];
    }, 120);

    try {
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
      });

      const data = await response.json();
      clearInterval(stepInterval);
      scanProgressWrap.style.display = "none";
      btnAnalyze.disabled = false;

      if (!response.ok || !data.success) {
        showToast(data.error || "Failed to analyze message.", "error");
        return;
      }

      // Render Results
      renderResult(data, message);

      // Refresh History and Stats
      loadHistory();
      loadStats();

    } catch (err) {
      clearInterval(stepInterval);
      scanProgressWrap.style.display = "none";
      btnAnalyze.disabled = false;
      showToast("Network error: Could not reach the detection server.", "error");
    }
  }

  function renderResult(data, originalMessage) {
    const isSpam = data.prediction === "SPAM";

    // Card styling
    resultCard.className = `result-card ${isSpam ? "is-spam" : "is-normal"}`;
    resultCard.style.display = "block";

    // Verdict Header
    verdictTitle.textContent = isSpam ? "SPAM DETECTED" : "NORMAL MESSAGE";
    verdictTag.textContent = isSpam ? "High-Risk Threat Identified" : "Legitimate Message Verified";

    // Verdict Icon
    if (isSpam) {
      verdictIcon.innerHTML = `
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
          <line x1="12" y1="9" x2="12" y2="13"/>
          <line x1="12" y1="17" x2="12.01" y2="17"/>
        </svg>
      `;
    } else {
      verdictIcon.innerHTML = `
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <path d="M9 12l2 2 4-4"/>
        </svg>
      `;
    }

    // Confidence
    confidenceVal.textContent = `${data.confidence.toFixed(1)}%`;

    // Probability Bars
    probSpamText.textContent = `Spam Probability: ${data.spam_probability.toFixed(1)}%`;
    probNormalText.textContent = `Normal Probability: ${data.normal_probability.toFixed(1)}%`;
    probBarSpam.style.width = `${data.spam_probability}%`;
    probBarNormal.style.width = `${data.normal_probability}%`;

    // Token Highlights Box
    renderTokenHighlights(data.token_highlights, highlightBox);

    // Reasons List
    reasonsList.innerHTML = "";
    (data.reasons || []).forEach(reason => {
      const li = document.createElement("li");
      li.textContent = reason;
      reasonsList.appendChild(li);
    });

    // Recommendations List
    recList.innerHTML = "";
    (data.recommendations || []).forEach(rec => {
      const li = document.createElement("li");
      li.textContent = rec;
      recList.appendChild(li);
    });

    // Links Analysis
    if (data.links_found && data.links_found.length > 0) {
      linksDetailsCard.style.display = "block";
      linksList.innerHTML = "";
      data.links_found.forEach(link => {
        const li = document.createElement("li");
        li.className = "link-item";
        li.innerHTML = `
          <div class="link-header">
            <span class="link-url">${escapeHtml(link.url)}</span>
            <span class="risk-badge risk-${link.risk_level}">${link.risk_level} risk</span>
          </div>
          <div style="font-size: 0.8rem; color: var(--text-muted);">
            ${link.threats.join(" &bull; ")}
          </div>
        `;
        linksList.appendChild(li);
      });
    } else {
      linksDetailsCard.style.display = "none";
    }

    // Disclaimer
    if (data.disclaimer) {
      disclaimerText.textContent = data.disclaimer;
    }

    // Smooth scroll to result
    resultCard.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function renderTokenHighlights(tokens, container) {
    container.innerHTML = "";
    if (!tokens || tokens.length === 0) {
      container.textContent = "No tokens to display.";
      return;
    }

    tokens.forEach(tok => {
      if (tok.type === "suspicious_word") {
        const span = document.createElement("span");
        span.className = tok.risk === "high" ? "token-suspicious-high" : "token-suspicious-medium";
        span.textContent = tok.text;
        span.title = tok.tooltip || "Flagged pattern token";
        container.appendChild(span);
      } else if (tok.type === "suspicious_url") {
        const span = document.createElement("span");
        span.className = "token-suspicious-url";
        span.textContent = tok.text;
        span.title = tok.tooltip || "Embedded URL Target";
        container.appendChild(span);
      } else {
        const textNode = document.createTextNode(tok.text);
        container.appendChild(textNode);
      }
    });
  }

  // =========================================================================
  // 5. Detection History Management
  // =========================================================================
  async function loadHistory() {
    try {
      const res = await fetch("/api/history?limit=50");
      const data = await res.json();
      if (data.success) {
        historyCache = data.history || [];
        renderHistoryList();
      }
    } catch (err) {
      console.warn("Could not fetch history from API, checking localStorage backup:", err);
      const local = localStorage.getItem("spamshield_history");
      if (local) {
        try {
          historyCache = JSON.parse(local);
          renderHistoryList();
        } catch (e) {}
      }
    }
  }

  function renderHistoryList() {
    historyList.innerHTML = "";

    const filtered = historyCache.filter(item => {
      if (currentFilter === "all") return true;
      if (currentFilter === "spam") return item.prediction === "SPAM";
      if (currentFilter === "normal") return item.prediction === "NORMAL";
      return true;
    });

    if (filtered.length === 0) {
      emptyHistoryState.style.display = "block";
      historyList.appendChild(emptyHistoryState);
      return;
    }

    emptyHistoryState.style.display = "none";

    filtered.forEach(item => {
      const card = document.createElement("div");
      card.className = "history-card";
      card.dataset.id = item.id;

      const isSpam = item.prediction === "SPAM";
      const pillClass = isSpam ? "pill-spam" : "pill-normal";
      const dateStr = formatDate(item.created_at);

      card.innerHTML = `
        <div class="history-main">
          <div class="history-meta">
            <span class="history-verdict-pill ${pillClass}">${item.prediction}</span>
            <span>Confidence: ${item.confidence.toFixed(1)}%</span>
            <span>&bull;</span>
            <span>${dateStr}</span>
          </div>
          <div class="history-preview" title="${escapeHtml(item.message)}">
            ${escapeHtml(item.message_preview || item.message)}
          </div>
        </div>

        <div class="history-item-actions">
          <button type="button" class="btn-icon btn-view" title="View Full Analysis">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
            </svg>
          </button>
          <button type="button" class="btn-icon btn-delete" title="Delete from history">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
          </button>
        </div>
      `;

      // Event listeners for actions
      card.querySelector(".btn-view").addEventListener("click", () => openHistoryDetail(item));
      card.querySelector(".btn-delete").addEventListener("click", () => deleteHistoryRecord(item.id, card));

      historyList.appendChild(card);
    });
  }

  // Filter tabs
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.getAttribute("data-filter");
      renderHistoryList();
    });
  });

  // Delete single record
  async function deleteHistoryRecord(id, cardElem) {
    try {
      const res = await fetch(`/api/history/${id}`, { method: "DELETE" });
      const data = await res.json();
      if (data.success) {
        historyCache = historyCache.filter(h => h.id !== id);
        cardElem.style.transition = "all 0.25s ease";
        cardElem.style.opacity = "0";
        cardElem.style.transform = "translateX(-20px)";
        setTimeout(() => renderHistoryList(), 250);
        showToast("Record deleted from history.");
        loadStats();
      } else {
        showToast("Failed to delete record.", "error");
      }
    } catch (err) {
      showToast("Network error deleting record.", "error");
    }
  }

  // Clear all history
  btnClearHistory.addEventListener("click", async () => {
    if (!confirm("Are you sure you want to clear your entire detection history?")) {
      return;
    }

    try {
      const res = await fetch("/api/history", { method: "DELETE" });
      const data = await res.json();
      if (data.success) {
        historyCache = [];
        localStorage.removeItem("spamshield_history");
        renderHistoryList();
        showToast("All detection history cleared.");
        loadStats();
      }
    } catch (err) {
      showToast("Error clearing history.", "error");
    }
  });

  // History detail modal
  function openHistoryDetail(item) {
    const isSpam = item.prediction === "SPAM";
    historyModalTitle.textContent = `Detection Report: #${item.id} (${item.prediction})`;

    historyModalBody.innerHTML = `
      <div style="margin-bottom: 1.25rem;">
        <span class="history-verdict-pill ${isSpam ? "pill-spam" : "pill-normal"}" style="font-size: 0.85rem; padding: 0.3rem 0.8rem;">
          ${item.prediction} &bull; ${item.confidence.toFixed(1)}% Confidence
        </span>
        <span style="font-size: 0.85rem; color: var(--text-muted); margin-left: 0.75rem;">
          Analyzed: ${formatDate(item.created_at)}
        </span>
      </div>

      <div style="margin-bottom: 1.25rem;">
        <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">Full Message:</h4>
        <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 1rem; font-size: 0.95rem; white-space: pre-wrap; word-break: break-word;">
          ${escapeHtml(item.message)}
        </div>
      </div>

      <div style="margin-bottom: 1.25rem;">
        <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">Reasons:</h4>
        <ul class="reasons-list">
          ${(item.reasons || []).map(r => `<li>${escapeHtml(r)}</li>`).join("")}
        </ul>
      </div>

      ${item.links_found && item.links_found.length > 0 ? `
        <div style="margin-bottom: 1.25rem;">
          <h4 style="font-size: 0.9rem; color: var(--text-muted); text-transform: uppercase; margin-bottom: 0.4rem;">Links Detected:</h4>
          <ul class="links-list">
            ${item.links_found.map(l => `
              <li class="link-item">
                <span class="link-url">${escapeHtml(l.url)}</span>
                <span class="risk-badge risk-${l.risk_level}">${l.risk_level} risk</span>
              </li>
            `).join("")}
          </ul>
        </div>
      ` : ""}

      <div style="display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem;">
        <button type="button" class="btn btn-secondary" id="btnCopyFromModal">Copy Text</button>
        <button type="button" class="btn btn-primary" id="btnLoadInScanner">Load in Scanner</button>
      </div>
    `;

    document.getElementById("btnCopyFromModal").addEventListener("click", () => {
      navigator.clipboard.writeText(item.message);
      showToast("Message copied to clipboard!");
    });

    document.getElementById("btnLoadInScanner").addEventListener("click", () => {
      messageInput.value = item.message;
      updateCounters();
      historyModal.classList.remove("show");
      document.getElementById("detector").scrollIntoView({ behavior: "smooth" });
      showToast("Loaded message into detection scanner.");
    });

    historyModal.classList.add("show");
  }

  btnCloseHistoryModal.addEventListener("click", () => {
    historyModal.classList.remove("show");
  });

  // =========================================================================
  // 6. ML Model Evaluation Report Modal
  // =========================================================================
  btnViewModelReport.addEventListener("click", async () => {
    modelModal.classList.add("show");
    modelModalBody.innerHTML = "<p>Fetching real-time model evaluation metrics...</p>";

    try {
      const res = await fetch("/api/model-info");
      const data = await res.json();
      if (!data.success) {
        modelModalBody.innerHTML = `<p style="color: var(--spam-red);">Error: ${data.error}</p>`;
        return;
      }

      const m = data.metrics;
      modelModalBody.innerHTML = `
        <div style="margin-bottom: 1.5rem;">
          <div style="font-size: 0.85rem; color: var(--accent-cyan); font-weight: 700; text-transform: uppercase;">Architecture Details</div>
          <h4 style="font-size: 1.2rem; font-weight: 700; margin-bottom: 0.35rem;">${m.model_name}</h4>
          <p style="font-size: 0.9rem; color: var(--text-secondary);">${m.algorithm} with ${m.vectorizer}</p>
        </div>

        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; margin-bottom: 1.5rem;">
          <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem; text-align: center;">
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--normal-green); font-family: var(--font-mono);">${(m.accuracy * 100).toFixed(1)}%</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Accuracy</div>
          </div>
          <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem; text-align: center;">
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--accent-cyan); font-family: var(--font-mono);">${(m.precision * 100).toFixed(1)}%</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Precision</div>
          </div>
          <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem; text-align: center;">
            <div style="font-size: 1.35rem; font-weight: 800; color: var(--accent-blue); font-family: var(--font-mono);">${(m.recall * 100).toFixed(1)}%</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Recall</div>
          </div>
          <div style="background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); padding: 0.85rem; text-align: center;">
            <div style="font-size: 1.35rem; font-weight: 800; color: #a855f7; font-family: var(--font-mono);">${(m.f1_score * 100).toFixed(1)}%</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">F1-Score</div>
          </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.6rem;">Held-Out Test Set Confusion Matrix</h4>
          <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 0.88rem;">
            <thead>
              <tr style="border-bottom: 1px solid var(--border-color); color: var(--text-muted);">
                <th style="padding: 0.5rem; text-align: left;">Actual \\ Predicted</th>
                <th style="padding: 0.5rem;">Predicted Normal</th>
                <th style="padding: 0.5rem;">Predicted Spam</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom: 1px dashed var(--border-color);">
                <td style="padding: 0.6rem 0.5rem; text-align: left; font-weight: 600;">Actual Normal</td>
                <td style="padding: 0.6rem; color: var(--normal-green); font-weight: 700;">${m.confusion_matrix.tn} (TN)</td>
                <td style="padding: 0.6rem; color: var(--spam-red);">${m.confusion_matrix.fp} (FP)</td>
              </tr>
              <tr>
                <td style="padding: 0.6rem 0.5rem; text-align: left; font-weight: 600;">Actual Spam</td>
                <td style="padding: 0.6rem; color: var(--spam-red);">${m.confusion_matrix.fn} (FN)</td>
                <td style="padding: 0.6rem; color: var(--normal-green); font-weight: 700;">${m.confusion_matrix.tp} (TP)</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div style="margin-bottom: 1rem;">
          <h4 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.6rem;">Top Spam-Indicative Vocabulary Weights</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 0.4rem;">
            ${(m.top_spam_indicators || []).map(item => `
              <span style="background: var(--spam-bg); border: 1px solid rgba(239, 68, 68, 0.3); color: var(--spam-red); padding: 0.2rem 0.6rem; border-radius: var(--radius-full); font-size: 0.8rem; font-family: var(--font-mono);">
                ${item.word} (+${item.weight})
              </span>
            `).join("")}
          </div>
        </div>
      `;
    } catch (err) {
      modelModalBody.innerHTML = "<p style='color: var(--spam-red);'>Failed to load model evaluation metrics.</p>";
    }
  });

  btnCloseModelModal.addEventListener("click", () => {
    modelModal.classList.remove("show");
  });

  // Close modals on backdrop click
  window.addEventListener("click", (e) => {
    if (e.target === modelModal) modelModal.classList.remove("show");
    if (e.target === historyModal) historyModal.classList.remove("show");
  });

  // =========================================================================
  // 7. Contact Form Handling
  // =========================================================================
  contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("contactName").value.trim();
    const email = document.getElementById("contactEmail").value.trim();
    const subject = document.getElementById("contactSubject").value.trim();
    const message = document.getElementById("contactMessage").value.trim();

    if (!name || !email || !message) {
      showToast("Please fill in all required contact fields.", "error");
      return;
    }

    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, subject, message })
      });
      const data = await res.json();
      if (data.success) {
        showToast("Message sent successfully! Thank you for your feedback.");
        contactForm.reset();
      } else {
        showToast(data.error || "Failed to send message.", "error");
      }
    } catch (err) {
      showToast("Network error submitting feedback.", "error");
    }
  });

  // =========================================================================
  // 8. Stats & System Health Status
  // =========================================================================
  async function loadStats() {
    try {
      const res = await fetch("/api/stats");
      const data = await res.json();
      if (data.success && data.stats) {
        const total = data.stats.total_analyzed || 0;
        document.getElementById("statTotalAnalyzed").textContent = total.toLocaleString();
      }
    } catch (e) {}
  }

  async function checkHealth() {
    try {
      const res = await fetch("/api/health");
      const data = await res.json();
      if (data.status === "healthy") {
        statusText.textContent = "Model Ready";
        statusPill.style.borderColor = "rgba(16, 185, 129, 0.4)";
      }
    } catch (e) {
      statusText.textContent = "Offline Mode";
      statusPill.style.color = "var(--warning-amber)";
      statusPill.style.borderColor = "rgba(245, 158, 11, 0.4)";
    }
  }

  // =========================================================================
  // 9. Toast Notification Utility
  // =========================================================================
  let toastTimer = null;
  function showToast(msg, type = "success") {
    const toast = document.getElementById("toastNotification");
    const toastIcon = document.getElementById("toastIcon");
    const toastMessage = document.getElementById("toastMessage");

    toastIcon.textContent = type === "success" ? "✓" : "⚠️";
    toastMessage.textContent = msg;

    toast.className = `toast show ${type === "success" ? "toast-success" : "toast-error"}`;

    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove("show");
    }, 3200);
  }

  // Helper: Escape HTML
  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Helper: Format Date
  function formatDate(isoStr) {
    if (!isoStr) return "Just now";
    try {
      const d = new Date(isoStr.replace(" ", "T") + "Z");
      return d.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    } catch (e) {
      return isoStr;
    }
  }

  // Initialize
  checkHealth();
  loadStats();
  loadHistory();
});
