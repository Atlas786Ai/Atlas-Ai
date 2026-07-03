"""Frozen Atlas v1.0 architecture manifest."""

FROZEN_REPOSITORIES = [
    "IdentityRepository",
    "MissionRepository",
    "KnowledgeRepository",
    "MemoryRepository",
    "CognitiveContextRepository",
    "ReasoningRepository",
    "PlanningRepository",
    "DecisionRepository",
    "PredictionRepository",
    "SimulationRepository",
    "ExecutionRepository",
    "PortfolioRepository",
    "MarketRepository",
    "RiskRepository",
    "AnalyticsRepository",
    "MonitoringRepository",
    "RecoveryRepository",
    "AuditRepository",
    "SecurityRepository",
    "RuntimeRepository",
    "ConfigurationRepository",
    "LoggingRepository",
]

BOOT_SEQUENCE = [
    ["ConfigurationRepository", "LoggingRepository", "SecurityRepository", "AuditRepository"],
    ["RuntimeRepository", "EventBus"],
    ["IdentityRepository", "MissionRepository", "KnowledgeRepository", "MemoryRepository", "CognitiveContextRepository"],
    ["ReasoningRepository", "PlanningRepository", "DecisionRepository", "PredictionRepository", "SimulationRepository"],
    ["PortfolioRepository", "MarketRepository", "RiskRepository", "AnalyticsRepository", "MonitoringRepository", "RecoveryRepository", "ExecutionRepository"],
]
