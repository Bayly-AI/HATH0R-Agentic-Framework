"""Data models and schemas for Hath0r Playwright UI testing integration."""

from __future__ import annotations

import enum
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class PlaywrightBrowserType(str, enum.Enum):
    """Supported Playwright browser engines."""

    CHROMIUM = "chromium"
    FIREFOX = "firefox"
    WEBKIT = "webkit"


class PlaywrightTestStatus(str, enum.Enum):
    """Lifecycle status of a Playwright test case."""

    AUTOMATED = "automated"
    PENDING_GENERATION = "pending_generation"
    MANUAL = "manual"
    SKIPPED = "skipped"
    DEPRECATED = "deprecated"


class PlaywrightActionType(str, enum.Enum):
    """Playwright step action types."""

    GOTO = "goto"
    CLICK = "click"
    FILL = "fill"
    TYPE = "type"
    PRESS = "press"
    HOVER = "hover"
    WAIT_FOR_SELECTOR = "waitForSelector"
    WAIT_FOR_TIMEOUT = "waitForTimeout"
    EXPECT_VISIBLE = "expectVisible"
    EXPECT_TEXT = "expectText"
    EXPECT_VALUE = "expectValue"
    EXPECT_VISUAL_MATCH = "expectVisualMatch"
    SCREENSHOT = "screenshot"


@dataclass
class PlaywrightStep:
    """Individual action/assertion step in a Playwright test."""

    step_number: int
    action: PlaywrightActionType
    selector: Optional[str] = None
    value: Optional[str] = None
    timeout_ms: Optional[int] = None
    expected: Optional[str] = None
    snapshot_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "step_number": self.step_number,
            "action": self.action.value if isinstance(self.action, PlaywrightActionType) else self.action,
        }
        if self.selector is not None:
            data["selector"] = self.selector
        if self.value is not None:
            data["value"] = self.value
        if self.timeout_ms is not None:
            data["timeout_ms"] = self.timeout_ms
        if self.expected is not None:
            data["expected"] = self.expected
        if self.snapshot_name is not None:
            data["snapshot_name"] = self.snapshot_name
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaywrightStep:
        return cls(
            step_number=int(data["step_number"]),
            action=PlaywrightActionType(data["action"]),
            selector=data.get("selector"),
            value=data.get("value"),
            timeout_ms=data.get("timeout_ms"),
            expected=data.get("expected"),
            snapshot_name=data.get("snapshot_name"),
        )


@dataclass
class PlaywrightTestCase:
    """Canonical test case specification for Playwright."""

    test_id: str
    title: str
    description: str
    status: PlaywrightTestStatus = PlaywrightTestStatus.AUTOMATED
    browser: PlaywrightBrowserType = PlaywrightBrowserType.CHROMIUM
    tags: List[str] = field(default_factory=list)
    steps: List[PlaywrightStep] = field(default_factory=list)
    expected_outcome: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value if isinstance(self.status, PlaywrightTestStatus) else self.status,
            "browser": self.browser.value if isinstance(self.browser, PlaywrightBrowserType) else self.browser,
            "tags": list(self.tags),
            "steps": [s.to_dict() for s in self.steps],
            "expected_outcome": self.expected_outcome,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaywrightTestCase:
        return cls(
            test_id=data["test_id"],
            title=data["title"],
            description=data.get("description", ""),
            status=PlaywrightTestStatus(data.get("status", "automated")),
            browser=PlaywrightBrowserType(data.get("browser", "chromium")),
            tags=list(data.get("tags", [])),
            steps=[PlaywrightStep.from_dict(s) for s in data.get("steps", [])],
            expected_outcome=data.get("expected_outcome"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
        )


@dataclass
class PlaywrightTestSuite:
    """Suite grouping related Playwright test cases for a component or page."""

    suite_id: str
    title: str
    description: str
    target_component: str
    target_path: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    test_cases: List[PlaywrightTestCase] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_id": self.suite_id,
            "title": self.title,
            "description": self.description,
            "target_component": self.target_component,
            "target_path": self.target_path,
            "tags": list(self.tags),
            "test_cases": [tc.to_dict() for tc in self.test_cases],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaywrightTestSuite:
        return cls(
            suite_id=data["suite_id"],
            title=data["title"],
            description=data.get("description", ""),
            target_component=data["target_component"],
            target_path=data.get("target_path"),
            tags=list(data.get("tags", [])),
            test_cases=[PlaywrightTestCase.from_dict(tc) for tc in data.get("test_cases", [])],
        )


@dataclass
class PlaywrightCatalogMetadata:
    """Metadata settings for the master catalog."""

    framework: str = "playwright"
    default_browser: PlaywrightBrowserType = PlaywrightBrowserType.CHROMIUM
    default_timeout_ms: int = 30000
    viewport_width: int = 1280
    viewport_height: int = 720

    def to_dict(self) -> Dict[str, Any]:
        return {
            "framework": self.framework,
            "default_browser": self.default_browser.value if isinstance(self.default_browser, PlaywrightBrowserType) else self.default_browser,
            "default_timeout_ms": self.default_timeout_ms,
            "viewport": {
                "width": self.viewport_width,
                "height": self.viewport_height,
            },
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaywrightCatalogMetadata:
        vp = data.get("viewport", {})
        return cls(
            framework=data.get("framework", "playwright"),
            default_browser=PlaywrightBrowserType(data.get("default_browser", "chromium")),
            default_timeout_ms=int(data.get("default_timeout_ms", 30000)),
            viewport_width=int(vp.get("width", 1280)),
            viewport_height=int(vp.get("height", 720)),
        )


@dataclass
class PlaywrightMasterCatalog:
    """Top-level master catalog containing all Playwright suites and metadata."""

    project: str
    schema_version: str = "hath0r.playwright.testspec/1"
    last_synced_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: PlaywrightCatalogMetadata = field(default_factory=PlaywrightCatalogMetadata)
    suites: List[PlaywrightTestSuite] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "project": self.project,
            "last_synced_at": self.last_synced_at,
            "metadata": self.metadata.to_dict(),
            "suites": [s.to_dict() for s in self.suites],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PlaywrightMasterCatalog:
        return cls(
            schema_version=data.get("schema_version", "hath0r.playwright.testspec/1"),
            project=data.get("project", "HATH0R-Project"),
            last_synced_at=data.get("last_synced_at", datetime.now(timezone.utc).isoformat()),
            metadata=PlaywrightCatalogMetadata.from_dict(data.get("metadata", {})),
            suites=[PlaywrightTestSuite.from_dict(s) for s in data.get("suites", [])],
        )


@dataclass
class PlaywrightExecutionResult:
    """Results from running a Playwright test case."""

    test_id: str
    suite_id: str
    status: str  # "PASS", "FAIL", "SKIPPED"
    duration_ms: float
    error: Optional[str] = None
    screenshot_path: Optional[str] = None
    trace_path: Optional[str] = None
    steps_passed: int = 0
    steps_total: int = 0
    visual_diff_percentage: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
