document.addEventListener("DOMContentLoaded", () => {
  function parseNumberFromText(text) {
    if (!text) return 0;
    const normalized = String(text)
      .replace(/\u2212/g, "-")
      .replace(",", ".");
    const cleaned = normalized.replace(/[^0-9.\-]/g, "");
    const n = parseFloat(cleaned);
    return isNaN(n) ? 0 : n;
  }

  function isVisible(el) {
    return el && el.getClientRects && el.getClientRects().length > 0;
  }

  function recalcTotals() {
    let totalSpent = 0;
    let totalAdded = 0;
    let detectedCurrency = null;
    let visibleRows = 0;

    document.querySelectorAll("#history-body tr").forEach((row) => {
      if (!isVisible(row)) return;
      visibleRows++;

      const spentEl = row.querySelector(".spent");
      const addedEl = row.querySelector(".added");

      if (spentEl) {
        const v = parseNumberFromText(spentEl.textContent);
        totalSpent += Math.abs(v);
        if (!detectedCurrency) {
          const m = spentEl.textContent.match(/([A-Za-zА-Яа-я₽$€]+)/);
          if (m) detectedCurrency = m[0];
        }
      }

      if (addedEl) {
        const v = parseNumberFromText(addedEl.textContent);
        totalAdded += Math.abs(v);
        if (!detectedCurrency) {
          const m = addedEl.textContent.match(/([A-Za-zА-Яа-я₽$€]+)/);
          if (m) detectedCurrency = m[0];
        }
      }
    });

    const currencyStr = detectedCurrency ? " " + detectedCurrency : " RUB";
    const spentTd = document.getElementById("total-spent");
    const addedTd = document.getElementById("total-added");
    if (spentTd)
      spentTd.textContent = visibleRows
        ? "-" + totalSpent.toFixed(2) + currencyStr
        : "—";
    if (addedTd)
      addedTd.textContent = visibleRows
        ? "+" + totalAdded.toFixed(2) + currencyStr
        : "—";
  }

  recalcTotals();

  const tbody = document.getElementById("history-body");
  if (tbody) {
    const mo = new MutationObserver(() => recalcTotals());
    mo.observe(tbody, {
      childList: true,
      subtree: true,
      attributes: true,
      characterData: true,
    });
  }

  document
    .querySelectorAll(
      ".platform-option, #selectAllPlatforms, #platformsOkBtn, #filterPeriod"
    )
    .forEach((el) => {
      el.addEventListener("change", () => setTimeout(recalcTotals, 60));
      el.addEventListener("click", () => setTimeout(recalcTotals, 60));
    });

  if (window.jQuery && jQuery.fn && jQuery.fn.dataTable) {
    try {
      jQuery("table").on("draw.dt", () => recalcTotals());
    } catch (e) {}
  }
});
