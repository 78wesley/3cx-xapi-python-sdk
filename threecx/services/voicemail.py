from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseService


class VoicemailService(BaseService):
    _PATH = "/VoicemailSettings"

    def get_settings(self) -> Dict[str, Any]:
        return self._get(self._PATH)

    def update_settings(self, data: Dict[str, Any]) -> None:
        self._patch(self._PATH, json=data)

    def create_converter_config(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.CreateConverterConfiguration", json=data)

    def delete_converter_config(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteConverterConfiguration", json=data)

    def get_configured_converters(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Pbx.GetConfiguredConverters()")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_connected_converters(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Pbx.GetConnectedConvertersData()")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_transcribe_languages(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PATH}/Pbx.GetTranscribeLanguages()")
        return self._list_values(data) if isinstance(data, dict) else data

    def get_converter_request_status(self, strict: bool = False) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetConverterRequestStatus(strict={'true' if strict else 'false'})")

    def delete_all_user_voicemails(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.DeleteAllUserVoicemails", json=data)

    def get_music_on_hold_settings(self) -> Dict[str, Any]:
        return self._get("/MusicOnHoldSettings")

    def update_music_on_hold_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/MusicOnHoldSettings", json=data)
