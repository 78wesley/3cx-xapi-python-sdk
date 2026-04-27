from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.phones import DeviceInfo, Firmware, Fxs, FxsTemplate, Phone, PhoneTemplate, SipDevice
from ..odata import ODataQuery
from .base import BaseService


class PhonesService(BaseService):
    _PHONES = "/Phones"
    _TEMPLATES = "/PhoneTemplates"
    _SIP_DEVICES = "/SipDevices"
    _FXS = "/Fxs"
    _FXS_TEMPLATES = "/FxsTemplates"
    _DEVICE_INFOS = "/DeviceInfos"
    _FIRMWARES = "/Firmwares"
    _PHONE_LOGOS = "/PhoneLogos"

    # ------------------------------------------------------------------
    # Phones
    # ------------------------------------------------------------------

    def list(self, query: Optional[ODataQuery] = None) -> List[Phone]:
        data = self._list_raw(self._PHONES, query)
        return [Phone.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Phone]:
        yield from self._paginate(self._PHONES, Phone, query)

    def get(self, phone_id: int, query: Optional[ODataQuery] = None) -> Phone:
        data = self._get(f"{self._PHONES}({phone_id})", params=self._query_params(query))
        return Phone.model_validate(data)

    def update(self, phone_id: int, changes: Phone | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Phone) else changes
        self._patch(f"{self._PHONES}({phone_id})", json=payload)

    def delete(self, phone_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PHONES}({phone_id})", etag=etag)

    # ------------------------------------------------------------------
    # Phone templates
    # ------------------------------------------------------------------

    def list_templates(self, query: Optional[ODataQuery] = None) -> List[PhoneTemplate]:
        data = self._list_raw(self._TEMPLATES, query)
        return [PhoneTemplate.model_validate(item) for item in data.get("value", [])]

    def get_template(self, template_id: int) -> PhoneTemplate:
        data = self._get(f"{self._TEMPLATES}({template_id})")
        return PhoneTemplate.model_validate(data)

    def create_template(self, tmpl: PhoneTemplate | Dict[str, Any]) -> PhoneTemplate:
        payload = tmpl.model_dump(by_alias=True, exclude_none=True) if isinstance(tmpl, PhoneTemplate) else tmpl
        data = self._post(self._TEMPLATES, json=payload)
        return PhoneTemplate.model_validate(data)

    def update_template(self, template_id: int, changes: PhoneTemplate | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, PhoneTemplate) else changes
        self._patch(f"{self._TEMPLATES}({template_id})", json=payload)

    def delete_template(self, template_id: int) -> None:
        self._delete(f"{self._TEMPLATES}({template_id})")

    # ------------------------------------------------------------------
    # Phone actions (triggered via Users service path)
    # ------------------------------------------------------------------

    def reboot(self, mac: str) -> None:
        self._post("/Users/Pbx.RebootPhone", json={"MAC": mac})

    def reprovision(self, mac: str) -> None:
        self._post("/Users/Pbx.ReprovisionPhone", json={"MAC": mac})

    # ------------------------------------------------------------------
    # SIP Devices
    # ------------------------------------------------------------------

    def list_sip_devices(self, query: Optional[ODataQuery] = None) -> List[SipDevice]:
        data = self._list_raw(self._SIP_DEVICES, query)
        return [SipDevice.model_validate(item) for item in data.get("value", [])]

    def push_sip_firmware(self, device_id: int) -> None:
        self._post(f"{self._SIP_DEVICES}({device_id})/Pbx.PushFirmware")

    # ------------------------------------------------------------------
    # FXS devices
    # ------------------------------------------------------------------

    def list_fxs(self, query: Optional[ODataQuery] = None) -> List[Fxs]:
        data = self._list_raw(self._FXS, query)
        return [Fxs.model_validate(item) for item in data.get("value", [])]

    def create_fxs(self, fxs: Fxs | Dict[str, Any]) -> Fxs:
        payload = fxs.model_dump(by_alias=True, exclude_none=True) if isinstance(fxs, Fxs) else fxs
        data = self._post(self._FXS, json=payload)
        return Fxs.model_validate(data)

    def get_fxs(self, mac: str) -> Fxs:
        data = self._get(f"{self._FXS}('{mac}')")
        return Fxs.model_validate(data)

    def update_fxs(self, mac: str, changes: Fxs | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Fxs) else changes
        self._patch(f"{self._FXS}('{mac}')", json=payload)

    def delete_fxs(self, mac: str) -> None:
        self._delete(f"{self._FXS}('{mac}')")

    def regenerate_fxs_web_credentials(self, mac: str) -> None:
        self._post(f"{self._FXS}('{mac}')/Pbx.RegenerateWebCredentials")

    # ------------------------------------------------------------------
    # FXS templates
    # ------------------------------------------------------------------

    def list_fxs_templates(self, query: Optional[ODataQuery] = None) -> List[FxsTemplate]:
        data = self._list_raw(self._FXS_TEMPLATES, query)
        return [FxsTemplate.model_validate(item) for item in data.get("value", [])]

    def create_fxs_template(self, tmpl: FxsTemplate | Dict[str, Any]) -> FxsTemplate:
        payload = tmpl.model_dump(by_alias=True, exclude_none=True) if isinstance(tmpl, FxsTemplate) else tmpl
        data = self._post(self._FXS_TEMPLATES, json=payload)
        return FxsTemplate.model_validate(data)

    def get_fxs_template(self, template_id: int) -> FxsTemplate:
        data = self._get(f"{self._FXS_TEMPLATES}({template_id})")
        return FxsTemplate.model_validate(data)

    def update_fxs_template(self, template_id: int, changes: FxsTemplate | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, FxsTemplate) else changes
        self._patch(f"{self._FXS_TEMPLATES}({template_id})", json=payload)

    def delete_fxs_template(self, template_id: int) -> None:
        self._delete(f"{self._FXS_TEMPLATES}({template_id})")

    # ------------------------------------------------------------------
    # Device infos
    # ------------------------------------------------------------------

    def list_device_infos(self, query: Optional[ODataQuery] = None) -> List[DeviceInfo]:
        data = self._list_raw(self._DEVICE_INFOS, query)
        return [DeviceInfo.model_validate(item) for item in data.get("value", [])]

    def get_device_info(self, device_id: str) -> DeviceInfo:
        data = self._get(f"{self._DEVICE_INFOS}('{device_id}')")
        return DeviceInfo.model_validate(data)

    def delete_device_info(self, device_id: str) -> None:
        self._delete(f"{self._DEVICE_INFOS}('{device_id}')")

    def provision_device(self, device_id: str) -> None:
        self._post(f"{self._DEVICE_INFOS}('{device_id}')/Pbx.Provision")

    # ------------------------------------------------------------------
    # Firmwares
    # ------------------------------------------------------------------

    def list_firmwares(self, query: Optional[ODataQuery] = None) -> List[Firmware]:
        data = self._list_raw(self._FIRMWARES, query)
        return [Firmware.model_validate(item) for item in data.get("value", [])]

    def delete_firmware(self, firmware_id: str) -> None:
        self._delete(f"{self._FIRMWARES}('{firmware_id}')")

    def cleanup_firmwares(self) -> None:
        self._post(f"{self._FIRMWARES}/Pbx.CleanUp")

    def get_firmware_state(self) -> Dict[str, Any]:
        return self._get(f"{self._FIRMWARES}/Pbx.GetFirmwareState()")

    def push_firmware_for_phones(self, firmware_id: str, data: Dict[str, Any]) -> None:
        self._post(f"{self._FIRMWARES}('{firmware_id}')/Pbx.PushFirmwareForPhones", json=data)

    # ------------------------------------------------------------------
    # Phone logos
    # ------------------------------------------------------------------

    def list_phone_logos(self) -> List[Dict[str, Any]]:
        data = self._get(self._PHONE_LOGOS)
        return self._list_values(data) if isinstance(data, dict) else data

    def delete_phone_logo(self, filename: str) -> None:
        self._delete(f"{self._PHONE_LOGOS}('{filename}')")
