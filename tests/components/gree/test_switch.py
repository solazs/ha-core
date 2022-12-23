"""Tests for gree component."""
from greeclimate.exceptions import DeviceTimeoutError
import pytest

from homeassistant.components.gree.const import DOMAIN as GREE_DOMAIN
from homeassistant.components.switch import DOMAIN
from homeassistant.const import (
    ATTR_ENTITY_ID,
    ATTR_FRIENDLY_NAME,
    SERVICE_TOGGLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
    STATE_OFF,
    STATE_ON,
)
from homeassistant.helpers import entity_registry as er

from tests.common import MockConfigEntry

ENTITY_ID_LIGHT_PANEL = f"{DOMAIN}.fake_device_1_panel_light"
ENTITY_ID_HEALTH_MODE = f"{DOMAIN}.fake_device_1_health_mode"
ENTITY_ID_QUIET = f"{DOMAIN}.fake_device_1_quiet"
ENTITY_ID_FRESH_AIR = f"{DOMAIN}.fake_device_1_fresh_air"
ENTITY_ID_XFAN = f"{DOMAIN}.fake_device_1_xfan"


async def async_setup_gree(hass):
    """Set up the gree switch platform."""
    entry = MockConfigEntry(domain=GREE_DOMAIN, data={GREE_DOMAIN: {DOMAIN: {}}})
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()


async def test_health_mode_disabled_by_default(hass):
    """Test for making sure health mode is disabled on first load."""
    await async_setup_gree(hass)

    assert (
        er.async_get(hass).async_get(ENTITY_ID_HEALTH_MODE).disabled_by
        == er.RegistryEntryDisabler.INTEGRATION
    )


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_HEALTH_MODE,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
    ],
)
async def test_send_switch_on(hass, entity, entity_registry_enabled_by_default):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_HEALTH_MODE,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
    ],
)
async def test_send_switch_on_device_timeout(
    hass, device, entity, entity_registry_enabled_by_default
):
    """Test for sending power on command to the device with a device timeout."""
    device().push_state_update.side_effect = DeviceTimeoutError

    await async_setup_gree(hass)

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_HEALTH_MODE,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
    ],
)
async def test_send_switch_off(hass, entity, entity_registry_enabled_by_default):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_OFF,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_OFF


@pytest.mark.parametrize(
    "entity",
    [
        ENTITY_ID_LIGHT_PANEL,
        ENTITY_ID_HEALTH_MODE,
        ENTITY_ID_QUIET,
        ENTITY_ID_FRESH_AIR,
        ENTITY_ID_XFAN,
    ],
)
async def test_send_switch_toggle(hass, entity, entity_registry_enabled_by_default):
    """Test for sending power on command to the device."""
    await async_setup_gree(hass)

    # Turn the service on first
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TURN_ON,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON

    # Toggle it off
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TOGGLE,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_OFF

    # Toggle is back on
    assert await hass.services.async_call(
        DOMAIN,
        SERVICE_TOGGLE,
        {ATTR_ENTITY_ID: entity},
        blocking=True,
    )

    state = hass.states.get(entity)
    assert state is not None
    assert state.state == STATE_ON


@pytest.mark.parametrize(
    "entity,name",
    [
        (ENTITY_ID_LIGHT_PANEL, "Panel Light"),
        (ENTITY_ID_HEALTH_MODE, "Health mode"),
        (ENTITY_ID_QUIET, "Quiet"),
        (ENTITY_ID_FRESH_AIR, "Fresh Air"),
        (ENTITY_ID_XFAN, "XFan"),
    ],
)
async def test_entity_name(hass, entity, name, entity_registry_enabled_by_default):
    """Test for name property."""
    await async_setup_gree(hass)
    state = hass.states.get(entity)
    assert state.attributes[ATTR_FRIENDLY_NAME] == f"fake-device-1 {name}"
