document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".header");
  const menuToggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".nav");

  window.addEventListener("scroll", () => {
    header?.classList.toggle("scrolled", window.scrollY > 20);
  }, { passive: true });

  menuToggle?.addEventListener("click", () => {
    const open = nav?.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && nav?.classList.contains("open")) {
      nav.classList.remove("open");
      menuToggle?.setAttribute("aria-expanded", "false");
      menuToggle?.focus();
    }
  });

  document.querySelectorAll(".product-info__tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const panel = tab.dataset.panel;
      document.querySelectorAll(".product-info__tab").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      document.querySelectorAll(".product-info__panel").forEach((p) => {
        p.hidden = p.dataset.panel !== panel;
      });
    });
  });

  document.querySelectorAll(".product-gallery__thumb").forEach((thumb) => {
    thumb.addEventListener("click", () => {
      const main = document.querySelector(".product-gallery__main img");
      const src = thumb.querySelector("img")?.src;
      if (main && src) {
        main.src = src;
        document.querySelectorAll(".product-gallery__thumb").forEach((t) => t.classList.remove("active"));
        thumb.classList.add("active");
      }
    });
  });

  initSmartstoreLinks();
  initBannerRotate();
  initProductGrid();
  initLineupPage();
  initReviews();
  initFamilyCases();
  initStylingGallery();
  initBrandTimeline();
  initStores();
  initArticles();
  initProductPage();
});

function initBannerRotate() {
  const banner = document.querySelector(".top-banner__rotate");
  if (!banner || typeof KING_SLEEP_DATA === "undefined" || !KING_SLEEP_DATA.bannerMessages?.length) return;
  let idx = 0;
  banner.textContent = KING_SLEEP_DATA.bannerMessages[0];
  setInterval(() => {
    idx = (idx + 1) % KING_SLEEP_DATA.bannerMessages.length;
    banner.style.opacity = "0";
    setTimeout(() => {
      banner.textContent = KING_SLEEP_DATA.bannerMessages[idx];
      banner.style.opacity = "1";
    }, 300);
  }, 5000);
}

function initSmartstoreLinks() {
  const url = getSmartstoreUrl();
  document.querySelectorAll("[data-smartstore]").forEach((el) => {
    el.href = url;
    el.target = "_blank";
    el.rel = "noopener";
  });
}

function categoryLabel(cat) {
  return { mattress: "매트리스", bedding: "베딩", headboard: "헤드보드" }[cat] || cat;
}

function initProductGrid() {
  const grid = document.getElementById("product-grid");
  if (!grid || typeof KING_SLEEP_DATA === "undefined") return;

  let activeTab = "all";
  let activeCategory = "all";

  const tabs = document.querySelectorAll(".collection-tab");
  const filters = document.querySelectorAll(".category-filter");

  function render() {
    const items = KING_SLEEP_DATA.products.filter((p) => {
      const tabOk = activeTab === "all" || p.tab === activeTab;
      const catOk = activeCategory === "all" || p.category === activeCategory;
      return tabOk && catOk;
    });

    grid.innerHTML = items.map((p) => `
      <article class="catalog-card">
        <a href="${p.link}" class="catalog-card__image-wrap">
          ${p.badge ? `<span class="product-card__badge">${p.badge}</span>` : ""}
          <img src="${p.image}" alt="${p.nameFull}" loading="eager">
          <div class="catalog-card__hover">
            <span class="catalog-card__hover-price">${p.referencePrice}</span>
            <span class="catalog-card__hover-spec">${p.spec}</span>
            <span class="catalog-card__hover-rating">★ ${p.rating} · 리뷰 ${p.reviews}건</span>
            <span class="catalog-card__hover-cta">상세 보기 →</span>
          </div>
        </a>
        <div class="catalog-card__body">
          <span class="catalog-card__category">${categoryLabel(p.category)}</span>
          <h3 class="catalog-card__name"><a href="${p.link}">${p.name}</a></h3>
          <p class="catalog-card__tagline">${p.tagline}</p>
          <p class="catalog-card__desc">${p.description}</p>
          <div class="catalog-card__actions">
            <a href="${p.link}" class="btn-outline">제품 상세 보기</a>
            <a href="${getSmartstoreUrl()}" class="catalog-card__store" data-smartstore target="_blank" rel="noopener">스마트스토어 구매 →</a>
          </div>
        </div>
      </article>
    `).join("");

    initSmartstoreLinks();
  }

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      activeTab = tab.dataset.tab;
      render();
    });
  });

  filters.forEach((f) => {
    f.addEventListener("click", () => {
      filters.forEach((x) => x.classList.remove("active"));
      f.classList.add("active");
      activeCategory = f.dataset.category;
      render();
    });
  });

  render();
}

function initLineupPage() {
  const wrap = document.getElementById("lineup-sections");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  const groups = [
    { key: "mattress", title: "MATTRESS", subtitle: "매트리스 라인업" },
    { key: "bedding", title: "BEDDING", subtitle: "베딩 라인업" },
    { key: "headboard", title: "HEADBOARD", subtitle: "헤드보드 라인업" },
  ];

  wrap.innerHTML = groups.map((g) => {
    const items = KING_SLEEP_DATA.products.filter((p) => p.category === g.key);
    if (!items.length) return "";
    return `
      <section class="lineup-section" id="lineup-${g.key}">
        <div class="lineup-section__header">
          <h2>${g.title}</h2>
          <p>${g.subtitle}</p>
        </div>
        <div class="lineup-section__grid">
          ${items.map((p) => `
            <a href="${p.link}" class="lineup-card">
              <div class="lineup-card__image">
                <img src="${p.image}" alt="${p.nameFull}">
                <div class="lineup-card__hover">
                  <span>${p.referencePrice}</span>
                  <span>★ ${p.rating} · ${p.reviews}건</span>
                </div>
              </div>
              <div class="lineup-card__body">
                <h3>${p.name}</h3>
                <p>${p.tagline}</p>
                <span class="lineup-card__cta">자세히 보기 →</span>
              </div>
            </a>
          `).join("")}
        </div>
      </section>`;
  }).join("");
}

function initFamilyCases() {
  const wrap = document.getElementById("family-cases-grid");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.familyCases.map((c) => `
    <article class="family-case">
      <a href="${c.link}" class="family-case__image">
        <img src="${c.image}" alt="${c.title}">
        <span class="family-case__persona">${c.persona}</span>
      </a>
      <div class="family-case__body">
        <h3>${c.title}</h3>
        <p>${c.text}</p>
        <span class="family-case__product">${c.product}</span>
      </div>
    </article>
  `).join("");
}

function initStylingGallery() {
  const wrap = document.getElementById("styling-gallery");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.stylingGallery.map((s) => `
    <a href="${s.link}" class="styling-shot">
      <img src="${s.image}" alt="${s.title}">
      <div class="styling-shot__overlay">
        <span class="styling-shot__tag">${s.tag}</span>
        <span class="styling-shot__title">${s.title}</span>
      </div>
    </a>
  `).join("");
}

function initBrandTimeline() {
  const wrap = document.getElementById("brand-timeline");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.brandMilestones.map((m) => `
    <div class="timeline-item">
      <div class="timeline-item__year">${m.year}</div>
      <h3>${m.title}</h3>
      <p>${m.desc}</p>
    </div>
  `).join("");
}

function initReviews() {
  const wrap = document.getElementById("reviews-grid");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.reviews.map((r) => `
    <article class="review-card">
      <div class="review-card__stars">${"★".repeat(r.rating)}</div>
      <h3 class="review-card__title">${r.title}</h3>
      <p class="review-card__text">${r.text}</p>
      <p class="review-card__meta">${r.author} · ${r.product}</p>
    </article>
  `).join("");
}

function initStores() {
  const wrap = document.getElementById("stores-grid");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.stores.map((s) => `
    <div class="store-card">
      <span class="store-card__type">${s.type}</span>
      <h3 class="store-card__name">${s.name}</h3>
      <p class="store-card__addr">${s.address}</p>
      <p class="store-card__hours">${s.hours}</p>
      <div class="store-card__actions">
        <a href="tel:${s.tel.replace(/-/g, "")}" class="store-card__tel">${s.tel}</a>
        <a href="tel:${s.tel.replace(/-/g, "")}" class="store-card__book">체험 예약</a>
      </div>
    </div>
  `).join("");
}

function initArticles() {
  const wrap = document.getElementById("articles-grid");
  if (!wrap || typeof KING_SLEEP_DATA === "undefined") return;

  wrap.innerHTML = KING_SLEEP_DATA.articles.map((a) => `
    <a href="${a.link}" class="article-card">
      <time class="article-card__date">${a.date}</time>
      <h3 class="article-card__title">${a.title}</h3>
      <p class="article-card__excerpt">${a.excerpt}</p>
      <span class="article-card__link">읽기 →</span>
    </a>
  `).join("");
}

function initProductPage() {
  if (typeof KING_SLEEP_DATA === "undefined") return;
  if (!document.querySelector(".product-detail--catalog")) return;

  const params = new URLSearchParams(location.search);
  const product = getProduct(params.get("id") || "royal-signature");

  document.title = `${product.nameFull} — KING SLEEP`;

  const setText = (sel, text) => {
    const el = document.querySelector(sel);
    if (el && text) el.textContent = text;
  };

  setText(".product-hero__category", categoryLabel(product.category));
  setText(".product-hero__title", product.name);
  setText(".product-hero__tagline", product.tagline);
  setText(".product-hero__desc", product.description);
  setText(".product-sidebar__title", product.nameFull);
  setText(".product-sidebar__ref-price", `참고가 ${product.referencePrice}`);

  const installment = document.getElementById("installment-note");
  if (installment) installment.textContent = KING_SLEEP_DATA.installmentNote;

  const reviewMeta = document.getElementById("product-review-meta");
  if (reviewMeta) reviewMeta.textContent = `★ ${product.rating} · 구매 리뷰 ${product.reviews}건`;

  const metricsWrap = document.getElementById("product-tech-metrics");
  if (metricsWrap && product.techMetrics?.length) {
    metricsWrap.innerHTML = product.techMetrics.map((m) => `
      <div class="tech-metric">
        <span class="tech-metric__value">${m.value}</span>
        <span class="tech-metric__label">${m.label}</span>
      </div>
    `).join("");
  } else if (metricsWrap) {
    metricsWrap.closest(".tech-metrics")?.remove();
  }

  const mainImg = document.querySelector(".product-gallery__main img");
  if (mainImg) {
    mainImg.src = product.image;
    mainImg.alt = product.nameFull;
  }

  const techWrap = document.getElementById("product-technologies");
  if (techWrap && product.technologies) {
    techWrap.innerHTML = product.technologies.map((t) => `
      <div class="tech-block">
        <h3>${t.title}</h3>
        <p>${t.desc}</p>
      </div>
    `).join("");
  }

  const matWrap = document.getElementById("product-materials");
  if (matWrap && product.materials) {
    matWrap.innerHTML = product.materials.map((m) => `<li>${m}</li>`).join("");
  }

  const sizeWrap = document.getElementById("product-sizes");
  if (sizeWrap && product.sizes) {
    sizeWrap.innerHTML = `
      <table class="spec-table">
        <thead><tr><th>사이즈</th><th>가로</th><th>세로</th><th>높이</th></tr></thead>
        <tbody>
          ${product.sizes.map((s) => `
            <tr><td>${s.name}</td><td>${s.width}</td><td>${s.length}</td><td>${s.height}</td></tr>
          `).join("")}
        </tbody>
      </table>
      <p class="spec-note">※ 사이즈·구성은 제품별 상이합니다. 구매 전 스마트스토어 상세 페이지를 확인해 주세요.</p>`;
  }

  const notice = document.getElementById("purchase-notice");
  if (notice) notice.textContent = KING_SLEEP_DATA.purchaseNotice;
}
