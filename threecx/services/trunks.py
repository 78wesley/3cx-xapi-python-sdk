from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from ..models.trunks import Peer, Sbc, Trunk
from ..odata import ODataQuery
from .base import BaseService


class TrunksService(BaseService):
    """CRUD operations for trunks, peers, and SBCs.

    Reference paths:
      GET    /Trunks
      POST   /Trunks
      GET    /Trunks({Id})
      PATCH  /Trunks({Id})
      DELETE /Trunks({Id})
      GET    /Peers
      POST   /Peers
      GET    /Peers({Id})
      PATCH  /Peers({Id})
      DELETE /Peers({Id})
      GET    /Sbcs
    """

    _TRUNKS = "/Trunks"
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

    def update_trunk(self, trunk_id: int, changes: Trunk | Dict[str, Any]) -> None:
        payload = changes.model_dump(by_alias=True, exclude_none=True) if isinstance(changes, Trunk) else changes
        self._patch(f"{self._TRUNKS}({trunk_id})", json=payload)

    def delete_trunk(self, trunk_id: int, etag: Optional[str] = None) -> None:
        self._delete(f"{self._TRUNKS}({trunk_id})", etag=etag)

    # ------------------------------------------------------------------
    # Peers
    # ------------------------------------------------------------------

    def list_peers(self, query: Optional[ODataQuery] = None) -> List[Peer]:
        data = self._list_raw(self._PEERS, query)
        return [Peer.model_validate(item) for item in data.get("value", [])]

    def get_peer(self, peer_id: int, query: Optional[ODataQuery] = None) -> Peer:
        data = self._get(f"{self._PEERS}({peer_id})", params=self._query_params(query))
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

    # ------------------------------------------------------------------
    # SBCs (read-only in most deployments)
    # ------------------------------------------------------------------

    def list_sbcs(self, query: Optional[ODataQuery] = None) -> List[Sbc]:
        data = self._list_raw(self._SBCS, query)
        return [Sbc.model_validate(item) for item in data.get("value", [])]

    def get_sbc(self, sbc_id: int, query: Optional[ODataQuery] = None) -> Sbc:
        data = self._get(f"{self._SBCS}({sbc_id})", params=self._query_params(query))
        return Sbc.model_validate(data)
