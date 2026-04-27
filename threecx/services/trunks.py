from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.trunks import Peer, Sbc, Trunk, TrunkTemplate
from ..odata import ODataQuery
from .base import BaseService


class TrunksService(BaseService):
    _TRUNKS = "/Trunks"
    _TRUNK_TEMPLATES = "/TrunkTemplates"
    _PEERS = "/Peers"
    _SBCS = "/Sbcs"

    # ------------------------------------------------------------------
    # Trunks
    # ------------------------------------------------------------------

    def list_trunks(self, query: Optional[ODataQuery] = None) -> List[Trunk]:
        data = self._list_raw(self._TRUNKS, query)
        return [Trunk.model_validate(item) for item in data.get("value", [])]

    def iterate_trunks(self, query: Optional[ODataQuery] = None) -> Iterator[Trunk]:
        yield from self._paginate(self._TRUNKS, Trunk, query)

    def create_trunk(self, trunk: Trunk | Dict[str, Any]) -> Trunk:
        payload = trunk.model_dump(by_alias=True, exclude_none=True) if isinstance(trunk, Trunk) else trunk
        data = self._post(self._TRUNKS, json=payload)
        return Trunk.model_validate(data)

    def get_trunk(self, trunk_id: int, query: Optional[ODataQuery] = None) -> Trunk:
        data = self._get(f"{self._TRUNKS}({trunk_id})", params=self._query_params(query))
        return Trunk.model_validate(data)

    def get_trunk_by_number(self, number: str, query: Optional[ODataQuery] = None) -> Trunk:
        data = self._get(f"{self._TRUNKS}(Number='{number}')", params=self._query_params(query))
        return Trunk.model_validate(data)

    def update_trunk(self, trunk_id: int, changes: Trunk | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Trunk) else changes
        self._patch(f"{self._TRUNKS}({trunk_id})", json=payload)

    def delete_trunk(self, trunk_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._TRUNKS}({trunk_id})", etag=etag)

    def get_first_available_trunk_number(self) -> str:
        data = self._get(f"{self._TRUNKS}/Pbx.GetFirstAvailableTrunkNumber()")
        return str(data.get("value", ""))

    def init_master_bridge(self) -> Dict[str, Any]:
        return self._get(f"{self._TRUNKS}/Pbx.InitMasterBridge()")

    def init_slave_bridge(self) -> Dict[str, Any]:
        return self._get(f"{self._TRUNKS}/Pbx.InitSlaveBridge()")

    def init_trunk(self, template: str) -> Dict[str, Any]:
        return self._get(f"{self._TRUNKS}/Pbx.InitTrunk(template='{template}')")

    def refresh_registration(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._TRUNKS}/Pbx.RefreshRegistration", json=data)

    def set_routes(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._TRUNKS}/Pbx.SetRoutes", json=data)

    def finalize_trunk_provisioning(self, data: Dict[str, Any]) -> None:
        self._post(f"{self._TRUNKS}/Pbx.FinalizeTrunkProvisioning", json=data)

    def get_provider_phones(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post(f"{self._TRUNKS}/Pbx.GetProviderPhones", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def export_trunk(self, trunk_id: int) -> bytes:
        return self._get_bytes(f"{self._TRUNKS}({trunk_id})/Pbx.ExportTrunk()")

    def run_analysis(self, trunk_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"{self._TRUNKS}({trunk_id})/Pbx.RunAnalysis", json=data)

    def test_inbound_call(self, trunk_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"{self._TRUNKS}({trunk_id})/Pbx.TestInboundCall", json=data)

    def test_outbound_call(self, trunk_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"{self._TRUNKS}({trunk_id})/Pbx.TestOutboundCall", json=data)

    # ------------------------------------------------------------------
    # Trunk templates
    # ------------------------------------------------------------------

    def list_trunk_templates(self, query: Optional[ODataQuery] = None) -> List[TrunkTemplate]:
        data = self._list_raw(self._TRUNK_TEMPLATES, query)
        return [TrunkTemplate.model_validate(item) for item in data.get("value", [])]

    def create_trunk_template(self, tmpl: TrunkTemplate | Dict[str, Any]) -> TrunkTemplate:
        payload = tmpl.model_dump(by_alias=True, exclude_none=True) if isinstance(tmpl, TrunkTemplate) else tmpl
        data = self._post(self._TRUNK_TEMPLATES, json=payload)
        return TrunkTemplate.model_validate(data)

    def get_trunk_template(self, template_id: int) -> TrunkTemplate:
        data = self._get(f"{self._TRUNK_TEMPLATES}({template_id})")
        return TrunkTemplate.model_validate(data)

    def update_trunk_template(self, template_id: int, changes: TrunkTemplate | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, TrunkTemplate) else changes
        self._patch(f"{self._TRUNK_TEMPLATES}({template_id})", json=payload)

    def delete_trunk_template(self, template_id: int) -> None:
        self._delete(f"{self._TRUNK_TEMPLATES}({template_id})")

    # ------------------------------------------------------------------
    # Peers
    # ------------------------------------------------------------------

    def list_peers(self, query: Optional[ODataQuery] = None) -> List[Peer]:
        data = self._list_raw(self._PEERS, query)
        return [Peer.model_validate(item) for item in data.get("value", [])]

    def get_peer(self, peer_id: int, query: Optional[ODataQuery] = None) -> Peer:
        data = self._get(f"{self._PEERS}({peer_id})", params=self._query_params(query))
        return Peer.model_validate(data)

    def get_peer_by_number(self, number: str) -> Peer:
        data = self._get(f"{self._PEERS}(Number='{number}')")
        return Peer.model_validate(data)

    def create_peer(self, peer: Peer | Dict[str, Any]) -> Peer:
        payload = peer.model_dump(by_alias=True, exclude_none=True) if isinstance(peer, Peer) else peer
        data = self._post(self._PEERS, json=payload)
        return Peer.model_validate(data)

    def update_peer(self, peer_id: int, changes: Peer | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Peer) else changes
        self._patch(f"{self._PEERS}({peer_id})", json=payload)

    def delete_peer(self, peer_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._PEERS}({peer_id})", etag=etag)

    def get_report_peers(self) -> List[Dict[str, Any]]:
        data = self._get(f"{self._PEERS}/Pbx.GetReportPeers()")
        return self._list_values(data) if isinstance(data, dict) else data

    def retrieve_peers_by_numbers(self, data: Dict[str, Any]) -> List[Peer]:
        result = self._post(f"{self._PEERS}/Pbx.RetreivePeersByNumbers", json=data)
        items = result.get("value", result) if isinstance(result, dict) else result
        return [Peer.model_validate(item) for item in items]

    # ------------------------------------------------------------------
    # SBCs
    # ------------------------------------------------------------------

    def list_sbcs(self, query: Optional[ODataQuery] = None) -> List[Sbc]:
        data = self._list_raw(self._SBCS, query)
        return [Sbc.model_validate(item) for item in data.get("value", [])]

    def get_sbc(self, sbc_name: str, query: Optional[ODataQuery] = None) -> Sbc:
        data = self._get(f"{self._SBCS}('{sbc_name}')", params=self._query_params(query))
        return Sbc.model_validate(data)

    def create_sbc(self, sbc: Sbc | Dict[str, Any]) -> Sbc:
        payload = sbc.model_dump(by_alias=True, exclude_none=True) if isinstance(sbc, Sbc) else sbc
        data = self._post(self._SBCS, json=payload)
        return Sbc.model_validate(data)

    def update_sbc(self, sbc_name: str, changes: Sbc | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Sbc) else changes
        self._patch(f"{self._SBCS}('{sbc_name}')", json=payload)

    def delete_sbc(self, sbc_name: str) -> None:
        self._delete(f"{self._SBCS}('{sbc_name}')")

    def push_sbc_config(self, sbc_name: str) -> None:
        self._post(f"{self._SBCS}('{sbc_name}')/Pbx.PushConfig")
