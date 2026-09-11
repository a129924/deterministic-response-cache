# model-feature-identity — Technical Specification

## Contract placement

新增的 executable modules 位於 `src/deterministic_response_cache/identity/`：

- `contracts.py`：PureType、immutable VO、Outcome、`IdentitySource` ABC 與 stage Protocol。
- `builders.py`：注入式 `ModelIdentityBuilder` 與 `FeatureIdentityBuilder` orchestration。
- `__init__.py`：Identity package 的 explicit public re-export surface；不改變 root package
  initializer。

`identity/.gitkeep` 不是本 topic 的 artifact；它屬於另一 active topic，保持原樣。

## Type and pipeline contract

- `PureType` 是遞迴 type alias：JSON scalar、`list`／`tuple` 與 key 為 `str` 的 mapping。
  list／tuple 的順序是 input contract；mapping 的 canonical sort 是 Sorter responsibility。
- 每個 pipeline boundary 都以 named immutable VO handoff；Encoder 的 handoff 是具型別標記的
  canonical representation，Serializer 的 handoff 是 deterministic bytes。這些 VO 不暗示特定
  serialized wire format 或 hash algorithm。
- `Hash(value: str)` 是不透明 immutable value；不承諾 SHA-256、hex encoding 或 digest length。
- `Validator.validate(...)` 回傳 `Success[ValidatedIdentity] | Failure`。`Failure` 包含一個非空
  immutable `tuple[ValidationIssue, ...]`；每個 issue 有 `path`、`code`、`message`。
- Sorter、Encoder、Serializer 與 Hasher 的 Protocol 各自只消費前一 stage 的 immutable handoff；
  Hasher 回傳 `Hash`。

## Builder behavior

1. `ModelIdentityBuilder.build(source)` 取得 `source.identity_fields()`，依固定五 stage 順序
   建立 `ModelIdentity`，或原樣回傳 Validator 的 `Failure`。
2. `FeatureIdentityBuilder.build(source)` 依相同規則建立 `FeatureIdentity`。
3. `FeatureIdentityBuilder.combine(model_identity, feature_identity)` 將 leaf identities 放入固定
   具名 aggregate；aggregate 必須再通過 Validator → Sorter → Encoder → Serializer → Hasher，
   成為 `CompleteRequestIdentity`。不得直接 concatenate hash strings。
4. 任一 Validator invocation 回傳 `Failure` 時，該 invocation 的後續 Sorter、Encoder、
   Serializer、Hasher 一律不得呼叫。

## Boundary decisions

- 這是 non-stable-library topic：不修改 README、version、release notes 或 root package public
  surface，且沒有 release action。
- Concrete stage implementation 及其 exception policy 是後續、獨立 topic 的責任；本 topic 只
  固定 Validator 的 Outcome contract。
- tests 以 injected fakes 驗證 orchestration、stage order、immutable handoff、short-circuit 與
  aggregate re-hash；不以真實 hash algorithm 測試替代這些 contract tests。
