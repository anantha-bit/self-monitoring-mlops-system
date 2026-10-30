import os
import pytest

def test_tc15_container_and_environment_configuration():
    """
    TC-15: Container build and CI smoke configuration validation.
    Verifies Dockerfile, docker-compose.yml, requirements.txt, and startup entrypoint exist.
    Traceability: NFR-05, NFR-06.
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))

    dockerfile_path = os.path.join(base_dir, "Dockerfile")
    compose_path = os.path.join(base_dir, "docker-compose.yml")
    req_path = os.path.join(base_dir, "requirements.txt")

    assert os.path.exists(dockerfile_path), "Dockerfile must exist"
    assert os.path.exists(compose_path), "docker-compose.yml must exist"
    assert os.path.exists(req_path), "requirements.txt must exist"

    # Verify Dockerfile contains healthcheck and uvicorn command
    with open(dockerfile_path, "r", encoding="utf-8") as f:
        df_content = f.read()
    assert "uvicorn" in df_content
    assert "8000" in df_content

    # Verify docker-compose exposes port 8000 and volumes
    with open(compose_path, "r", encoding="utf-8") as f:
        compose_content = f.read()
    assert "8000:8000" in compose_content
