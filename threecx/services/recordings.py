from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.recordings import Recording
from ..odata import ODataQuery
from .base import BaseService


class RecordingsService(BaseService):
    _PATH = "/Recordings"

    def list(self, query: Optional[ODataQuery] = None) -> List[Recording]:
        data = self._list_raw(self._PATH, query)
        return [Recording.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[Recording]:
        yield from self._paginate(self._PATH, Recording, query)

    def download(self, rec_id: int) -> bytes:
        return self._get_bytes(f"{self._PATH}/Pbx.DownloadRecording(recId={rec_id})")

    def get_repository_settings(self) -> Dict[str, Any]:
        return self._get(f"{self._PATH}/Pbx.GetRecordingRepositorySettings()")

    def set_repository_settings(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.SetRecordingRepositorySettings", json=data)

    def archive(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.Archive", json=data)

    def bulk_archive(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkRecordingsArchive", json=data)

    def bulk_delete(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkRecordingsDelete", json=data)

    def purge_archive(self) -> None:
        self._post(f"{self._PATH}/Pbx.PurgeArchive")

    def purge_local(self) -> None:
        self._post(f"{self._PATH}/Pbx.PurgeLocal")

    def transcribe(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.TranscribeRecordings", json=data)

    # ------------------------------------------------------------------
    # Remote archiving settings
    # ------------------------------------------------------------------

    def get_remote_archiving_settings(self) -> Dict[str, Any]:
        return self._get("/RemoteArchivingSettings")

    def update_remote_archiving_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/RemoteArchivingSettings", json=data)

    def archive_chats(self) -> None:
        self._post("/RemoteArchivingSettings/Pbx.ArchiveChats")

    def archive_faxes(self) -> None:
        self._post("/RemoteArchivingSettings/Pbx.ArchiveFaxes")

    def archive_recordings(self) -> None:
        self._post("/RemoteArchivingSettings/Pbx.ArchiveRecordings")

    def archive_voicemail(self) -> None:
        self._post("/RemoteArchivingSettings/Pbx.ArchiveVoicemail")
