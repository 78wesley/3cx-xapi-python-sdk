from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..odata import ODataQuery
from .base import BaseService


class SecurityService(BaseService):

    # ------------------------------------------------------------------
    # Security tokens (admin view of all sessions)
    # ------------------------------------------------------------------

    def list_security_tokens(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/SecurityTokens", query)
        return self._list_values(data)

    def revoke_security_token(self, token_id: int) -> None:
        self._post(f"/SecurityTokens({token_id})/Pbx.RevokeToken")

    # ------------------------------------------------------------------
    # My tokens (current user's own sessions)
    # ------------------------------------------------------------------

    def list_my_tokens(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/MyTokens", query)
        return self._list_values(data)

    def revoke_my_token(self, token_id: int) -> None:
        self._post(f"/MyTokens({token_id})/Pbx.RevokeToken")

    # ------------------------------------------------------------------
    # Service principals
    # ------------------------------------------------------------------

    def list_service_principals(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/ServicePrincipals", query)
        return self._list_values(data)

    def create_service_principal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/ServicePrincipals", json=data)

    def get_service_principal(self, sp_id: int) -> Dict[str, Any]:
        return self._get(f"/ServicePrincipals({sp_id})")

    def update_service_principal(self, sp_id: int, changes: Dict[str, Any]) -> None:
        self._patch(f"/ServicePrincipals({sp_id})", json=changes)

    def delete_service_principal(self, sp_id: int) -> None:
        self._delete(f"/ServicePrincipals({sp_id})")

    def generate_app_token(self, sp_id: int) -> str:
        data = self._post(f"/ServicePrincipals({sp_id})/Pbx.GenerateAppToken")
        return str(data.get("value", "")) if isinstance(data, dict) else data

    # ------------------------------------------------------------------
    # Blacklist numbers (blocked callers)
    # ------------------------------------------------------------------

    def list_blacklist_numbers(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/BlackListNumbers", query)
        return self._list_values(data)

    def create_blacklist_number(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/BlackListNumbers", json=data)

    def get_blacklist_number(self, num_id: int) -> Dict[str, Any]:
        return self._get(f"/BlackListNumbers({num_id})")

    def update_blacklist_number(self, num_id: int, changes: Dict[str, Any]) -> None:
        self._patch(f"/BlackListNumbers({num_id})", json=changes)

    def delete_blacklist_number(self, num_id: int) -> None:
        self._delete(f"/BlackListNumbers({num_id})")

    def bulk_delete_blacklist_numbers(self, data: Dict[str, Any]) -> None:
        self._post("/BlackListNumbers/Pbx.BulkNumbersDelete", json=data)

    # ------------------------------------------------------------------
    # IP blocklist
    # ------------------------------------------------------------------

    def list_blocklist(self, query: Optional[ODataQuery] = None) -> List[Dict[str, Any]]:
        data = self._list_raw("/Blocklist", query)
        return self._list_values(data)

    def create_blocklist(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/Blocklist", json=data)

    def get_blocklist_entry(self, entry_id: int) -> Dict[str, Any]:
        return self._get(f"/Blocklist({entry_id})")

    def update_blocklist_entry(self, entry_id: int, changes: Dict[str, Any]) -> None:
        self._patch(f"/Blocklist({entry_id})", json=changes)

    def delete_blocklist_entry(self, entry_id: int) -> None:
        self._delete(f"/Blocklist({entry_id})")

    def bulk_delete_blocklist_ips(self, data: Dict[str, Any]) -> None:
        self._post("/Blocklist/Pbx.BulkIpsDelete", json=data)

    # ------------------------------------------------------------------
    # Anti-hacking settings
    # ------------------------------------------------------------------

    def get_anti_hacking_settings(self) -> Dict[str, Any]:
        return self._get("/AntiHackingSettings")

    def update_anti_hacking_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/AntiHackingSettings", json=data)

    # ------------------------------------------------------------------
    # Firewall check
    # ------------------------------------------------------------------

    def get_firewall_state(self) -> Dict[str, Any]:
        return self._get("/Firewall")

    def get_firewall_last_result(self) -> Dict[str, Any]:
        return self._get("/Firewall/Pbx.GetLastResult()")

    def start_firewall_check(self) -> None:
        self._post("/Firewall/Pbx.StartCheck")

    def stop_firewall_check(self) -> None:
        self._post("/Firewall/Pbx.StopCheck")
