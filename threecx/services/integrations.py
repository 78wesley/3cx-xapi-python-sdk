from __future__ import annotations

from typing import Any, Dict, List

from .base import BaseService


class IntegrationsService(BaseService):

    # ------------------------------------------------------------------
    # Microsoft 365
    # ------------------------------------------------------------------

    def get_m365(self) -> Dict[str, Any]:
        return self._get("/Microsoft365Integration")

    def update_m365(self, data: Dict[str, Any]) -> None:
        self._patch("/Microsoft365Integration", json=data)

    def test_m365_subscription(self) -> Dict[str, Any]:
        return self._get("/Microsoft365Integration/Pbx.TestSubscription()")

    def authorize_m365_presence(self, data: Dict[str, Any]) -> None:
        self._post("/Microsoft365Integration/Pbx.AuthorizePresence", json=data)

    def test_m365_presence(self, data: Dict[str, Any]) -> None:
        self._post("/Microsoft365Integration/Pbx.TestPresence", json=data)

    def deauthorize_m365_presence(self) -> None:
        self._post("/Microsoft365Integration/Pbx.DeauthorizePresence")

    def get_m365_access_token(self) -> str:
        data = self._get("/Microsoft365Integration/Pbx.GetMicrosoftAccessToken()")
        return str(data.get("value", ""))

    def get_m365_directory(self) -> Dict[str, Any]:
        return self._get("/Microsoft365Integration/Pbx.GetMicrosoft365Directory()")

    def get_m365_users(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post("/Microsoft365Integration/Pbx.GetM365Users", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def get_m365_groups(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post("/Microsoft365Integration/Pbx.GetM365Groups", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    def get_users_by_principal_names(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post("/Microsoft365Integration/Pbx.GetUsersByPrincipalNames", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    # ------------------------------------------------------------------
    # Microsoft Teams
    # ------------------------------------------------------------------

    def get_m365_teams(self) -> Dict[str, Any]:
        return self._get("/Microsoft365TeamsIntegration")

    def update_m365_teams(self, data: Dict[str, Any]) -> None:
        self._patch("/Microsoft365TeamsIntegration", json=data)

    def get_dial_plan_script(self) -> str:
        data = self._get("/Microsoft365TeamsIntegration/Pbx.GetDialPlanScript()")
        return str(data.get("value", ""))

    def get_map_users_script(self) -> str:
        data = self._get("/Microsoft365TeamsIntegration/Pbx.GetMapUsersScript()")
        return str(data.get("value", ""))

    def check_map_users_script(self) -> Dict[str, Any]:
        return self._get("/Microsoft365TeamsIntegration/Pbx.CheckMapUsersScript()")

    def check_fqdn_record(self, fqdn: str) -> Dict[str, Any]:
        return self._get(f"/Microsoft365TeamsIntegration/Pbx.CheckFqdnRecord(fqdn='{fqdn}')")

    # ------------------------------------------------------------------
    # Google
    # ------------------------------------------------------------------

    def get_google_settings(self) -> Dict[str, Any]:
        return self._get("/GoogleSettings")

    def update_google_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/GoogleSettings", json=data)

    def get_google_users(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        result = self._post("/GoogleSettings/Pbx.GetGoogleUsers", json=data)
        return self._list_values(result) if isinstance(result, dict) else result

    # ------------------------------------------------------------------
    # Amazon
    # ------------------------------------------------------------------

    def get_amazon_settings(self) -> Dict[str, Any]:
        return self._get("/AmazonIntegrationSettings")

    def update_amazon_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/AmazonIntegrationSettings", json=data)

    def generate_iam_policy_file(self) -> bytes:
        return self._get_bytes("/AmazonIntegrationSettings/Pbx.GenerateIamPolicyFile()")

    # ------------------------------------------------------------------
    # Data connector
    # ------------------------------------------------------------------

    def get_data_connector_settings(self) -> Dict[str, Any]:
        return self._get("/DataConnectorSettings")

    def update_data_connector_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/DataConnectorSettings", json=data)

    def synchronize_data_connector(self) -> None:
        self._post("/DataConnectorSettings/Pbx.Synchronize")

    def test_data_connector(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/DataConnectorSettings/Pbx.TestDataConnector", json=data)

    # ------------------------------------------------------------------
    # AI settings
    # ------------------------------------------------------------------

    def get_ai_settings(self) -> Dict[str, Any]:
        return self._get("/AISettings")

    def update_ai_settings(self, data: Dict[str, Any]) -> None:
        self._patch("/AISettings", json=data)

    def get_ai_resources(self) -> Dict[str, Any]:
        return self._get("/AISettings/Pbx.GetAIResources()")

    def get_ai_template_contents(self, template_id: str) -> str:
        data = self._get(f"/AISettings/Pbx.GetAITemplateContents(id='{template_id}')")
        return str(data.get("value", ""))

    def get_vector_stores(self, limit: int = 20, after: str = "") -> Dict[str, Any]:
        return self._get(f"/AISettings/Pbx.GetVectorStores(limit={limit},after='{after}')")

    def get_vector_store(self, store_id: str) -> Dict[str, Any]:
        return self._get(f"/AISettings/Pbx.GetVectorStore(id='{store_id}')")

    def get_vector_store_files(self, store_id: str, limit: int = 20, after: str = "") -> Dict[str, Any]:
        return self._get(f"/AISettings/Pbx.GetVectorStoreFiles(id='{store_id}',limit={limit},after='{after}')")

    def create_vector_store(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/AISettings/Pbx.CreateVectorStore", json=data)

    def update_vector_store(self, data: Dict[str, Any]) -> None:
        self._post("/AISettings/Pbx.UpdateVectorStore", json=data)

    def delete_vector_store(self, data: Dict[str, Any]) -> None:
        self._post("/AISettings/Pbx.DeleteVectorStore", json=data)

    def delete_vector_store_file(self, data: Dict[str, Any]) -> None:
        self._post("/AISettings/Pbx.DeleteVectorStoreFile", json=data)

    def delete_openai_file(self, data: Dict[str, Any]) -> None:
        self._post("/AISettings/Pbx.DeleteOpenAiFile", json=data)

    def add_vector_store_files(self, data: Dict[str, Any]) -> None:
        self._post("/AISettings/Pbx.AddVectorStoreFiles", json=data)
