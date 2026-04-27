from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..models.prompts import Playlist, PromptSet
from ..odata import ODataQuery
from .base import BaseService


class PromptsService(BaseService):
    _PROMPT_SETS = "/PromptSets"
    _CUSTOM_PROMPTS = "/CustomPrompts"
    _PLAYLISTS = "/Playlists"

    # ------------------------------------------------------------------
    # Prompt sets
    # ------------------------------------------------------------------

    def list_prompt_sets(self, query: Optional[ODataQuery] = None) -> List[PromptSet]:
        data = self._list_raw(self._PROMPT_SETS, query)
        return [PromptSet.model_validate(item) for item in data.get("value", [])]

    def get_prompt_set(self, set_id: int, query: Optional[ODataQuery] = None) -> PromptSet:
        data = self._get(f"{self._PROMPT_SETS}({set_id})", params=self._query_params(query))
        return PromptSet.model_validate(data)

    def update_prompt_set(self, set_id: int, changes: PromptSet | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, PromptSet) else changes
        self._patch(f"{self._PROMPT_SETS}({set_id})", json=payload)

    def delete_prompt_set(self, set_id: int) -> None:
        self._delete(f"{self._PROMPT_SETS}({set_id})")

    def get_active_prompt_set(self) -> PromptSet:
        data = self._get(f"{self._PROMPT_SETS}/Pbx.GetActive()")
        return PromptSet.model_validate(data)

    def copy_prompt_set(self, set_id: int, data: Dict[str, Any]) -> PromptSet:
        result = self._post(f"{self._PROMPT_SETS}({set_id})/Pbx.Copy", json=data)
        return PromptSet.model_validate(result)

    def play_prompt(self, set_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PROMPT_SETS}({set_id})/Pbx.PlayPrompt", json=data)

    def record_prompt(self, set_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PROMPT_SETS}({set_id})/Pbx.RecordPrompt", json=data)

    def set_active_prompt_set(self, set_id: int) -> None:
        self._post(f"{self._PROMPT_SETS}({set_id})/Pbx.SetActive")

    def set_alternate_pronunciation(self, set_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PROMPT_SETS}({set_id})/Pbx.SetAlternatePronunciation", json=data)

    def list_prompts(self, set_id: int, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PROMPT_SETS}({set_id})/Prompts", params=self._query_params(query))
        return self._list_values(data)

    # ------------------------------------------------------------------
    # Custom prompts
    # ------------------------------------------------------------------

    def list_custom_prompts(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw(self._CUSTOM_PROMPTS, query)
        return self._list_values(data)

    def delete_custom_prompt(self, filename: str) -> None:
        self._delete(f"{self._CUSTOM_PROMPTS}('{filename}')")

    def make_call_record_prompt(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._CUSTOM_PROMPTS}/Pbx.MakeCallRecordCustomPrompt", json=data)

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------

    def list_playlists(self, query: Optional[ODataQuery] = None) -> List[Playlist]:
        data = self._list_raw(self._PLAYLISTS, query)
        return [Playlist.model_validate(item) for item in data.get("value", [])]

    def create_playlist(self, playlist: Playlist | Dict[str, Any]) -> Playlist:
        payload = playlist.model_dump(by_alias=True, exclude_none=True) if isinstance(playlist, Playlist) else playlist
        data = self._post(self._PLAYLISTS, json=payload)
        return Playlist.model_validate(data)

    def get_playlist(self, name: str) -> Playlist:
        data = self._get(f"{self._PLAYLISTS}('{name}')")
        return Playlist.model_validate(data)

    def update_playlist(self, name: str, changes: Playlist | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Playlist) else changes
        self._patch(f"{self._PLAYLISTS}('{name}')", json=payload)

    def delete_playlist(self, name: str) -> None:
        self._delete(f"{self._PLAYLISTS}('{name}')")

    def delete_playlist_file(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PLAYLISTS}/Pbx.DeletePlaylistFile", json=data)

    def download_playlist_file(self, playlist_key: str, file_name: str) -> bytes:
        return self._get_bytes(
            f"{self._PLAYLISTS}/Pbx.DownloadPlaylistFile(playlistKey='{playlist_key}',fileName='{file_name}')"
        )
