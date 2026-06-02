from flask import Flask, request, jsonify
import requests
import json
import threading
import logging
import traceback
import docker
from typing import Dict, Optional

class ReverseProxy:
    def __init__(self, config_path: str = "config.json"):
        # Setup logging first with more detailed format
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize other attributes
        self.app = Flask(__name__)
        self.config_path = config_path
        self.endpoints: Dict[str, str] = {}
        self.config_lock = threading.Lock()
        
        try:
            self.docker_client = docker.from_env()
            self.logger.info("Successfully connected to Docker daemon")
        except Exception as e:
            self.logger.error(f"Failed to connect to Docker daemon: {str(e)}")
            self.docker_client = None
        
        # Load configuration before setting up routes
        self.load_config()
        
        # Setup routes
        self.setup_routes()

    def setup_routes(self):
        """Setup all Flask routes."""
        self.app.route('/<path:endpoint>', methods=['GET', 'POST'])(self.proxy_request)
        self.app.route('/admin/endpoints', methods=['GET'])(self.list_endpoints)
        self.app.route('/admin/register', methods=['POST'])(self.register_endpoint)
        self.app.route('/admin/remove', methods=['POST'])(self.remove_endpoint)
        self.app.route('/', methods=['GET'])(self.health_check)
        self.app.route('/admin/update-service', methods=['POST'])(self.update_service)

    def health_check(self):
        """Simple health check endpoint."""
        return jsonify({"status": "healthy", "endpoints": len(self.endpoints)})

    def load_config(self) -> None:
        """Load endpoint configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                with self.config_lock:
                    self.endpoints = json.load(f)
            self.logger.info(f"Loaded configuration with {len(self.endpoints)} endpoints: {self.endpoints}")
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}\n{traceback.format_exc()}")
            self.endpoints = {}

    def save_config(self) -> None:
        """Save current endpoint configuration to JSON file."""
        try:
            with open(self.config_path, 'w') as f:
                with self.config_lock:
                    json.dump(self.endpoints, f, indent=4)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")

    def list_endpoints(self):
        """List all registered endpoints."""
        with self.config_lock:
            return jsonify(self.endpoints)

    def register_endpoint(self):
        """Register a new endpoint."""
        data = request.get_json()
        if not data or 'name' not in data or 'url' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        with self.config_lock:
            self.endpoints[data['name']] = data['url']
            self.save_config()

        return jsonify({"message": "Endpoint registered successfully"})

    def remove_endpoint(self):
        """Remove an endpoint."""
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({"error": "Missing endpoint name"}), 400

        with self.config_lock:
            if data['name'] in self.endpoints:
                del self.endpoints[data['name']]
                self.save_config()
                return jsonify({"message": "Endpoint removed successfully"})
            else:
                return jsonify({"error": "Endpoint not found"}), 404

    def update_service(self):
        """
        Update a service with a new Docker container.
        Expected JSON payload:
        {
            "service_name": "my-service",
            "image": "nginx:latest",
            "container_name": "my-service-container",
            "port": 8080,
            "env": {"KEY": "VALUE"} // optional
        }
        """
        if not self.docker_client:
            return jsonify({"error": "Docker client not available"}), 503
            
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['service_name', 'image', 'container_name', 'port']):
                return jsonify({"error": "Missing required fields"}), 400

            service_name = data['service_name']
            image = data['image']
            container_name = data['container_name']
            port = data['port']
            env = data.get('env', {})

            # Pull the latest image
            self.logger.info(f"Pulling image: {image}")
            self.docker_client.images.pull(image)

            # Stop and remove the existing container if it exists
            try:
                existing_container = self.docker_client.containers.get(container_name)
                self.logger.info(f"Stopping existing container: {container_name}")
                existing_container.stop()
                self.logger.info(f"Removing container: {container_name}")
                existing_container.remove()
            except docker.errors.NotFound:
                self.logger.info(f"No existing container found: {container_name}")

            # Create and start the new container
            self.logger.info(f"Creating new container: {container_name}")
            container = self.docker_client.containers.run(
                image=image,
                name=container_name,
                environment=env,
                ports={f'{port}/tcp': port},
                detach=True,
                restart_policy={"Name": "always"}
            )

            # Update the proxy endpoint
            with self.config_lock:
                self.endpoints[service_name] = f"http://localhost:{port}"
                self.save_config()

            return jsonify({
                "message": "Service updated successfully",
                "container_id": container.id,
                "endpoint": f"http://localhost:{port}"
            })

        except docker.errors.ImageNotFound:
            error_msg = f"Docker image not found: {image}"
            self.logger.error(error_msg)
            return jsonify({"error": error_msg}), 404

        except docker.errors.APIError as e:
            error_msg = f"Docker API error: {str(e)}"
            self.logger.error(error_msg)
            return jsonify({"error": error_msg}), 500

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({"error": error_msg}), 500

    def proxy_request(self, endpoint: str):
        """Handle incoming proxy requests."""
        try:
            self.logger.info(f"Received request for endpoint: {endpoint}")
            self.logger.info(f"Request method: {request.method}")
            
            with self.config_lock:
                target_url = self.endpoints.get(endpoint)

            if not target_url:
                self.logger.error(f"Endpoint not found: {endpoint}")
                return jsonify({"error": f"Endpoint '{endpoint}' not found"}), 404

            # Ensure the target URL ends with the query string if present
            full_url = f"{target_url.rstrip('/')}"
            if request.query_string:
                full_url += f"?{request.query_string.decode('utf-8')}"

            self.logger.info(f"Forwarding request to: {full_url}")

            # Forward the request method, headers, and data
            headers = {k: v for k, v in request.headers.items() 
                      if k.lower() not in ['host', 'content-length']}
            
            # Get request data based on content type
            data = None
            if request.is_json:
                data = request.get_json()
            else:
                data = request.get_data()

            response = requests.request(
                method=request.method,
                url=full_url,
                headers=headers,
                json=data if request.is_json else None,
                data=None if request.is_json else data,
                timeout=30
            )

            self.logger.info(f"Response status code: {response.status_code}")

            # Return the proxied response
            return response.content, response.status_code, dict(response.headers).items()

        except requests.exceptions.RequestException as e:
            error_msg = f"Proxy error for {endpoint}: {str(e)}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({
                "error": "Proxy request failed",
                "details": str(e),
                "target_url": target_url
            }), 502

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            return jsonify({
                "error": "Internal server error",
                "details": str(e)
            }), 500

    def run(self, host: str = '0.0.0.0', port: int = 80, debug: bool = False):
        """Run the proxy server."""
        self.logger.info(f"Starting proxy server on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    proxy = ReverseProxy()
    proxy.run()