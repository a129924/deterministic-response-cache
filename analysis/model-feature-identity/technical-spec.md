# model-feature-identity — Technical Specification

## Contract placement

新增的 executable modules 位於 `src/deterministic_response_cache/identity/`：

- `contracts.py`：PureType、immutable VO、Outcome、`IdentitySource` ABC 與 stage Protocol。
- `builders.py`：注入式 `ModelIdentityBuilder` 與 `FeatureIdentityBuilder` orchestration。
- `__init__.py`：Identity package 的 explicit public re-export surface；不改變 root package
  initializer。

`identity/.gitkeep` 不是本 topic 的 artifact；它屬於另一 active topic，保持原樣。

## Type and pipeline contract

- `JSONScalar = None | bool | int | float | str`；`PureType` 是遞迴 type alias：`JSONScalar`、
  `list[PureType]`、`tuple[PureType, ...]` 與 `Mapping[str, PureType]`。list／tuple 的順序是
  input contract；mapping 的 canonical sort 是 Sorter responsibility。
- 下列 VO 一律是 `@dataclass(frozen=True, slots=True)`；每個 field 均依此表固定，並由 Builder
  以 immutable tuple handoff 傳遞。`IdentityField` 的 `value` 仍是 `PureType`，不在本 topic
  指定 nested value 的具體 canonical representation。

  | VO | Fixed fields |
  | --- | --- |
  | `IdentityField` | `name: str`, `value: PureType` |
  | `RawIdentity` | `fields: tuple[IdentityField, ...]` |
  | `ValidatedIdentity` | `fields: tuple[IdentityField, ...]` |
  | `SortedIdentity` | `fields: tuple[IdentityField, ...]` |
  | `EncodedIdentity` | `value: str`（opaque、具型別標記的 canonical representation） |
  | `SerializedIdentity` | `value: bytes`（deterministic bytes） |
  | `Hash` | `value: str`（opaque digest value） |
  | `ModelIdentity` | `value: Hash` |
  | `FeatureIdentity` | `value: Hash` |
  | `LeafIdentityAggregate` | `model_identity: ModelIdentity`, `feature_identity: FeatureIdentity` |
  | `CompleteRequestIdentity` | `value: Hash` |
  | `ValidationIssue` | `path: str`, `code: str`, `message: str` |
  | `Success[T]` | `value: T` |
  | `Failure` | `issues: tuple[ValidationIssue, ...]`，必須 non-empty |

- `Hash.value` 不承諾 SHA-256、hex encoding 或 digest length。`Failure` 的 `issues` 必須是只含
  `ValidationIssue` 的 non-empty `tuple`；非 tuple、含非 `ValidationIssue` 元素與 empty tuple 都是
  contract-construction error。Validator 對 invalid input 必須回傳含完整 issues 的 `Failure`，而非
  partial success。
- 每個 Protocol 的唯一 callable 與精確型別如下；Protocol 不宣告其他 public method：

  ```python
  class Validator(Protocol):
      def validate(self, identity: RawIdentity) -> Success[ValidatedIdentity] | Failure: ...


  class Sorter(Protocol):
      def sort(self, identity: ValidatedIdentity) -> SortedIdentity: ...


  class Encoder(Protocol):
      def encode(self, identity: SortedIdentity) -> EncodedIdentity: ...


  class Serializer(Protocol):
      def serialize(self, identity: EncodedIdentity) -> SerializedIdentity: ...


  class Hasher(Protocol):
      def hash(self, identity: SerializedIdentity) -> Hash: ...
  ```

  `IdentitySource.identity_fields() -> Mapping[str, PureType]` 是唯一 abstract method。Builder 在建立
  `RawIdentity` 前必須遞迴 snapshot 每個 `PureType` value：scalar 保持原值；list 與 tuple 轉成遞迴
  snapshot 的 tuple；每個 mapping 轉成含遞迴 snapshot key/value 的新 `dict` 再以
  `types.MappingProxyType` 包裝。nested container 不可與 caller 共用，所有 sequence 的原有順序與
  mapping 的 key/value 內容必須保留，且 mapping canonical sort 仍是 Sorter 的責任。如此 caller 在
  `build()` 回傳後修改 nested source value，不得改變已交給 Validator 或其後 stage 的 `RawIdentity`。

## Builder behavior

1. `ModelIdentityBuilder` 與 `FeatureIdentityBuilder` 都以相同的 keyword-only constructor
   注入 stage dependency：

   ```python
   def __init__(
       self,
       *,
       validator: Validator,
       sorter: Sorter,
       encoder: Encoder,
       serializer: Serializer,
       hasher: Hasher,
   ) -> None: ...
   ```

2. `ModelIdentityBuilder.build(self, source: IdentitySource) -> Success[ModelIdentity] | Failure`
   及 `FeatureIdentityBuilder.build(self, source: IdentitySource) -> Success[FeatureIdentity] | Failure`
   都從 source snapshot 得到 `RawIdentity`，依 `validate → sort → encode → serialize → hash` 執行，
   並分別包裝最終 `Hash` 成 leaf identity。
3. `FeatureIdentityBuilder.combine(self, model_identity: ModelIdentity, feature_identity:
   FeatureIdentity) -> Success[CompleteRequestIdentity] | Failure` 必須先建立固定欄位的
   `LeafIdentityAggregate`。它接著僅以 aggregate 的兩個 hash value 建立新的 `RawIdentity`：
   `model_identity` 與 `feature_identity`（兩個 `IdentityField.name` 均為此 exact string），再完整
   執行 `validate → sort → encode → serialize → hash`，並以結果建立 `CompleteRequestIdentity`。不得
   concatenate hash strings。
4. 任一 `Validator.validate()` invocation 回傳 `Failure` 時，該 invocation 的後續 Sorter、Encoder、
   Serializer、Hasher 一律不得呼叫；Builder 原樣回傳該 `Failure`。

## PR #5 comment-fix contract

此 route 只處理 PR #5 的四個既有 inline threads；它不改變 Identity BC 的其他行為或 public API。repair
subject 只可變更 `contracts.py`、`builders.py` 與相對應兩個 direct-import test files。

1. `PRRT_kwDOUJTij86hljUO`：保留 separated subject/tester/reviewer ancestry；在 resolution 前以實際 Git
   ancestor check 驗證 S1、T1、S2 subject、S2 Tester 與 S2 Reviewer evidence 都可從 PR repair head 到達。
2. `PRRT_kwDOUJTij86hlk-Z`：實作上述 recursive source snapshot，並以 nested mapping/list mutation regression
   test 證明 source mutation 不會改變已記錄的 Validator input。
3. `PRRT_kwDOUJTij86hlk--`：以 Planner-derived PRC1 route state 取代任何靜態 R5 pending claim；此為 planning
   candidate 的修正，非 repair subject 的 source change。
4. `PRRT_kwDOUJTij86hlk_c`：實作 `Failure` constructor 的 tuple 與 element-type validation，並以 direct
   regression tests 覆蓋 list、empty tuple 與 non-`ValidationIssue` element。

## Boundary decisions

- 這是 non-stable-library topic：不修改 README、version、release notes 或 root package public
  surface，且沒有 release action。
- Concrete stage implementation 及其 exception policy 是後續、獨立 topic 的責任；本 topic 只
  固定 Validator 的 Outcome contract。
- tests 以 injected fakes 驗證 orchestration、stage order、immutable handoff、short-circuit 與
  aggregate re-hash；不以真實 hash algorithm 測試替代這些 contract tests。
