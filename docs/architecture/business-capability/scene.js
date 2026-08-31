const W = 1480, H = 1910;

const PLANES = {
  consumer: { c: '#94A3B8', label: 'Consumer integration' },
  identity: { c: '#7DD3FC', label: 'Identity authority' },
  reuse: { c: '#4ADE80', label: 'Response reuse — now' },
  runtime: { c: '#A78BFA', label: 'Runtime retention — future' },
  execution: { c: '#F6821F', label: 'Model execution — future' },
  provider: { c: '#FB7185', label: 'Provider boundary — future' }
};

const BANDS = [
  { id: 'band-consumer', plane: 'consumer', x: 160, y: 200, w: 1260, h: 160, alpha: 0.45,
    hdr: { x: 184, y: 230, t: 'CONSUMER INTEGRATION — EXTERNAL PYTHON APPLICATIONS' },
    tagr: { x: 1396, y: 230, t: 'SWAPPABLE APP SURFACES', alpha: 0.65 } },
  { id: 'band-identity', plane: 'identity', x: 160, y: 450, w: 1260, h: 220, alpha: 0.55, dash: true,
    hdr: { x: 184, y: 480, t: 'IDENTITY BC — FOUNDATION · ONLY IDENTITY AUTHORITY' },
    tagr: { x: 1396, y: 480, t: 'OWNED CORE ABSTRACTIONS', alpha: 0.65 } },
  { id: 'band-reuse', plane: 'reuse', x: 160, y: 760, w: 1260, h: 300, alpha: 0.62, dash: true,
    hdr: { x: 184, y: 790, t: 'RESPONSE REUSE BC — NOW · CACHESTORE IS INTERNAL' },
    tagr: { x: 1396, y: 790, t: 'FIRST IMPLEMENTATION TOPIC', alpha: 0.7 } },
  { id: 'band-future-core', plane: null, x: 160, y: 1150, w: 1260, h: 330, stroke: '#3A4250', alpha: 1,
    hdr: { x: 184, y: 1180, t: 'FUTURE CORE CAPABILITIES — NOT BASELINE IMPLEMENTATION', fill: C.slate },
    tagr: { x: 1396, y: 1180, t: 'OWNED ABSTRACTIONS', fill: C.slate, alpha: 0.7 } },
  { id: 'band-provider', plane: 'provider', x: 160, y: 1570, w: 1260, h: 200, alpha: 0.3,
    hdr: { x: 184, y: 1600, t: 'PROVIDER ADAPTER BOUNDARY — FUTURE · LOCAL OR REMOTE' },
    tagr: { x: 1396, y: 1600, t: 'SWAPPABLE EXTERNAL SURFACES', alpha: 0.7 } }
];

const BOXES = [
  { id: 'consumer', plane: 'consumer', band: 'band-consumer', x: 200, y: 260, w: 340, h: 80, r: 10,
    name: 'Python consumer', about: '外部應用程式使用 library 能力，但不成為核心政策的擁有者。',
    texts: [ ['bl', 224, 288, 'Python consumer'], ['bs', 224, 310, '嵌入 library capability'], ['bs', 224, 326, '不擁有核心政策'] ] },
  { id: 'submission', plane: 'consumer', band: 'band-consumer', x: 590, y: 260, w: 400, h: 80, r: 10,
    name: 'Model and request submission', about: '將模型與請求脈絡交給核心 Identity authority。',
    texts: [ ['bl', 614, 288, 'Model + request submission'], ['bs', 614, 310, '提供完整執行脈絡'], ['bs', 614, 326, '不判定是否重用'] ] },
  { id: 'receiver', plane: 'consumer', band: 'band-consumer', x: 1040, y: 260, w: 340, h: 80, r: 10,
    name: 'Result receiver', about: '接收安全重用的 response，或未來模型執行所產生的結果。',
    texts: [ ['bl', 1064, 288, 'Result receiver'], ['bs', 1064, 310, '重用或新產生的 response'], ['bs', 1064, 326, 'provider-agnostic consumer'] ] },

  { id: 'model-identity', plane: 'identity', band: 'band-identity', x: 200, y: 530, w: 340, h: 104, r: 10, dash: true,
    name: 'Model identity', about: '確認實際模型是否相同，而非只比較名稱或路徑。',
    texts: [ ['bl', 224, 558, 'Model identity'], ['bs', 224, 580, '確認實際模型是否相同'], ['bs', 224, 596, '名稱或路徑不足以判定'], ['bn', 224, 618, '僅屬於 identity authority'] ] },
  { id: 'request-identity', plane: 'identity', band: 'band-identity', x: 570, y: 530, w: 360, h: 104, r: 10, dash: true,
    name: 'Complete request identity', about: '確認所有會影響 response 的請求脈絡是否描述同一件請求。',
    texts: [ ['bl', 594, 558, 'Complete request identity'], ['bs', 594, 580, '確認完整請求脈絡'], ['bs', 594, 596, '其他地方不得推測欄位'], ['bn', 594, 618, '僅屬於 identity authority'] ] },
  { id: 'confirmation', plane: 'identity', band: 'band-identity', x: 980, y: 530, w: 380, h: 104, r: 10, dash: true,
    name: 'Identity confirmation', about: '將已確認的模型與請求身分，唯一交接給 Response Reuse。',
    texts: [ ['bl', 1004, 558, 'Identity confirmation'], ['bs', 1004, 580, '唯一的已確認身分交接'], ['bs', 1004, 596, '只提供給 Response Reuse'], ['bn', 1004, 618, '不處理 cache 或 execution'] ] },

  { id: 'reuse-bc', plane: 'reuse', band: 'band-reuse', x: 200, y: 840, w: 500, h: 120, r: 10, dash: true,
    name: 'Response Reuse BC', about: '只消費已確認 identity，並擁有安全重用既有 response 的決策責任。',
    texts: [ ['bl', 224, 868, 'Response Reuse BC'], ['bs', 224, 890, '只消費已確認的 identity'], ['bs', 224, 906, '安全重用決策，不執行模型'], ['bn', 224, 934, '第一個 implementation topic'] ] },
  { id: 'reuse-decision', plane: 'reuse', band: 'band-reuse', x: 750, y: 840, w: 270, h: 104, r: 10, dash: true,
    name: 'Safe reuse decision', about: '只有已確認 identity 允許時，才選擇直接回傳 response 的路徑。',
    texts: [ ['bl', 774, 868, 'Safe reuse decision'], ['bs', 774, 890, 'hit → 直接回傳 response'], ['bs', 774, 906, 'miss → 未來 runtime path'], ['bn', 774, 928, '不自行推導 identity'] ] },
  { id: 'cache-store', plane: 'reuse', band: 'band-reuse', x: 1070, y: 840, w: 290, h: 104, r: 10, dash: true,
    name: 'CacheStore — internal', about: 'Response Reuse 內部元件，只保存與取回 response。',
    texts: [ ['bl', 1094, 868, 'CacheStore — internal'], ['bs', 1094, 890, '保存與取回 response'], ['bs', 1094, 906, '不擁有 identity 或 runtime'], ['bn', 1094, 928, '不是頂層 BC'] ] },
  { id: 'reuse-return', plane: 'reuse', band: 'band-reuse', x: 540, y: 980, w: 310, h: 52, r: 10, dash: true,
    name: 'Reused response return', about: '安全重用決策完成後，直接將 response 回傳給 consumer。',
    texts: [ ['bl', 564, 1008, 'Reused response return'], ['bs', 564, 1024, '直接 hit path'] ] },

  { id: 'runtime-cache', plane: 'runtime', band: 'band-future-core', x: 200, y: 1240, w: 270, h: 104, r: 10, dash: true,
    name: 'Loaded Runtime Cache', about: '未來能力：重用已初始化且可執行的模型 runtime。',
    texts: [ ['bl', 224, 1268, 'Loaded Runtime Cache'], ['bs', 224, 1290, '未來：重用 initialized runtime'], ['bs', 224, 1306, '不屬於 response reuse'], ['bn', 224, 1328, '未來能力'] ] },
  { id: 'runtime-registry', plane: 'runtime', band: 'band-future-core', x: 500, y: 1240, w: 270, h: 104, r: 10, dash: true,
    name: 'Runtime Store / Registry', about: '未來 runtime 專用保存元件，結構上與 CacheStore 分離。',
    texts: [ ['bl', 524, 1268, 'Runtime Store / Registry'], ['bs', 524, 1290, '只保存 runtime state'], ['bs', 524, 1306, '與 CacheStore 分離'], ['bn', 524, 1328, '未來能力'] ] },
  { id: 'runtime-preparation', plane: 'runtime', band: 'band-future-core', x: 330, y: 1370, w: 310, h: 80, r: 10, dash: true,
    name: 'Runtime preparation', about: '未來 miss path：取得或準備可執行的 runtime。',
    texts: [ ['bl', 354, 1398, 'Runtime preparation'], ['bs', 354, 1420, '準備可執行的 runtime'], ['bs', 354, 1436, '不保存 response'] ] },
  { id: 'execution', plane: 'execution', band: 'band-future-core', x: 870, y: 1240, w: 490, h: 104, r: 10, dash: true,
    name: 'Model Execution', about: '未來協調者：當 response 無法重用時，協調 runtime 與模型執行。',
    texts: [ ['bl', 894, 1268, 'Model Execution'], ['bs', 894, 1290, '協調 runtime 與 invocation'], ['bs', 894, 1306, '不擁有 identity 或 reuse policy'], ['bn', 894, 1328, '未來能力'] ] },
  { id: 'result-handoff', plane: 'execution', band: 'band-future-core', x: 960, y: 1370, w: 310, h: 80, r: 10, dash: true,
    name: 'Execution result handoff', about: '將未來 execution 結果交回 Response Reuse，但不直接保存。',
    texts: [ ['bl', 984, 1398, 'Execution result handoff'], ['bs', 984, 1420, '將新 response 交回 reuse'], ['bs', 984, 1436, '不直接保存 response'] ] },

  { id: 'adapter-boundary', plane: 'provider', band: 'band-provider', x: 200, y: 1640, w: 360, h: 88, r: 10,
    name: 'Provider adapter boundary', about: '未來外部邊界，使 provider-specific 行為保持可替換。',
    texts: [ ['bl', 224, 1668, 'Provider adapter boundary'], ['bs', 224, 1690, '未來、可替換的外部邊界'], ['bs', 224, 1706, '不擁有核心政策'] ] },
  { id: 'local-adapter', plane: 'provider', band: 'band-provider', x: 630, y: 1640, w: 320, h: 88, r: 10,
    name: 'Local provider adapter', about: '未來可替換的 local model provider adapter。',
    texts: [ ['bl', 654, 1668, 'Local provider adapter'], ['bs', 654, 1690, '未來 local provider edge'], ['bs', 654, 1706, '可替換 surface'] ] },
  { id: 'remote-adapter', plane: 'provider', band: 'band-provider', x: 1020, y: 1640, w: 340, h: 88, r: 10,
    name: 'Remote provider adapter', about: '未來可替換的 remote model provider adapter。',
    texts: [ ['bl', 1044, 1668, 'Remote provider adapter'], ['bs', 1044, 1690, '未來 remote provider edge'], ['bs', 1044, 1706, '可替換 surface'] ] }
];

const EDGES = [
  { from: 'consumer', to: 'submission', pts: [[542,300],[584,300]], label: { s: 'al', x: 563, y: 288, t: '提交', anchor: 'center' } },
  { from: 'submission', to: 'model-identity', pts: [[790,340],[790,410],[370,410],[370,524]], label: { s: 'al', x: 580, y: 398, t: '模型脈絡', anchor: 'center' } },
  { from: 'submission', to: 'request-identity', pts: [[790,340],[790,524]], label: { s: 'al', x: 804, y: 430, t: '請求脈絡' } },
  { from: 'model-identity', to: 'confirmation', pts: [[542,582],[974,582]], label: { s: 'al', x: 758, y: 570, t: '模型身分', anchor: 'center' } },
  { from: 'request-identity', to: 'confirmation', pts: [[932,582],[974,582]], label: { s: 'al', x: 953, y: 570, t: '請求', anchor: 'center' } },
  { from: 'confirmation', to: 'reuse-bc', pts: [[1170,636],[1170,700],[450,700],[450,834]], label: { s: 'al', x: 810, y: 688, t: '已確認的 identity', anchor: 'center' } },
  { from: 'reuse-bc', to: 'reuse-decision', pts: [[702,892],[744,892]], label: { s: 'al', x: 723, y: 880, t: '判定', anchor: 'center' } },
  { from: 'reuse-decision', to: 'cache-store', pts: [[1022,892],[1064,892]], label: { s: 'al', x: 1043, y: 880, t: '查詢', anchor: 'center' } },
  { from: 'reuse-decision', to: 'reuse-return', pts: [[885,946],[885,970],[695,970],[695,974]], label: { s: 'al', x: 800, y: 962, t: '安全 hit', anchor: 'center' } },
  { from: 'reuse-return', to: 'receiver', pts: [[856,1006],[1436,1006],[1436,300],[1386,300]], label: { s: 'al', x: 1452, y: 660, t: '回傳重用 response', rot: -90, anchor: 'center' } },
  { from: 'reuse-decision', to: 'runtime-cache', pts: [[885,946],[885,1100],[335,1100],[335,1234]], label: { s: 'al', x: 610, y: 1088, t: 'miss — 未來路徑', anchor: 'center' } },
  { from: 'runtime-cache', to: 'runtime-registry', pts: [[472,1292],[494,1292]], label: { s: 'al', x: 483, y: 1280, t: '保存', anchor: 'center' } },
  { from: 'runtime-registry', to: 'runtime-preparation', pts: [[635,1346],[635,1358],[485,1358],[485,1364]], label: { s: 'al', x: 560, y: 1350, t: '取得', anchor: 'center' } },
  { from: 'runtime-preparation', to: 'execution', pts: [[642,1410],[800,1410],[800,1292],[864,1292]], label: { s: 'al', x: 814, y: 1360, t: 'runtime' } },
  { from: 'execution', to: 'adapter-boundary', pts: [[1115,1346],[1115,1510],[380,1510],[380,1634]], label: { s: 'al', x: 748, y: 1498, t: '呼叫 provider', anchor: 'center' } },
  { from: 'adapter-boundary', to: 'local-adapter', pts: [[562,1684],[624,1684]], label: { s: 'al', x: 593, y: 1672, t: 'local', anchor: 'center' } },
  { from: 'adapter-boundary', to: 'remote-adapter', pts: [[562,1708],[780,1708],[780,1750],[1190,1750],[1190,1734]], label: { s: 'al', x: 985, y: 1738, t: 'remote', anchor: 'center' } },
  { from: 'execution', to: 'result-handoff', pts: [[1115,1346],[1115,1364]], label: { s: 'al', x: 1129, y: 1358, t: '新 response' } },
  { from: 'result-handoff', to: 'reuse-bc', pts: [[958,1410],[116,1410],[116,900],[194,900]], label: { s: 'al', x: 100, y: 1156, t: '保存新 response', rot: -90, anchor: 'center' } },
  { from: 'reuse-bc', to: 'receiver', pts: [[450,834],[450,730],[1398,730],[1398,344]], label: { s: 'al', x: 924, y: 718, t: '未來 execution 後的新 response', anchor: 'center' } }
];

const TEXTS = [
  { s: 'title', x: 160, y: 86, t: 'deterministic-response-cache — business capability architecture' },
  { s: 'sub', x: 160, y: 118, t: 'provider-agnostic library baseline：確認 identity → 安全重用 response → 保留 runtime → 執行模型' },
  { s: 'tag', x: 160, y: 146, runs: [
    { t: 'Identity', fill: C.sky }, { t: ' → ', fill: '#4A5462' },
    { t: 'Response Reuse', fill: C.green }, { t: ' → ', fill: '#4A5462' },
    { t: 'Runtime', fill: C.violet }, { t: ' → ', fill: '#4A5462' },
    { t: 'Execution', fill: C.orange } ] },
  { s: 'legend', x: 1082, y: 86, t: '虛線 — 自有的核心 abstraction' },
  { s: 'legend', x: 1082, y: 110, t: '實線 — 可替換的 app 或 provider surface' },
  { s: 'legend', x: 1143, y: 134, t: '顏色 — 所屬 capability plane' },
  { s: 'plane', x: 485, y: 1214, t: 'RUNTIME RETENTION — FUTURE', anchor: 'center', fill: planeColor('runtime') },
  { s: 'plane', x: 1115, y: 1214, t: 'MODEL EXECUTION — FUTURE', anchor: 'center', fill: planeColor('execution') },
  { s: 'bn', x: 160, y: 1844, t: 'invariant：只有 Identity BC 確認模型與完整請求身分；名稱與路徑不足以判定' },
  { s: 'bn', x: 160, y: 1864, t: 'boundary：CacheStore 位於 Response Reuse 內部；Runtime Store / Registry 獨立且屬於未來能力' },
  { s: 'bn', x: 160, y: 1884, t: 'scope：baseline 只記錄 capability boundary；不實作 cache、runtime、execution 或 provider adapter' }
];

const SWATCHES = [
  { x: 1046, y: 75, w: 26, h: 13, stroke: '#8B93A1', alpha: 0.8, dash: true },
  { x: 1046, y: 99, w: 26, h: 13, stroke: C.boxStroke, alpha: 1, fill: C.boxFill }
];

const CHIPS = ['consumer', 'identity', 'reuse', 'runtime', 'execution', 'provider']
  .map((id, i) => ({ x: 1046 + i * 13, y: 123, w: 9, h: 13, fill: planeColor(id) }));
