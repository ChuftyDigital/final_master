"""ComfyUI API client with HTTP + WebSocket support for real-time progress tracking."""

import json
import time
import uuid
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests
import websocket

logger = logging.getLogger("superfactory.comfyui")


class ComfyUIClient:
    """Full-featured ComfyUI API client with WebSocket progress tracking."""

    def __init__(
        self,
        server: str = "127.0.0.1:8188",
        protocol: str = "http",
        timeout: int = 300,
        verify_ssl: bool = False,
        max_retries: int = 3,
    ):
        self.server = server
        self.base_url = f"{protocol}://{server}"
        ws_proto = "wss" if protocol == "https" else "ws"
        self.ws_url = f"{ws_proto}://{server}/ws"
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.max_retries = max_retries
        self.client_id = str(uuid.uuid4())
        self._session = requests.Session()
        self._session.verify = verify_ssl

    def test_connection(self) -> bool:
        """Test if ComfyUI server is reachable."""
        try:
            resp = self._session.get(
                f"{self.base_url}/system_stats", timeout=10
            )
            if resp.status_code == 200:
                stats = resp.json()
                version = stats.get("system", {}).get("comfyui_version", "unknown")
                logger.info(f"Connected to ComfyUI v{version} at {self.server}")
                return True
        except Exception as e:
            logger.error(f"Cannot connect to ComfyUI at {self.server}: {e}")
        return False

    def get_system_stats(self) -> Dict[str, Any]:
        """Get system stats including GPU info."""
        resp = self._session.get(f"{self.base_url}/system_stats", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def queue_prompt(self, workflow: Dict[str, Any]) -> str:
        """Queue a workflow for execution. Returns the prompt_id."""
        payload = {"prompt": workflow, "client_id": self.client_id}
        resp = self._session.post(
            f"{self.base_url}/prompt",
            json=payload,
            timeout=30,
        )
        if resp.status_code >= 400:
            # Log the full error body from ComfyUI before raising
            try:
                error_data = resp.json()
                error_msg = json.dumps(error_data, indent=2)[:2000]
            except Exception:
                error_msg = resp.text[:2000]
            logger.error(f"ComfyUI rejected workflow ({resp.status_code}):\n{error_msg}")
        resp.raise_for_status()
        return resp.json()["prompt_id"]

    def get_history(self, prompt_id: str) -> Dict[str, Any]:
        """Get execution history for a prompt."""
        resp = self._session.get(
            f"{self.base_url}/history/{prompt_id}", timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """Download a generated image from ComfyUI."""
        params = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        resp = self._session.get(
            f"{self.base_url}/view", params=params, timeout=60
        )
        resp.raise_for_status()
        return resp.content

    def get_queue(self) -> Dict[str, Any]:
        """Get the current queue status."""
        resp = self._session.get(f"{self.base_url}/queue", timeout=10)
        resp.raise_for_status()
        return resp.json()

    def cancel_current(self):
        """Cancel the currently running prompt."""
        self._session.post(
            f"{self.base_url}/interrupt", timeout=10
        )

    def clear_queue(self):
        """Clear all queued prompts."""
        self._session.post(
            f"{self.base_url}/queue",
            json={"clear": True},
            timeout=10,
        )

    def generate_and_wait(
        self,
        workflow: Dict[str, Any],
        on_progress: callable = None,
    ) -> Dict[str, Any]:
        """Queue a workflow, wait for completion via WebSocket, return outputs.

        Args:
            workflow: The ComfyUI API workflow dict.
            on_progress: Optional callback(value, max_value, node_id) for progress.

        Returns:
            Dict with prompt_id and output images info.
        """
        prompt_id = self.queue_prompt(workflow)
        logger.debug(f"Queued prompt: {prompt_id}")

        # Try WebSocket-based waiting first, fall back to polling
        try:
            self._wait_ws(prompt_id, on_progress)
        except RuntimeError:
            # Execution errors from ComfyUI — re-raise, don't swallow
            raise
        except Exception as e:
            logger.debug(f"WebSocket unavailable ({e}), falling back to polling")
            self._wait_poll(prompt_id)

        # Fetch results
        history = self.get_history(prompt_id)
        if prompt_id not in history:
            raise RuntimeError(f"Prompt {prompt_id} not found in history after completion")

        prompt_result = history[prompt_id]
        status = prompt_result.get("status", {})
        if status.get("status_str") == "error":
            msgs = status.get("messages", [])
            error_detail = ""
            for msg in msgs:
                if isinstance(msg, list) and len(msg) >= 2:
                    error_detail += f" {msg[0]}: {msg[1]}"
            raise RuntimeError(f"ComfyUI execution failed:{error_detail}")

        return {"prompt_id": prompt_id, "outputs": prompt_result.get("outputs", {})}

    def _wait_ws(self, prompt_id: str, on_progress: callable = None):
        """Wait for prompt completion using WebSocket."""
        ws = websocket.create_connection(
            f"{self.ws_url}?clientId={self.client_id}",
            timeout=self.timeout,
            sslopt={"cert_reqs": 0} if not self.verify_ssl else {},
        )
        try:
            while True:
                msg = ws.recv()
                if isinstance(msg, str):
                    data = json.loads(msg)
                    msg_type = data.get("type")

                    if msg_type == "executing":
                        exec_data = data.get("data", {})
                        if exec_data.get("prompt_id") == prompt_id:
                            if exec_data.get("node") is None:
                                # Execution complete
                                return

                    elif msg_type == "progress" and on_progress:
                        prog = data.get("data", {})
                        on_progress(
                            prog.get("value", 0),
                            prog.get("max", 0),
                            prog.get("node", ""),
                        )

                    elif msg_type == "execution_error":
                        err = data.get("data", {})
                        raise RuntimeError(
                            f"ComfyUI execution error: {err.get('exception_message', 'unknown')}"
                        )
        finally:
            ws.close()

    def _wait_poll(self, prompt_id: str):
        """Fallback: wait for prompt completion by polling history."""
        waited = 0
        interval = 2
        while waited < self.timeout:
            try:
                history = self.get_history(prompt_id)
                if prompt_id in history:
                    status = history[prompt_id].get("status", {})
                    if status.get("completed", False) or "outputs" in history[prompt_id]:
                        return
            except Exception:
                pass
            time.sleep(interval)
            waited += interval

        raise TimeoutError(f"Prompt {prompt_id} timed out after {self.timeout}s")

    def save_images_from_output(
        self,
        outputs: Dict[str, Any],
        output_dir: Path,
        prefix: str = "",
    ) -> list:
        """Download and save all images from a generation output.

        Returns list of saved file paths.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        saved = []

        for node_id, node_output in outputs.items():
            if "images" not in node_output:
                continue
            for img_info in node_output["images"]:
                filename = img_info["filename"]
                subfolder = img_info.get("subfolder", "")
                folder_type = img_info.get("type", "output")

                image_data = self.get_image(filename, subfolder, folder_type)
                save_name = f"{prefix}{filename}" if prefix else filename
                save_path = output_dir / save_name

                with open(save_path, "wb") as f:
                    f.write(image_data)

                saved.append(save_path)
                logger.debug(f"Saved: {save_path} ({len(image_data) / 1024:.1f} KB)")

        return saved
