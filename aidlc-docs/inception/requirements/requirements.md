# Requirements Document

## Intent Analysis

- **User Request**: Implement dzengi-sdk logger with debug logging to see request and response details
- **Request Type**: SDK enhancement / observability
- **Scope**: Client initialization, shared request layer, unit tests, README
- **Complexity**: Simple

## Functional Requirements

1. **FR-1**: `DzengiClient` must expose an opt-in way to enable SDK debug logging.
2. **FR-2**: When debug logging is enabled, outbound SDK requests must log request details.
3. **FR-3**: When debug logging is enabled, inbound SDK responses must log response details.
4. **FR-4**: Sensitive request values, including signatures and secrets, must not appear in debug logs.
5. **FR-5**: Existing SDK behavior must remain unchanged when debug logging is not enabled.
6. **FR-6**: Public documentation must describe how to enable SDK debug logging.

## Non-Functional Requirements

1. **NFR-1**: The solution must use Python's standard logging framework.
2. **NFR-2**: Debug logging must be low overhead when disabled.
3. **NFR-3**: The implementation must preserve compatibility with the existing supported Python versions.

## Technical Context

- **Language**: Python (>=3.8)
- **Package**: `dzengi_com_client`
- **Request Layer**: `dzengi_com_client/api/base.py`
- **Client Entry Point**: `dzengi_com_client/client.py`
- **Testing Strategy**: `pytest` with `responses` mocks
