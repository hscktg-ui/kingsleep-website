const KING_SLEEP_DATA = {
  siteUrl: "https://kingsleep.co.kr",
  smartstoreUrl: "https://smartstore.naver.com/kingsleep",
  purchaseNotice: "본 사이트는 제품 안내용입니다. 가격 확인·구매·결제는 네이버 스마트스토어에서 진행됩니다.",

  // 사업자등록증(2026-10-13 발급) 기준. 바꿀 때는 각 HTML 푸터도 함께 수정하고 scripts/predeploy-check.py를 돌린다.
  company: {
    name: "킹슬립(KING SLEEP)",
    ceo: "강경육",
    bizNumber: "106-29-52393",
    address: "경기도 시흥시 매화산단3길 1, 317호(매화동, 리드스마트스퀘어)",
  },
  contact: {
    phone: "031-573-9171",
    tel: "0315739171",
  },

  bannerMessages: [
    "제품 안내 사이트 · 구매는 네이버 스마트스토어",
    "국내 제작 매트리스 · 전문 기사 배송·설치",
    "전문 상담 031-573-9171",
  ],

  products: [
    {
      id: "royal-signature",
      name: "로얄 시그니처",
      nameFull: "로얄 시그니처 매트리스",
      category: "mattress",
      tab: "pick",
      badge: "추천",
      tagline: "프리미엄 수면의 새로운 기준",
      description: "7존 독립 포켓스프링과 메모리폼·라텍스 레이어가 만나 깊고 편안한 휴식을 완성합니다.",
      spec: "30cm · 7존 독립스프링 · 메모리폼 + 라텍스",
      image: "assets/images/mattress-royal.jpg",
      gallery: ["assets/images/mattress-royal.jpg", "assets/images/mattress-detail.jpg", "assets/images/interior-navy.jpg"],
      link: "product.html?id=royal-signature",
      techMetrics: [
        { label: "스프링 수 (Q)", value: "1,020개" },
        { label: "폼 밀도", value: "45kg/m³" },
        { label: "총 높이", value: "30cm" },
      ],
      technologies: [
        { title: "7-Zone System", desc: "머리·어깨·허리·골반·다리별 체압을 분산하는 7존 독립 스프링 구조" },
        { title: "Deep Comfort Layer", desc: "메모리폼과 라텍스가 이중으로 감싸 체형에 맞는 맞춤 지지" },
        { title: "Royal Quilt Cover", desc: "부드러운 촉감의 퀼팅 커버 원단" },
      ],
      layers: [
        { name: "퀼팅 커버", value: "커버 원단" },
        { name: "메모리폼", value: "5cm" },
        { name: "라텍스", value: "3cm" },
        { name: "7존 포켓스프링", value: "18cm" },
      ],
      materials: ["퀼팅 원단", "쿨링 메모리폼", "천연 라텍스", "7존 포켓스프링"],
      sizes: [
        { name: "퀸 (Q)", width: "150cm", length: "200cm", height: "30cm" },
        { name: "킹 (K)", width: "180cm", length: "200cm", height: "30cm" },
        { name: "LK", width: "200cm", length: "220cm", height: "30cm" },
      ],
    },
    {
      id: "cloud-comfort",
      name: "클라우드 컴포트",
      nameFull: "클라우드 컴포트 매트리스",
      category: "mattress",
      tab: "pick",
      badge: null,
      tagline: "구름 위에 누운 듯한 포근함",
      description: "쿨링 젤 레이어와 포켓스프링이 만나 사계절 쾌적한 수면 환경을 제공합니다.",
      spec: "28cm · 포켓스프링 · 쿨링 젤 레이어",
      image: "assets/images/mattress-cloud.jpg",
      link: "product.html?id=cloud-comfort",
      techMetrics: [
        { label: "스프링 수 (Q)", value: "880개" },
        { label: "쿨링 젤 레이어", value: "3cm" },
        { label: "총 높이", value: "28cm" },
      ],
      technologies: [
        { title: "Cooling Gel Layer", desc: "체열을 분산해 여름에도 쾌적한 접촉면 유지" },
        { title: "Pocket Spring", desc: "독립 스프링이 파트너의 움직임 전달을 최소화" },
      ],
      materials: ["쿨링 젤 폼", "고탄성 폼", "포켓스프링"],
      sizes: [
        { name: "퀸 (Q)", width: "150cm", length: "200cm", height: "28cm" },
        { name: "킹 (K)", width: "180cm", length: "200cm", height: "28cm" },
      ],
    },
    {
      id: "hybrid-elite",
      name: "하이브리드 엘리트",
      nameFull: "하이브리드 엘리트 매트리스",
      category: "mattress",
      tab: "pick",
      badge: "추천",
      tagline: "듀얼 스프링의 완벽한 밸런스",
      description: "듀얼 스프링 시스템과 프리미엄 폼 레이어로 지지력과 편안함을 동시에 제공합니다.",
      spec: "32cm · 듀얼 스프링 · 라텍스 + 메모리폼",
      image: "assets/images/mattress-detail.jpg",
      link: "product.html?id=hybrid-elite",
      techMetrics: [
        { label: "듀얼 스프링", value: "1,240개" },
        { label: "라텍스 레이어", value: "4cm" },
        { label: "총 높이", value: "32cm" },
      ],
      technologies: [
        { title: "Dual Spring System", desc: "이중 스프링 구조로 반발력과 내구성을 강화" },
        { title: "Elite Comfort Stack", desc: "32cm 두께의 프리미엄 멀티 레이어" },
      ],
      materials: ["메모리폼", "라텍스", "듀얼 포켓스프링"],
      sizes: [
        { name: "퀸 (Q)", width: "150cm", length: "200cm", height: "32cm" },
        { name: "킹 (K)", width: "180cm", length: "200cm", height: "32cm" },
      ],
    },
    {
      id: "deep-sleep-set",
      name: "딥 슬립",
      nameFull: "딥 슬립 베딩 세트",
      category: "bedding",
      tab: "new",
      badge: "NEW",
      tagline: "피부에 닿는 순간의 차이",
      description: "100% 순면 이불·베개·커버 세트로 수면 환경을 완성합니다.",
      spec: "이불 + 베개 + 커버 · 100% 순면",
      image: "assets/images/bedding-deep.jpg",
      link: "product.html?id=deep-sleep-set",
      technologies: [
        { title: "Pure Cotton", desc: "통기성과 부드러움을 갖춘 100% 순면" },
      ],
      materials: ["100% 순면"],
      sizes: [{ name: "퀸 세트", width: "—", length: "—", height: "—" }],
    },
    {
      id: "royal-headboard",
      name: "로얄 벨벳",
      nameFull: "로얄 벨벳 헤드보드",
      category: "headboard",
      tab: "new",
      badge: null,
      tagline: "침실의 품격을 완성하는 포인트",
      description: "버튼 튜프팅 벨벳 헤드보드로 프리미엄 침실 무드를 연출합니다.",
      spec: "벨벳 · 버튼 튜프팅 · 퀸/킹",
      image: "assets/images/headboard-royal.jpg",
      link: "product.html?id=royal-headboard",
      technologies: [
        { title: "Button Tufting", desc: "클래식 체스터필드 스타일의 고급 마감" },
      ],
      materials: ["프리미엄 벨벳", "목재 프레임"],
      sizes: [
        { name: "퀸", width: "160cm", length: "120cm", height: "—" },
        { name: "킹", width: "190cm", length: "120cm", height: "—" },
      ],
    },
    {
      id: "cooling-pad",
      name: "로얄 쿨링",
      nameFull: "로얄 쿨링 패드",
      category: "bedding",
      tab: "new",
      badge: "NEW",
      tagline: "사계절 쾌적한 접촉면",
      description: "접촉면 쿨링 원단으로 더운 계절에도 편안한 수면을 돕습니다.",
      spec: "쿨링 원단 · 사계절 사용",
      image: "assets/images/collection-bedding.jpg",
      link: "product.html?id=cooling-pad",
      technologies: [{ title: "Cool Touch Fabric", desc: "피부에 닿을 때 시원한 촉감의 원단" }],
      materials: ["쿨링 폴리에스터"],
      sizes: [{ name: "퀸", width: "150cm", length: "200cm", height: "—" }],
    },
  ],
};

function getSmartstoreUrl() {
  return KING_SLEEP_DATA.smartstoreUrl;
}

function getProduct(id) {
  return KING_SLEEP_DATA.products.find((p) => p.id === id) || KING_SLEEP_DATA.products[0];
}
