from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.users import ForwardingProfile, Greeting, User, UserGroupRef
from ..odata import ODataQuery
from .base import BaseService


class UsersService(BaseService):
    _PATH = "/Users"

    # ------------------------------------------------------------------
    # Collection
    # ------------------------------------------------------------------

    def list(self, query: Optional[ODataQuery] = None) -> List[User]:
        data = self._list_raw(self._PATH, query)
        return [User.model_validate(item) for item in data.get("value", [])]

    def iterate(self, query: Optional[ODataQuery] = None) -> Iterator[User]:
        yield from self._paginate(self._PATH, User, query)

    def create(self, user: User | Dict[str, Any]) -> User:
        payload = user.model_dump(by_alias=True, exclude_none=True) if isinstance(user, User) else user
        data = self._post(self._PATH, json=payload)
        return User.model_validate(data)

    # ------------------------------------------------------------------
    # Single entity
    # ------------------------------------------------------------------

    def get(self, user_id: int, query: Optional[ODataQuery] = None) -> User:
        data = self._get(f"{self._PATH}({user_id})", params=self._query_params(query))
        return User.model_validate(data)

    def get_by_number(self, number: str, query: Optional[ODataQuery] = None) -> User:
        data = self._get(f"{self._PATH}(Number='{number}')", params=self._query_params(query))
        return User.model_validate(data)

    def update(self, user_id: int, changes: User | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, User) else changes
        self._patch(f"{self._PATH}({user_id})", json=payload)

    def delete(self, user_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PATH}({user_id})", etag=etag)

    # ------------------------------------------------------------------
    # Sub-resources
    # ------------------------------------------------------------------

    def get_groups(self, user_id: int) -> List[UserGroupRef]:
        data = self._get(f"{self._PATH}({user_id})/Groups")
        return [UserGroupRef.model_validate(item) for item in data.get("value", [])]

    def get_forwarding_profiles(self, user_id: int) -> List[ForwardingProfile]:
        data = self._get(f"{self._PATH}({user_id})/ForwardingProfiles")
        return [ForwardingProfile.model_validate(item) for item in data.get("value", [])]

    def get_greetings(self, user_id: int) -> List[Greeting]:
        data = self._get(f"{self._PATH}({user_id})/Greetings")
        return [Greeting.model_validate(item) for item in data.get("value", [])]

    # ------------------------------------------------------------------
    # Per-user actions
    # ------------------------------------------------------------------

    def send_welcome_email(self, user_id: int) -> None:
        self._post(f"{self._PATH}({user_id})/Pbx.SendWelcomeEmail")

    def make_call(self, user_id: int, destination: str) -> None:
        self._post(f"{self._PATH}({user_id})/Pbx.MakeCall", json={"Destination": destination})

    def generate_prov_link(self, user_id: int) -> str:
        data = self._get(f"{self._PATH}({user_id})/Pbx.GenerateProvLink()")
        return str(data.get("value", ""))

    def get_phone_secret(self, user_id: int) -> str:
        data = self._get(f"{self._PATH}({user_id})/Pbx.GetPhoneSecret()")
        return str(data.get("value", ""))

    def has_duplicated_email(self, user_id: int) -> bool:
        data = self._get(f"{self._PATH}({user_id})/Pbx.HasDuplicatedEmail()")
        return bool(data.get("value", data))

    def make_call_record_greeting(self, user_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}({user_id})/Pbx.MakeCallUserRecordGreeting", json=data)

    def regenerate(self, user_id: int) -> None:
        self._post(f"{self._PATH}({user_id})/Pbx.Regenerate")

    def set_monitor_status(self, user_id: int, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}({user_id})/Pbx.SetMonitorStatus", json=data)

    # ------------------------------------------------------------------
    # Collection-level actions
    # ------------------------------------------------------------------

    def batch_delete(self, user_ids: List[int]) -> None:
        self._post(f"{self._PATH}/Pbx.BatchDelete", json={"userIds": user_ids})

    def bulk_update(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.BulkUpdate", json=data)

    def multi_user_update(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.MultiUserUpdate", json=data)

    def regenerate_passwords(self) -> None:
        self._post(f"{self._PATH}/Pbx.RegeneratePasswords")

    def reprove_all_phones(self) -> None:
        self._post(f"{self._PATH}/Pbx.ReprovisionAllPhones")

    def install_firmware(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.InstallFirmware", json=data)

    def upgrade_phone(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.UpgradePhone", json=data)

    def multi_delete_greeting(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._PATH}/Pbx.MultiDeleteGreeting", json=data)

    def get_duplicated_emails(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post(f"{self._PATH}/Pbx.GetDuplicatedEmails", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def get_multi_edit_greetings(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post(f"{self._PATH}/Pbx.GetMultiEditGreetings", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def get_phone_registrars(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post(f"{self._PATH}/Pbx.GetPhoneRegistrars", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def get_phone_registrar(self, mac: str) -> Dict[str, Any]:
        return self._get(f"/Users/Pbx.GetPhoneRegistrar(mac='{mac}')")

    def get_first_available_extension(self) -> str:
        data = self._get(f"{self._PATH}/Pbx.GetFirstAvailableExtensionNumber()")
        return str(data.get("value", ""))

    def get_first_available_hotdesking_number(self) -> str:
        data = self._get(f"{self._PATH}/Pbx.GetFirstAvailableHotdeskingNumber()")
        return str(data.get("value", ""))

    def export_extensions(self) -> bytes:
        return self._get_bytes(f"{self._PATH}/Pbx.ExportExtensions()")

    def download_greeting(self, user_id: int, file_name: str) -> bytes:
        return self._get_bytes(f"{self._PATH}/Pbx.DownloadGreeting(userId={user_id},fileName='{file_name}')")
