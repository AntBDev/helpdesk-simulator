from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.device_state import DeviceState
from app.models.ticket import Ticket
from app.schemas.device_state import DeviceStateCreate
from app.services.tool_event_service import (
    record_tool_action,
)


def get_device_state_by_device_id(
    db: Session,
    device_id: int,
) -> DeviceState | None:
    statement = select(DeviceState).where(DeviceState.device_id == device_id)

    return db.scalar(statement)


def create_device_state(
    db: Session,
    state_data: DeviceStateCreate,
) -> DeviceState:
    state = DeviceState(**state_data.model_dump())

    db.add(state)
    db.commit()
    db.refresh(state)

    return state


def device_state_snapshot(
    state: DeviceState,
) -> dict[str, object]:
    return {
        "network_adapter_enabled": (state.network_adapter_enabled),
        "gateway_reachable": (state.gateway_reachable),
        "dns_resolving": state.dns_resolving,
        "internet_reachable": (state.internet_reachable),
        "disk_total_gb": state.disk_total_gb,
        "disk_free_gb": state.disk_free_gb,
        "cpu_usage_percent": (state.cpu_usage_percent),
        "memory_usage_percent": (state.memory_usage_percent),
        "pending_reboot": state.pending_reboot,
        "primary_service_name": (state.primary_service_name),
        "primary_service_running": (state.primary_service_running),
    }


def save_diagnostic_action(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
    *,
    action: str,
    changed: bool,
    before: dict[str, object],
    message: str,
) -> tuple[DeviceState, bool, str]:
    after = device_state_snapshot(state)

    try:
        record_tool_action(
            db,
            ticket,
            tool="DEVICE_DIAGNOSTICS",
            action=action,
            changed=changed,
            before=before,
            after=after,
            message=message,
        )

        db.commit()
        db.refresh(state)

        return state, changed, message

    except Exception:
        db.rollback()
        raise


def inspect_device(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    snapshot = device_state_snapshot(state)

    message = "Technician inspected simulated device health information."

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="INSPECT",
        changed=False,
        before=snapshot,
        message=message,
    )


def test_connectivity(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    snapshot = device_state_snapshot(state)

    if not state.network_adapter_enabled:
        message = "Connectivity test failed: network adapter is disabled."

    elif not state.gateway_reachable:
        message = "Connectivity test failed: default gateway is unreachable."

    elif not state.internet_reachable:
        message = "Gateway is reachable, but external network connectivity failed."

    else:
        message = (
            "Connectivity test passed. Gateway and external network are reachable."
        )

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="CONNECTIVITY_TEST",
        changed=False,
        before=snapshot,
        message=message,
    )


def test_dns(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    snapshot = device_state_snapshot(state)

    if not state.network_adapter_enabled:
        message = "DNS test could not complete because the network adapter is disabled."

    elif not state.gateway_reachable:
        message = "DNS test could not complete because the gateway is unreachable."

    elif state.dns_resolving:
        message = "DNS resolution test passed."

    else:
        message = "DNS resolution test failed."

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="DNS_TEST",
        changed=False,
        before=snapshot,
        message=message,
    )


def check_resources(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    snapshot = device_state_snapshot(state)

    disk_used = state.disk_total_gb - state.disk_free_gb

    disk_used_percent = round(disk_used / state.disk_total_gb * 100)

    message = (
        f"Resource check: CPU "
        f"{state.cpu_usage_percent}%, memory "
        f"{state.memory_usage_percent}%, disk "
        f"{disk_used_percent}% used."
    )

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="RESOURCE_CHECK",
        changed=False,
        before=snapshot,
        message=message,
    )


def enable_network_adapter(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    before = device_state_snapshot(state)

    changed = not state.network_adapter_enabled

    state.network_adapter_enabled = True

    if changed:
        message = "Network adapter was enabled."
    else:
        message = "Network adapter was already enabled."

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="ENABLE_NETWORK_ADAPTER",
        changed=changed,
        before=before,
        message=message,
    )


def restart_primary_service(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    before = device_state_snapshot(state)

    if state.primary_service_name is None:
        return save_diagnostic_action(
            db,
            ticket,
            state,
            action="RESTART_SERVICE",
            changed=False,
            before=before,
            message=("No managed primary service is configured for this device."),
        )

    changed = not state.primary_service_running

    state.primary_service_running = True

    if changed:
        message = f"{state.primary_service_name} was restarted successfully."
    else:
        message = f"{state.primary_service_name} was already running."

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="RESTART_SERVICE",
        changed=changed,
        before=before,
        message=message,
    )


def reboot_device(
    db: Session,
    ticket: Ticket,
    state: DeviceState,
) -> tuple[DeviceState, bool, str]:
    before = device_state_snapshot(state)

    changed = state.pending_reboot or (
        state.primary_service_name is not None and not state.primary_service_running
    )

    state.pending_reboot = False

    if state.primary_service_name is not None:
        state.primary_service_running = True

    message = (
        "Simulated device reboot completed."
        if changed
        else (
            "Simulated device reboot completed; "
            "no pending device state required repair."
        )
    )

    return save_diagnostic_action(
        db,
        ticket,
        state,
        action="REBOOT",
        changed=changed,
        before=before,
        message=message,
    )
