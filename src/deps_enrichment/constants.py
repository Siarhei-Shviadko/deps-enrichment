PROJECT_NAME = "enrichment"
DESCRIPTION = "Service for storing additional document information"
V1_PREFIX = "/v1"
BASE_API_PREFIX = "/api/enrichment"
V1_API_PREFIX = BASE_API_PREFIX + V1_PREFIX
SWAGGER_DOC_URL = "/docs"

DOCUMENTS_EXCHANGER = "Documents"
DOCUMENT_TYPE_EXCHANGER = "DocumentType"

EVENTS_QUEUE = "enrichment-events"
COMMANDS_QUEUE = "enrichment-commands"

COMMANDS_CHANNEL = "EnrichmentCommands"
COMMANDS_REPLIES_CHANNEL = "EnrichmentCommandsReplies"
