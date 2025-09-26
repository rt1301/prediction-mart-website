// Utility: currency & percent formatters
const fmt = {
  money: (v, cur = "USD") => {
    const symbol = cur === "INR" ? "₹" : "$";
    return symbol + (v ?? 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  },
  percent: (v) => ((v ?? 0) * 100).toFixed(2) + "%"
};

// Sticky nav: mobile toggle
const menuBtn = document.getElementById("navMenuBtn");
const navLinks = document.querySelector(".nav__links");
if (menuBtn) {
  menuBtn.addEventListener("click", () => {
    if (!navLinks) return;
    const shown = getComputedStyle(navLinks).display !== "none";
    navLinks.style.display = shown ? "none" : "flex";
  });
}

// Smooth-ish scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener("click", (e) => {
    const id = a.getAttribute("href").substring(1);
    const target = document.getElementById(id);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});

// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// ---------- Payoff Calculator ----------
const priceInput = document.getElementById("priceInput");
const invInput = document.getElementById("investmentInput");
const feeInput = document.getElementById("feeInput");
const curSelect = document.getElementById("currencySelect");
const calcBtn = document.getElementById("calcBtn");
const resetBtn = document.getElementById("resetBtn");
const resultsEl = document.getElementById("calcResults");
const chartEl = document.getElementById("roiChart");

// Assumption: If currency is INR, we display by multiplying USD amounts by FX
const FX_RATE = 83.0; // display only; core math done in USD

function toUSD(amount, currency) {
  if (currency === "INR") return (amount ?? 0) / FX_RATE;
  return amount ?? 0;
}
function fromUSD(amountUSD, currency) {
  if (currency === "INR") return (amountUSD ?? 0) * FX_RATE;
  return amountUSD ?? 0;
}

function validate(price, investment, feePct) {
  const errors = [];
  if (!(price >= 0.01 && price <= 0.99)) errors.push("Price must be between 0.01 and 0.99.");
  if (!(investment > 0)) errors.push("Investment must be greater than 0.");
  if (!(feePct >= 0 && feePct <= 2)) errors.push("Fee % must be between 0 and 2.");
  return errors;
}

// Simple inline SVG chart (ROI vs. Price) around selected price
function renderChart(currentPrice, investmentUSD, fee) {
  const w = 520, h = 140, pad = 28;
  const prices = [];
  for (let p = Math.max(0.01, currentPrice - 0.15); p <= Math.min(0.99, currentPrice + 0.15); p += 0.01) {
    prices.push(+p.toFixed(2));
  }
  // ROI if correct at settlement (with fees both sides)
  const points = prices.map(p => {
    const shares = investmentUSD / (p || 1);
    const netPayout = shares * 1.0 * (1 - fee);
    const costTotal = investmentUSD * (1 + fee);
    const profit = netPayout - costTotal;
    const roi = profit / costTotal; // return on cost
    return { p, roi };
  });

  const minROI = Math.min(...points.map(d => d.roi));
  const maxROI = Math.max(...points.map(d => d.roi));

  const x = (p) => pad + ((p - prices[0]) / (prices[prices.length - 1] - prices[0])) * (w - 2 * pad);
  const y = (r) => h - pad - ((r - minROI) / (maxROI - minROI || 1)) * (h - 2 * pad);

  let poly = "";
  points.forEach((d, i) => {
    poly += (i ? " L " : "M ") + x(d.p).toFixed(1) + " " + y(d.roi).toFixed(1);
  });

  const axisY0 = y(0);

  chartEl.innerHTML = `
    <div class="muted small" style="margin-bottom:8px;">ROI vs. Price (assuming settlement “Yes” and fees applied on entry & exit)</div>
    <svg width="${w}" height="${h}" role="img" aria-label="ROI sparkline">
      <defs>
        <linearGradient id="grad" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="#4cc9f0" stop-opacity="0.9"/>
          <stop offset="100%" stop-color="#4cc9f0" stop-opacity="0.1"/>
        </linearGradient>
      </defs>
      <rect x="0" y="0" width="${w}" height="${h}" fill="rgba(255,255,255,.03)" rx="10"></rect>
      <line x1="${pad}" y1="${axisY0}" x2="${w-pad}" y2="${axisY0}" stroke="rgba(255,255,255,.2)" stroke-dasharray="4 4"/>
      <path d="${poly}" fill="none" stroke="#4cc9f0" stroke-width="2.2" />
      <circle cx="${x(currentPrice)}" cy="${y(points.find(d=>d.p===+currentPrice.toFixed(2))?.roi ?? points[Math.floor(points.length/2)].roi)}" r="4" fill="#8257e6" />
    </svg>
  `;
  chartEl.classList.remove("hidden");
}

function calculate() {
  const price = parseFloat(priceInput.value);
  const inv = parseFloat(invInput.value);
  const feePct = parseFloat(feeInput.value);
  const cur = curSelect.value;

  const errs = validate(price, inv, feePct);
  if (errs.length) {
    resultsEl.innerHTML = `<p style="color:#ffb4b4;"><b>Fix inputs:</b> ${errs.join(" ")}</p>`;
    resultsEl.classList.remove("hidden");
    chartEl.classList.add("hidden");
    return;
  }

  // Normalize to USD internally
  const investmentUSD = toUSD(inv, cur);
  const fee = feePct / 100;

  // Buy & hold to settlement (apply fee on entry and on payout)
  const shares = investmentUSD / price;
  const costTotal = investmentUSD * (1 + fee);
  const netPayoutIfYes = shares * (1.0) * (1 - fee);
  const profitIfYes = netPayoutIfYes - costTotal;
  const lossIfNo = -costTotal; // zero payout; entry fee already counted

  // Breakeven probability is simply price (ignoring fees). With fees, effective breakeven is a bit higher:
  const bePriceNoFees = price;
  const bePriceWithFees = (investmentUSD * (1 + fee)) / (shares * (1 - fee)); // algebra → needed price at payout to break even
  // Since settlement pays 1.0, bePriceWithFees is effectively the required payout per share; cap at 1 for display
  const beAdj = Math.min(1, bePriceWithFees);

  // Convert back for display
  const toDisp = (usd) => fmt.money(fromUSD(usd, cur), cur);

  resultsEl.innerHTML = `
    <p><b>Inputs:</b> Price = ${price.toFixed(2)}, Investment = ${fmt.money(inv, cur)}, Fees = ${feePct.toFixed(2)}% (each side)</p>
    <div class="table-wrap">
      <table class="table">
        <tbody>
          <tr><td>Shares Purchased</td><td><b>${shares.toFixed(2)}</b></td></tr>
          <tr><td>Max Payout if “Yes”</td><td><b>${toDisp(netPayoutIfYes)}</b></td></tr>
          <tr><td>Profit if Correct (after fees)</td><td style="color:${profitIfYes>=0?'#22c55e':'#ef4444'};"><b>${toDisp(profitIfYes)}</b></td></tr>
          <tr><td>Loss if Incorrect (after fees)</td><td style="color:#ef4444;"><b>${toDisp(lossIfNo)}</b></td></tr>
          <tr><td>Breakeven Probability (no fees)</td><td><b>${fmt.percent(bePriceNoFees)}</b></td></tr>
          <tr><td>Breakeven (with fees, effective)</td><td><b>${fmt.percent(beAdj)}</b></td></tr>
        </tbody>
      </table>
    </div>
    <p class="muted small">Assumption: fee% charged on buy and on payout/sale. Display currency conversion uses a fixed FX of ${FX_RATE.toFixed(1)} for INR; core math is in USD.</p>
  `;
  resultsEl.classList.remove("hidden");

  renderChart(price, investmentUSD, fee);
}

if (calcBtn) calcBtn.addEventListener("click", calculate);
if (resetBtn) resetBtn.addEventListener("click", () => {
  priceInput.value = "0.40";
  invInput.value = "100";
  feeInput.value = "0.5";
  curSelect.value = "USD";
  resultsEl.classList.add("hidden");
  chartEl.classList.add("hidden");
  resultsEl.innerHTML = "";
  chartEl.innerHTML = "";
});

// ---------- YouTube ID Apply ----------
const ytIdInput = document.getElementById("ytIdInput");
const ytApplyBtn = document.getElementById("ytApplyBtn");
const ytEmbed = document.getElementById("ytEmbed");

if (ytApplyBtn) {
  ytApplyBtn.addEventListener("click", () => {
    const id = (ytIdInput.value || "").trim();
    if (!id) return;
    ytEmbed.src = `https://www.youtube.com/embed/${encodeURIComponent(id)}`;
  });
}
