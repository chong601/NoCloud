# NoCloud VMM — Design Document

**Status:** Draft v0.2 — pending author review  
**Scope:** v1 library milestone (no daemon, no CLI, no snapshots)  
**Last updated:** 2026-05-18

---

## 1. Project Overview

NoCloud is a Python VMM library that uses libvirt/QEMU as its execution backend. It owns
the decision-making layer — what to do, when, and in what order — while libvirt handles
low-level hypervisor interaction. The project is intentionally library-first: no persistent
daemon, no web interface, no CLI in v1. Those layers build on top of a clean, well-tested
library API.

### Design Principles

- **Library-first.** Every capability is exposed as a callable API. Applications (CLI,
  daemon, web) are consumers of the library, not part of it.
- **Explicit over implicit.** Defaults are opinionated but visible. Nothing happens silently.
- **Warnings are soft, dispatch is hard.** Warnings in the XML pipeline are soft
  failures — data is still usable and inspectable. At the libvirt dispatch boundary,
  any warning becomes a hard lock. NoCloud only dispatches XML it fully accounts for.
- **Testability from day one.** All core logic is unit-testable without a running libvirt
  instance. Integration tests require libvirt but are clearly separated.
- **Schema portability.** The state store schema is defined for SQLite but designed to port
  to other backends (PostgreSQL, a document store) without a full rewrite.

---

## 2. Package Structure

```
nocloud/                        # VMM library
├── __init__.py
├── manager.py                  # VMManager — primary public API
├── operations/
│   ├── __init__.py
│   ├── base.py                 # Operation base class, op lock
│   ├── create.py
│   ├── start.py
│   ├── stop.py
│   ├── destroy.py
│   ├── delete.py
│   └── modify.py
├── state/
│   ├── __init__.py
│   ├── models.py               # VMRecord, VMSpec, VMStatus (Python dataclasses)
│   ├── store.py                # StateStore interface (abstract)
│   └── sqlite.py               # SQLiteStateStore (v1 reference implementation)
├── reconciler.py               # Spec→status reconciliation logic
├── defaults.py                 # NoCloud-level opinionated defaults
└── exceptions.py

nocloud_libvirt_xml/            # XML wrapper and schema library
├── __init__.py
├── models/
│   ├── __init__.py
│   ├── domain.py               # Domain, CPU, Memory, OS, …
│   ├── storage.py              # StoragePool, StorageVolume
│   ├── network.py              # Network, Interface definitions
│   └── capabilities.py        # Host capabilities introspection
├── pipeline.py                 # parse → validate → serialize pipeline + hash check
├── validation.py               # RelaxNG schema validation
├── dispatch.py                 # LibvirtDispatcher — only accepts ValidatedXML
├── validated.py                # ValidatedXML token type (private constructor)
├── defaults.py                 # libvirt-specific opinionated defaults
├── result.py                   # ParseResult, SerializeResult, Warning types
└── exceptions.py

tests/
├── unit/
│   ├── test_xml_pipeline.py
│   ├── test_models_domain.py
│   ├── test_models_storage.py
│   ├── test_models_network.py
│   ├── test_state_store.py
│   ├── test_operations.py
│   └── test_reconciler.py
└── integration/
    ├── conftest.py             # libvirt fixture (requires running libvirtd)
    ├── test_vm_lifecycle.py
    └── test_xml_roundtrip.py
```

---

## 3. `nocloud_libvirt_xml` — XML Wrapper

### 3.1 Responsibilities

- Pydantic model definitions for all libvirt XML object types that NoCloud manages.
- A well-defined parse → validate → serialize pipeline with explicit stages.
- Round-trip hash checking to detect data loss during serialization.
- RelaxNG schema validation as an explicit, callable step.
- Warning emission for unmodeled XML elements encountered during parsing.
- **No VMM logic.** This package knows nothing about VM lifecycle, state, or operations.

### 3.2 Pydantic-XML Models

All models use `pydantic-xml` for XML binding. Pydantic v2 is the base.

**Opinionated defaults enforced at model level:**

| Field | Default | Rationale |
|---|---|---|
| `machine` | `q35` | Modern chipset; i440fx is legacy |
| `memory unit` | Always stored as MiB internally | Avoids KiB/GiB ambiguity |
| `cpu.mode` | `host-model` | Reasonable performance/compat balance |
| `disk.driver` | `qemu`/`qcow2` | Standard for KVM |
| `disk.target_bus` | `virtio` | Best performance for Linux guests |
| `interface.model` | `virtio` | Best performance |
| `video.model` | `virtio` | Best for Linux guests |

**Example model sketch (domain):**

```python
from pydantic_xml import BaseXmlModel, attr, element, wrapped
from typing import Optional, List

class CPU(BaseXmlModel, tag="cpu"):
    mode: str = attr(default="host-model")
    model: Optional[str] = element(tag="model", default=None)
    sockets: int = ...  # from topology element
    cores: int = ...
    threads: int = ...

class Domain(BaseXmlModel, tag="domain"):
    type: str = attr(default="kvm")
    name: str = element(tag="name")
    uuid: Optional[str] = element(tag="uuid", default=None)
    memory_mib: int = ...   # always MiB, converted on parse/serialize
    vcpus: int = element(tag="vcpu")
    cpu: CPU = element(tag="cpu", default_factory=CPU)
    disks: List[Disk] = wrapped("devices", element(tag="disk", default_factory=list))
    interfaces: List[Interface] = wrapped("devices", element(tag="interface", default_factory=list))
    # ...
```

### 3.3 The XML Pipeline

All XML processing flows through a single pipeline object. Stages are explicit and
individually callable, but the full pipeline is the recommended entry point.

```
Input XML string
      │
      ▼
┌─────────────┐
│    PARSE    │  ET.fromstring() — well-formedness only
│             │  Raises: ParseError on malformed XML
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VALIDATE   │  RelaxNG check against libvirt schemas
│  (optional) │  Returns: ValidationResult (pass/fail + messages)
│             │  Skipped if schema files not installed
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MODEL     │  Pydantic-XML → Python object
│             │  Unknown elements → collected as warnings
└──────┬──────┘
       │
       ▼
  ParseResult
  ├── domain: Domain          # the Pydantic model
  ├── warnings: List[Warning] # unmodeled elements found
  ├── input_hash: str         # SHA-256 of lxml c14n of input XML
  └── validation: ValidationResult | None
```

**Serialization + dispatch pipeline:**

```
Domain object
      │
      ▼
┌─────────────┐
│  SERIALIZE  │  Pydantic-XML → XML string
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  HASH CHECK │  lxml c14n → SHA-256, compare to ParseResult.input_hash
│             │  Mismatch → raises PipelineError (never a warning)
└──────┬──────┘
       │  hash matches AND no warnings from parse stage
       ▼
┌─────────────┐
│  WARN CHECK │  Any warnings present? → raises PipelineError
│             │  Warnings = incomplete implementation; must fix before dispatch
└──────┬──────┘
       │  zero warnings
       ▼
  ValidatedXML                # proof-of-passage token; only pipeline can mint this
      │
      ▼
┌─────────────┐
│  DISPATCH   │  LibvirtDispatcher.define(validated: ValidatedXML)
│             │  Rejects anything that is not a ValidatedXML from the pipeline
└─────────────┘
```

`ValidatedXML` is the mandatory gate between the pipeline and libvirt. Any path to
libvirt that bypasses it is a design violation.

### 3.4 Warning Types

```python
class WarningCode(Enum):
    UNMODELED_ELEMENT    = "unmodeled_element"    # element exists in XML, not in our model
    HASH_MISMATCH        = "hash_mismatch"         # round-trip hash differs
    DEPRECATED_MACHINE   = "deprecated_machine"    # i440fx detected
    SCHEMA_SKIP          = "schema_skip"           # RelaxNG schemas not available

@dataclass
class Warning:
    code: WarningCode
    message: str
    element_path: Optional[str] = None   # e.g. "domain/devices/tpm"
```

### 3.5 `ValidatedXML` — The Dispatch Token

#### Warnings: soft in general use, hard at the dispatch boundary

Warnings in `nocloud_libvirt_xml` are **soft failures** in normal data handling. A
`ParseResult` carrying warnings is still a usable object — the caller can read fields,
mutate the model, re-serialize for inspection, and make informed decisions about how to
proceed. Warnings surface through `ParseResult.warnings` and as `logging.warning()`
calls; they do not make the data inert.

The dispatch boundary is the single exception. At the point where NoCloud hands XML to
libvirt, warnings become a **hard lock**. The reason is not libvirt's permissiveness —
libvirt will often accept data it doesn't fully understand. The reason is NoCloud's own
accountability: `ValidatedXML` is a claim that NoCloud fully understands and accounts
for every element in the XML being dispatched. A warning means that claim cannot be
made. Sending uncertain state to libvirt is the one place where "probably fine" is not
an acceptable answer.

This means `ValidatedXML` is not primarily a "libvirt will accept this" guarantee. It
is a "NoCloud completely owns this" guarantee.

#### The token

`ValidatedXML` is a frozen dataclass. It is the **only** type accepted by
`LibvirtDispatcher`. It carries no warnings by construction.

```python
# nocloud_libvirt_xml/validated.py

_PIPELINE_CALLER = "XMLPipeline"   # expected caller identity

@dataclass(frozen=True)
class ValidatedXML:
    xml: str
    schema_type: str        # "domain", "network", "storagepool", etc.
    input_hash: str         # c14n SHA-256 of the source XML
    _caller: str = field(default="", repr=False)

    def __post_init__(self):
        if self._caller != _PIPELINE_CALLER:
            raise TypeError(
                "ValidatedXML must be constructed by XMLPipeline, not directly. "
                f"Got caller: {self._caller!r}"
            )
```

`XMLPipeline` passes `_caller=_PIPELINE_CALLER` when constructing the token. Any
external attempt to instantiate `ValidatedXML` without the correct caller string raises
`TypeError` immediately.

`LibvirtDispatcher` enforces the token at runtime:

```python
# nocloud_libvirt_xml/dispatch.py

class LibvirtDispatcher:
    def define(self, validated: ValidatedXML) -> str:
        if not isinstance(validated, ValidatedXML):
            raise TypeError(f"Expected ValidatedXML, got {type(validated).__name__}")
        # proceed to libvirt defineXML(validated.xml)
```

**Invariants guaranteed by `ValidatedXML`:**
- XML was well-formed (parse stage passed)
- RelaxNG validation passed (schema files must be present — see note below)
- Round-trip hash matched (no data loss)
- Zero warnings at time of issue — NoCloud fully accounts for all elements

**Note on `SCHEMA_SKIP`:** If libvirt schema files are not installed, the validation
stage emits `Warning(SCHEMA_SKIP)`. Because that warning blocks `ValidatedXML`
issuance, schema files are a hard runtime dependency for the dispatch path. This is
intentional — a silent skip at the one point where correctness must be certain is
worse than a loud failure.

### 3.6 Hash-Based Round-Trip Check

The round-trip check uses **lxml c14n** (W3C Canonical XML) for both the input hash
and the output hash. lxml is already a dependency for RelaxNG validation, so c14n is
available at no additional cost and is strictly correct.

1. At parse time, canonicalise the input XML with lxml c14n and store SHA-256 as
   `input_hash` on `ParseResult`.
2. At serialize time, canonicalise the output XML and compute its SHA-256.
3. If hashes differ, raise `PipelineError` — this is never a warning. The error
   distinguishes two root causes based on whether parse warnings were emitted:
   - Warnings present → unmodeled elements caused data loss (implementation gap)
   - No warnings → serialization bug in the model (implementation error)

In both cases the result is the same: `ValidatedXML` is not issued and libvirt does
not receive the data.

### 3.7 RelaxNG Validation

libvirt ships RelaxNG schemas for all its XML types (domain, network, storage pool, etc.).
Validation is an explicit step, not automatic, and **required** on the dispatch path:

```python
result = pipeline.validate(xml_string, schema="domain")
# result.valid: bool
# result.errors: List[str]
```

Schema files are looked up from a configurable path (default:
`/usr/share/libvirt/schemas/`). If schemas are not found, a `Warning(SCHEMA_SKIP)` is
emitted. Because `SCHEMA_SKIP` is a warning, it blocks `ValidatedXML` issuance — schema
files must be present for any data to reach libvirt.

### 3.8 Supported XML Types (v1)

| Type | Parse | Serialize | Validate |
|---|---|---|---|
| Domain | ✓ | ✓ | ✓ |
| Storage Pool | ✓ | ✓ | ✓ |
| Storage Volume | ✓ | ✓ | ✓ |
| Network | ✓ | ✓ | ✓ |
| Host Capabilities | ✓ (read-only) | — | ✓ |

---

## 4. `nocloud` — VMM Library

### 4.1 Responsibilities

- Define what a VM is in NoCloud terms (spec + status).
- Manage VM state durably via the state store.
- Execute VM lifecycle operations sequentially via an operation lock.
- Translate NoCloud specs into `nocloud_libvirt_xml` objects and submit to libvirt.
- Reconcile desired state (spec) with observed state (status).
- **No libvirt XML knowledge.** All XML concerns are delegated to `nocloud_libvirt_xml`.

### 4.2 VM State Model

Inspired by Kubernetes CRD but simplified. No YAML/JSON on the wire — this is a pure
Python library.

```python
@dataclass
class VMSpec:
    """Desired state — what the user wants the VM to be."""
    name: str
    memory_mib: int
    vcpus: int
    cpu_mode: str = "host-model"
    machine: str = "q35"
    disks: List[DiskSpec] = field(default_factory=list)
    interfaces: List[InterfaceSpec] = field(default_factory=list)
    boot_order: List[str] = field(default_factory=lambda: ["hd"])
    # Future: cloud-init, tags, description

@dataclass
class VMStatus:
    """Observed state — what libvirt reports."""
    phase: VMPhase           # see below
    libvirt_state: Optional[str] = None   # "running", "shut off", etc.
    libvirt_uuid: Optional[str] = None
    error: Optional[str] = None
    last_transition: Optional[datetime] = None

class VMPhase(str, Enum):
    PENDING    = "Pending"      # created in DB, not yet in libvirt
    CREATING   = "Creating"     # operation in progress
    RUNNING    = "Running"
    STOPPED    = "Stopped"
    MODIFYING  = "Modifying"
    DELETING   = "Deleting"
    FAILED     = "Failed"
    DELETED    = "Deleted"      # terminal, kept for audit

@dataclass
class VMRecord:
    """Full record stored in the state store."""
    id: str                  # UUID, generated by NoCloud
    spec: VMSpec
    status: VMStatus
    created_at: datetime
    updated_at: datetime
```

### 4.3 State Store

The `StateStore` is an abstract interface. The v1 reference implementation is SQLite.

```python
class StateStore(Protocol):
    def get(self, vm_id: str) -> Optional[VMRecord]: ...
    def list(self) -> List[VMRecord]: ...
    def create(self, record: VMRecord) -> VMRecord: ...
    def update_status(self, vm_id: str, status: VMStatus) -> VMRecord: ...
    def update_spec(self, vm_id: str, spec: VMSpec) -> VMRecord: ...
    def delete(self, vm_id: str) -> None: ...
```

**SQLite schema:**

```sql
CREATE TABLE vms (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    phase       TEXT NOT NULL,
    created_at  TEXT NOT NULL,   -- ISO-8601
    updated_at  TEXT NOT NULL,   -- ISO-8601

    -- Queryable scalar fields extracted from spec/status
    memory_mib  INTEGER NOT NULL,
    vcpus       INTEGER NOT NULL,
    libvirt_uuid TEXT,
    error_msg   TEXT,

    -- Blob columns for structured data not worth normalising
    spec_json   TEXT NOT NULL,   -- JSON: full VMSpec
    status_json TEXT NOT NULL    -- JSON: full VMStatus
);

CREATE INDEX idx_vms_phase ON vms(phase);
CREATE INDEX idx_vms_name  ON vms(name);
```

Design rationale: queryable fields (phase, name, memory, vcpus) are promoted to columns
for efficient filtering. The full spec and status live in JSON columns so schema changes
to VMSpec/VMStatus don't require migrations for non-queryable fields.

### 4.4 Operation Model

**v1: global sequential lock.** One operation runs at a time, system-wide. This is a
deliberate simplification — the lock is an asyncio-compatible `asyncio.Lock` so the
architecture can be evolved to per-VM locking without interface changes.

```python
class OperationLock:
    """Global operation lock for v1. Swap internals for per-VM lock in v2."""
    async def acquire(self, vm_id: str, op_name: str) -> AsyncContextManager: ...
```

All operations follow the same pattern:

```
1. Acquire lock
2. Load VMRecord from state store
3. Assert pre-conditions (e.g. VM must be Stopped to Start)
4. Set phase to transitional state (e.g. CREATING)
5. Execute action (libvirt API call via nocloud_libvirt_xml)
6. Set phase to terminal state (RUNNING / FAILED)
7. Release lock
```

Errors in step 5 transition the VM to `FAILED` with the error message captured in
`VMStatus.error`. The lock is always released.

**Operation classes (v1):**

| Class | Input phase(s) | Output phase | libvirt action |
|---|---|---|---|
| `CreateOperation` | — (new) | `STOPPED` | `defineXML` |
| `StartOperation` | `STOPPED` | `RUNNING` | `create` |
| `StopOperation` | `RUNNING` | `STOPPED` | `shutdown` (ACPI) |
| `DestroyOperation` | `RUNNING` | `STOPPED` | `destroy` (force) |
| `ModifyOperation` | `STOPPED` | `STOPPED` | `undefine` + `defineXML` |
| `DeleteOperation` | `STOPPED` | `DELETED` | `undefine` |

### 4.5 Public API — VMManager

`VMManager` is the single entry point for library consumers.

```python
class VMManager:
    def __init__(
        self,
        libvirt_uri: str = "qemu:///system",
        state_store: Optional[StateStore] = None,   # defaults to SQLiteStateStore
        db_path: str = "/var/lib/nocloud/state.db",
    ): ...

    # --- Query ---
    def get(self, vm_id: str) -> VMRecord: ...
    def list(self, phase: Optional[VMPhase] = None) -> List[VMRecord]: ...

    # --- Lifecycle ---
    async def create(self, spec: VMSpec) -> VMRecord: ...
    async def start(self, vm_id: str) -> VMRecord: ...
    async def stop(self, vm_id: str, *, force: bool = False) -> VMRecord: ...
    async def delete(self, vm_id: str) -> VMRecord: ...
    async def modify(self, vm_id: str, spec: VMSpec) -> VMRecord: ...

    # --- Introspection ---
    def sync_status(self, vm_id: str) -> VMRecord:
        """Poll libvirt for current state and update status."""
        ...
```

Sync wrappers (`create_sync`, `start_sync`, etc.) are provided as convenience methods for
non-async callers. They run the coroutine in a managed event loop.

### 4.6 Spec → libvirt XML Translation

`nocloud` translates `VMSpec` → `nocloud_libvirt_xml.Domain` in `nocloud/reconciler.py`.
NoCloud defaults live here; `nocloud_libvirt_xml` defaults are only applied when NoCloud
provides no value.

```python
def spec_to_domain(spec: VMSpec, uuid: Optional[str] = None) -> Domain:
    """Translate a NoCloud VMSpec into a libvirt Domain model."""
    return Domain(
        name=spec.name,
        uuid=uuid or str(uuid4()),
        domain_type="kvm",
        memory_mib=spec.memory_mib,
        vcpus=spec.vcpus,
        cpu=CPU(mode=spec.cpu_mode),
        os=OS(type="hvm", arch="x86_64", machine=spec.machine, boot_dev=spec.boot_order),
        disks=[_disk_spec_to_model(d) for d in spec.disks],
        interfaces=[_iface_spec_to_model(i) for i in spec.interfaces],
        features=["acpi", "apic"],
        clock_offset="utc",
    )
```

### 4.7 NoCloud Defaults

Defined in `nocloud/defaults.py`. These are the VMM-level decisions:

```python
DEFAULT_MACHINE    = "q35"
DEFAULT_CPU_MODE   = "host-model"
DEFAULT_CLOCK      = "utc"
DEFAULT_FEATURES   = ["acpi", "apic"]
DEFAULT_DISK_BUS   = "virtio"
DEFAULT_DISK_FORMAT = "qcow2"
DEFAULT_NIC_MODEL  = "virtio"
DEFAULT_VIDEO      = "virtio"
DEFAULT_EMULATOR   = "/usr/bin/qemu-system-x86_64"
DEFAULT_IMAGE_DIR  = "/var/lib/libvirt/images"
```

---

## 5. Cross-Cutting Concerns

### 5.1 Error Handling

All public API errors derive from `NoCloudError`. Subclasses:

```
NoCloudError
├── VMNotFoundError
├── InvalidPhaseError        # e.g. trying to start a RUNNING VM
├── OperationFailedError     # libvirt reported failure
├── ValidationError          # spec or XML failed validation
└── StateStoreError          # DB error
```

`nocloud_libvirt_xml` errors:

```
LibvirtXMLError
├── ParseError               # malformed XML
├── ValidationError          # RelaxNG check failed
└── SerializeError           # serialization produced invalid output
```

### 5.2 Logging

Standard Python `logging` throughout. Logger names follow module paths:
`nocloud.manager`, `nocloud.operations.create`, `nocloud_libvirt_xml.pipeline`, etc.

Warnings from the XML pipeline are emitted both as `ParseResult.warnings` (structured)
and as `logging.warning()` calls (human-readable), so they surface regardless of whether
the caller inspects the result object.

### 5.3 Dependencies

**`nocloud_libvirt_xml`:**
- `pydantic >= 2.0`
- `pydantic-xml >= 2.0`
- `lxml` (RelaxNG validation)

**`nocloud`:**
- `nocloud_libvirt_xml`
- `libvirt-python`
- `aiosqlite` (async SQLite access)

**Dev / test:**
- `pytest`
- `pytest-asyncio`
- `pytest-cov`

### 5.4 Python Version

Minimum: Python 3.11 (used for `StrEnum`, `tomllib`, better typing).

---

## 6. Testing Strategy

### 6.1 Unit Tests (no libvirt required)

All unit tests run without a libvirt connection. libvirt calls are mocked via
`unittest.mock`.

Key test areas:

- **XML pipeline:** parse → model → serialize for each XML type. Round-trip hash
  consistency. Warning emission for known-unmodeled elements. Hash mismatch raises
  `PipelineError`, not a warning. `ValidatedXML` not issued when any warning present.
- **ValidatedXML enforcement:** Direct construction without pipeline caller raises
  `TypeError`. `LibvirtDispatcher` rejects non-`ValidatedXML` input.
- **Model validation:** Pydantic field validators catch bad values (negative memory, empty
  name, etc.).
- **Spec translation:** `spec_to_domain()` produces expected Domain objects for given
  inputs. Default values applied correctly.
- **State store:** CRUD operations, phase transitions, JSON round-trip for spec/status.
- **Operation pre-conditions:** `StartOperation` on RUNNING VM raises `InvalidPhaseError`.
  Phase transitions are recorded correctly.
- **Operation lock:** Concurrent operation attempts are serialised (asyncio test).

### 6.2 Integration Tests (libvirt required)

Marked with `pytest.mark.integration`. Skipped unless `NOCLOUD_LIBVIRT_URI` is set.

- Full VM lifecycle: create → start → stop → delete.
- Modify: change memory/vcpu on a stopped VM, verify libvirt reflects new values.
- `sync_status`: reconcile NoCloud state against live libvirt state.
- XML round-trip against real `virsh dumpxml` output.

### 6.3 Test Fixtures

```python
# tests/unit/conftest.py
@pytest.fixture
def minimal_spec():
    return VMSpec(
        name="test-vm",
        memory_mib=1024,
        vcpus=1,
        disks=[DiskSpec(source="/tmp/test.qcow2", target_dev="vda")],
        interfaces=[InterfaceSpec(source_network="default")],
    )

@pytest.fixture
def mock_libvirt(monkeypatch):
    # Returns a MagicMock wired to common libvirt calls
    ...
```

---

## 7. Out of Scope for v1

The following are explicitly deferred:

- **Snapshots** (online/offline, revert, delete)
- **Storage pool / volume lifecycle** (create pool, allocate volume)
- **Network lifecycle** (create/delete libvirt networks)
- **Hook integration / event listener** (requires daemon layer)
- **CLI** (`nocloud` command)
- **Migration** (live or offline)
- **Per-VM operation queues** (currently global lock)
- **cloud-init / ignition integration**
- **BGP / advanced networking**

---

## 8. Open Questions

These are flagged for resolution before or during implementation:

1. **`nocloud_libvirt_xml` package distribution.** PyPI-published independently, or
   bundled as a namespace package within `nocloud`? Affects import paths and versioning.

2. **SQLite WAL mode.** Should be enabled by default for better concurrent read
   performance even in v1 (reads during an in-progress write won't block).

3. **Async vs sync as primary interface.** Current design exposes async as primary with
   sync wrappers. If the majority of callers are sync scripts, this could be inverted.

4. **libvirt connection management.** Single shared connection vs. per-operation open/close.
   libvirt connections are not thread-safe; need a strategy for the async operation model.

---

## 9. Glossary

| Term | Definition |
|---|---|
| **Domain** | libvirt term for a virtual machine definition |
| **Phase** | NoCloud's view of a VM's lifecycle state |
| **Spec** | Desired state of a VM, as declared by the user |
| **Status** | Observed state of a VM, as reported by libvirt |
| **Round-trip** | Parse XML → model → serialize XML, producing equivalent output |
| **Operation** | An atomic, sequentially-executed lifecycle action on a VM |
| **Pipeline** | The parse → validate → model → serialize chain in `nocloud_libvirt_xml` |
| **ValidatedXML** | Immutable proof-of-passage token issued by the pipeline; certifies NoCloud fully accounts for all XML elements; required by `LibvirtDispatcher` |
| **PipelineError** | Hard failure raised when hash mismatches or warnings are present; blocks `ValidatedXML` issuance |
