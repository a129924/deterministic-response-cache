# model-feature-identity — Requirements

## Goal

在 Identity BC 建立可注入、可驗證的 Python contract layer，讓 Model 與 Feature
identity source 透過同一條 deterministic pipeline 產生各自 leaf identity，並組合成
完整 request identity。

## Required outcomes

1. 提供 `IdentitySource` ABC；唯一 abstract method 為
   `identity_fields() -> Mapping[str, PureType]`，Model 與 Feature source 都以它提供
   identity input。
2. 提供可注入的 `Validator`、`Sorter`、`Encoder`、`Serializer`、`Hasher` Protocol，並
   固定 Builder orchestration 順序為 Validator → Sorter → Encoder → Serializer → Hasher
   → Hash。
3. 提供 immutable handoff value objects、`Hash`、`ModelIdentity`、`FeatureIdentity` 與
   `CompleteRequestIdentity`；三種 identity 不可混用。
4. `ModelIdentityBuilder` 和 `FeatureIdentityBuilder` 分別建立 leaf identity；
   `FeatureIdentityBuilder.combine()` 必須以固定具名 aggregate 表示兩個 leaf identity，
   再走完整 canonicalization 與 hashing pipeline，產生 `CompleteRequestIdentity`。
5. Validator 以 `Success[T] | Failure` 回傳；`Failure` 必須保留非空、immutable 的完整
   `ValidationIssue` tuple，並使 Builder short-circuit，禁止後續 stage 執行。
6. `PureType` contract 支援 JSON scalar、遞迴 string-keyed mapping、保持順序的 list／tuple；
   validation contract 拒絕 set、非字串 key、`NaN` 與 `±Infinity`。

## Constraints

- Identity BC 是模型 identity 與完整 request identity 的唯一 authority；其他 BC 不得
  重建或解讀這些規則。
- 本 topic 僅建立 contracts 與 Builder orchestration，不提供 concrete Validator、Sorter、
  Encoder、Serializer 或 Hasher algorithm。
- 不實作 CacheStore、Response Reuse、Loaded Runtime Cache、Model Execution、Provider
  Adapter、外部 I/O、async API 或 legacy gateway compatibility。
- `src/deterministic_response_cache/identity/.gitkeep` 屬於 active
  `package-topology-skeleton-replay` topic；本 topic 必須保持它唯讀，不得刪除或修改。
- 不修改 root public surface、README、version、project configuration 或既有 direct-import
  regression。
