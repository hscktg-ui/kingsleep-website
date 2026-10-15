const HAS_DATA = typeof KING_SLEEP_DATA !== "undefined";
const REDUCED_MOTION = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initMenu();
  initBannerRotate();
  initPurchaseNotice();
  initProductGrid();
  initLineupPage();
  initProductPage();
  initInfoTabs();
  initSmartstoreLinks();
});

function initHeader() {
  const header = document.querySelector(".header");
  if (!header) return;
  const update = () => header.classList.toggle("scrolled", window.scrollY > 20);
  window.addEventListener("scroll", update, { passive: true });
  update();
}

function initMenu() {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");
  if (!toggle || !nav) return;

  const setOpen = (open) => {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "메뉴 닫기" : "메뉴 열기");
  };

  toggle.addEventListener("click", () => setOpen(!nav.classList.contains("open")));
  nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav.classList.contains("open")) {
      setOpen(false);
      toggle.focus();
    }
  });
}

function initSmartstoreLinks() {
  if (!HAS_DATA) return;
  document.querySelectorAll("[data-smartstore]").forEach((el) => {
    el.href = KING_SLEEP_DATA.smartstoreUrl;
    el.target = "_blank";
    el.rel = "noopener";
  });
}

function initBannerRotate() {
  const banner = document.querySelector(".top-banner__rotate");
  const messages = HAS_DATA ? KING_SLEEP_DATA.bannerMessages : [];
  if (!banner || messages.length < 2 || REDUCED_MOTION) return;
  let idx = 0;
  setInterval(() => {
    if (document.hidden) return;
    idx = (idx + 1) % messages.length;
    banner.style.opacity = "0";
    setTimeout(() => {
      banner.textContent = messages[idx];
      banner.style.opacity = "1";
    }, 300);
  }, 5000);
}

function initPurchaseNotice() {
  if (!HAS_DATA) return;
  document.querySelectorAll("[data-purchase-notice]").forEach((el) => {
    el.textContent = KING_SLEEP_DATA.purchaseNotice;
  });
}

function categoryLabel(cat) {
  return { mattress: "매트리스", bedding: "베딩", headboard: "헤드보드" }[cat] || cat;
}

function specList(p) {
  return p.spec.split(" · ");
}

function initProductGrid() {
  const grid = document.getElementById("product-grid");
  if (!grid || !HAS_DATA) return;

  let activeTab = "all";
  let activeCategory = "all";
  const tabs = document.querySelectorAll(".collection-tab");
  const filters = document.querySelectorAll(".category-filter");

  function render() {
    const items = KING_SLEEP_DATA.products.filter((p) =>
      (activeTab === "all" || p.tab === activeTab) && (activeCategory === "all" || p.category === activeCategory));

    grid.innerHTML = items.length ? items.map((p) => `
      <article class="catalog-card">
        <a href="${p.link}" class="catalog-card__image-wrap" aria-label="${p.nameFull} 상세 보기">
          ${p.badge ? `<span class="product-card__badge">${p.badge}</span>` : ""}
          <img src="${p.image}" alt="${p.nameFull}" loading="eager" decoding="async">
          <span class="catalog-card__hover" aria-hidden="true">
            <span class="catalog-card__hover-spec">${specList(p).join("<br>")}</span>
            <span class="catalog-card__hover-cta">상세 보기 →</span>
          </span>
        </a>
        <div class="catalog-card__body">
          <span class="catalog-card__category">${categoryLabel(p.category)}</span>
          <h3 class="catalog-card__name"><a href="${p.link}">${p.name}</a></h3>
          <p class="catalog-card__tagline">${p.tagline}</p>
          <p class="catalog-card__desc">${p.description}</p>
          <p class="catalog-card__spec">${p.spec}</p>
          <div class="catalog-card__actions">
            <a href="${p.link}" class="btn-outline">제품 상세 보기</a>
            <a href="${KING_SLEEP_DATA.smartstoreUrl}" class="catalog-card__store" data-smartstore target="_blank" rel="noopener">스마트스토어 구매 →</a>
          </div>
        </div>
      </article>
    `).join("") : `<p class="catalog-empty">조건에 맞는 제품이 없습니다. 다른 분류를 선택해 주세요.</p>`;
  }

  const bind = (buttons, key, setter) => buttons.forEach((btn) => {
    btn.setAttribute("aria-pressed", btn.classList.contains("active") ? "true" : "false");
    btn.addEventListener("click", () => {
      buttons.forEach((b) => { b.classList.remove("active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      setter(btn.dataset[key]);
      render();
      initSmartstoreLinks();
    });
  });
  bind(tabs, "tab", (v) => { activeTab = v; });
  bind(filters, "category", (v) => { activeCategory = v; });
  render();
}

function initLineupPage() {
  const wrap = document.getElementById("lineup-sections");
  if (!wrap || !HAS_DATA) return;

  const groups = [
    { key: "mattress", title: "MATTRESS", subtitle: "매트리스 라인업" },
    { key: "bedding", title: "BEDDING", subtitle: "베딩 라인업" },
    { key: "headboard", title: "HEADBOARD", subtitle: "헤드보드 라인업" },
  ];

  wrap.innerHTML = groups.map((g) => {
    const items = KING_SLEEP_DATA.products.filter((p) => p.category === g.key);
    if (!items.length) return "";
    return `
      <section class="lineup-section" id="lineup-${g.key}" aria-labelledby="lineup-${g.key}-title">
        <div class="lineup-section__header">
          <h2 id="lineup-${g.key}-title" lang="en">${g.title}</h2>
          <p>${g.subtitle}</p>
        </div>
        <div class="lineup-section__grid">
          ${items.map((p) => `
            <a href="${p.link}" class="lineup-card">
              <span class="lineup-card__image">
                <img src="${p.image}" alt="${p.nameFull}" decoding="async">
                <span class="lineup-card__hover" aria-hidden="true">${specList(p).join("<br>")}</span>
              </span>
              <span class="lineup-card__body">
                <span class="lineup-card__name">${p.name}</span>
                <span class="lineup-card__tagline">${p.tagline}</span>
                <span class="lineup-card__cta">자세히 보기 →</span>
              </span>
            </a>
          `).join("")}
        </div>
      </section>`;
  }).join("");

  if (location.hash) document.querySelector(location.hash)?.scrollIntoView();
}

function setMeta(selector, attr, value) {
  let el = document.head.querySelector(selector);
  if (!el) {
    el = document.createElement(selector.startsWith("link") ? "link" : "meta");
    const m = selector.match(/\[(\w+(?::\w+)?)="([^"]+)"\]/);
    if (m) el.setAttribute(m[1], m[2]);
    document.head.appendChild(el);
  }
  el.setAttribute(attr, value);
}

function initProductPage() {
  if (!HAS_DATA || !document.querySelector(".product-detail--catalog")) return;

  const product = getProduct(new URLSearchParams(location.search).get("id"));
  const url = `${KING_SLEEP_DATA.siteUrl}/product.html?id=${product.id}`;
  const title = `${product.nameFull} | 킹슬립 KING SLEEP`;
  const desc = `${product.nameFull} — ${product.tagline}. ${product.spec}. 가격·옵션은 네이버 스마트스토어에서 확인하세요.`;

  document.title = title;
  setMeta('meta[name="description"]', "content", desc);
  setMeta('link[rel="canonical"]', "href", url);
  setMeta('meta[property="og:title"]', "content", title);
  setMeta('meta[property="og:description"]', "content", desc);
  setMeta('meta[property="og:url"]', "content", url);
  setMeta('meta[name="twitter:title"]', "content", title);
  setMeta('meta[name="twitter:description"]', "content", desc);

  const setText = (sel, text) => {
    const el = document.querySelector(sel);
    if (el && text) el.textContent = text;
  };
  setText(".product-hero__category", categoryLabel(product.category));
  setText(".product-hero__title", product.name);
  setText(".product-hero__tagline", product.tagline);
  setText(".product-hero__desc", product.description);
  setText(".product-sidebar__category", categoryLabel(product.category));
  setText(".product-sidebar__title", product.nameFull);
  setText(".product-crumb__current", product.nameFull);

  const highlights = document.getElementById("product-highlights");
  if (highlights) highlights.innerHTML = specList(product).map((s) => `<li>${s}</li>`).join("");

  const gallery = product.gallery || [product.image];
  const mainImg = document.querySelector(".product-gallery__main img");
  if (mainImg) {
    mainImg.src = gallery[0];
    mainImg.alt = product.nameFull;
  }
  const thumbs = document.querySelector(".product-gallery__thumbs");
  if (thumbs) {
    thumbs.innerHTML = gallery.length > 1 ? gallery.map((src, i) => `
      <button type="button" class="product-gallery__thumb${i === 0 ? " active" : ""}" aria-label="${product.nameFull} 이미지 ${i + 1}" aria-pressed="${i === 0}">
        <img src="${src}" alt="">
      </button>`).join("") : "";
    thumbs.closest(".product-gallery")?.classList.toggle("product-gallery--single", gallery.length < 2);
    thumbs.querySelectorAll(".product-gallery__thumb").forEach((btn, i) => btn.addEventListener("click", () => {
      mainImg.src = gallery[i];
      thumbs.querySelectorAll(".product-gallery__thumb").forEach((b) => { b.classList.remove("active"); b.setAttribute("aria-pressed", "false"); });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
    }));
  }

  const metricsWrap = document.getElementById("product-tech-metrics");
  if (metricsWrap && product.techMetrics?.length) {
    metricsWrap.innerHTML = product.techMetrics.map((m) => `
      <div class="tech-metric">
        <span class="tech-metric__value">${m.value}</span>
        <span class="tech-metric__label">${m.label}</span>
      </div>`).join("");
  } else {
    metricsWrap?.closest(".tech-metrics")?.remove();
  }

  const techWrap = document.getElementById("product-technologies");
  if (techWrap && product.technologies) {
    techWrap.innerHTML = product.technologies.map((t) => `
      <div class="tech-block">
        <h3 lang="en">${t.title}</h3>
        <p>${t.desc}</p>
      </div>`).join("");
  }

  const layersWrap = document.getElementById("product-layers");
  if (layersWrap && product.layers?.length) {
    layersWrap.innerHTML = product.layers.map((l) => `<div class="tech-layer"><span>${l.name}</span><span>${l.value}</span></div>`).join("");
  } else {
    layersWrap?.closest(".tech-viz")?.remove();
  }

  const matWrap = document.getElementById("product-materials");
  if (matWrap && product.materials) matWrap.innerHTML = product.materials.map((m) => `<li>${m}</li>`).join("");

  const sizeWrap = document.getElementById("product-sizes");
  if (sizeWrap && product.sizes) {
    sizeWrap.innerHTML = `
      <table class="spec-table">
        <caption class="visually-hidden">${product.nameFull} 사이즈</caption>
        <thead><tr><th scope="col">사이즈</th><th scope="col">가로</th><th scope="col">세로</th><th scope="col">높이</th></tr></thead>
        <tbody>
          ${product.sizes.map((s) => `<tr><th scope="row">${s.name}</th><td>${s.width}</td><td>${s.length}</td><td>${s.height}</td></tr>`).join("")}
        </tbody>
      </table>
      <p class="spec-note">※ 사이즈·구성은 제품별로 다를 수 있습니다. 구매 전 스마트스토어 상세 페이지를 확인해 주세요.</p>`;
  }
}

function initInfoTabs() {
  const tabs = [...document.querySelectorAll(".product-info__tab")];
  if (!tabs.length) return;
  const select = (tab) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.classList.toggle("active", on);
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
    });
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener("click", () => select(tab));
    tab.addEventListener("keydown", (e) => {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      const next = tabs[(i + (e.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length];
      select(next);
      next.focus();
    });
  });
}
