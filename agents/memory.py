from typing import Dict, Any, Optional, List
import json
import redis
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


class Memory:
    def __init__(self, memory_type: str = "redis"):
        """
        Initialize memory storage.
        
        Args:
            memory_type: Type of memory storage ('memory' or 'redis')
        """
        self.memory_type = memory_type
        self.memory_store: Dict[str, Any] = {}
        self.redis_url: Optional[str] = None
        
        if memory_type == "redis":
            try:
                # Try to use local Redis configuration first
                redis_conf = os.getenv("REDIS_CONF")
                if redis_conf and os.path.exists(redis_conf):
                    print(f"Using Redis configuration from: {redis_conf}")
                
                self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
                self.redis_client = redis.from_url(self.redis_url)
                # Test connection
                self.redis_client.ping()
                print("Successfully connected to Redis")
            except redis.ConnectionError as e:
                print(f"Redis connection failed: {str(e)}")
                print("Falling back to in-memory storage")
                self.memory_type = "memory"
        self.memory = {}

    def store(self, key: str, value: Any) -> None:
        """Store a value in memory with timestamp."""
        data = {"value": value, "timestamp": datetime.utcnow().isoformat()}

        if self.memory_type == "redis":
            self.redis_client.set(key, json.dumps(data))
        else:
            self.memory[key] = data

    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve a value from memory."""
        if self.memory_type == "redis":
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)["value"]
        else:
            if key in self.memory:
                return self.memory[key]["value"]
        return None

    def store_context(self, job_id: str, context: Dict[str, Any]) -> None:
        """Store processing context for a job."""
        self.store(f"context:{job_id}", context)

    def get_context(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve processing context for a job."""
        return self.retrieve(f"context:{job_id}")

    def store_extraction(
        self, job_id: str, agent_type: str, data: Dict[str, Any]
    ) -> None:
        """Store extracted data from an agent."""
        key = f"extraction:{job_id}:{agent_type}"
        self.store(key, data)

    def get_extraction(self, job_id: str, agent_type: str) -> Optional[Dict[str, Any]]:
        """Retrieve extracted data from an agent."""
        key = f"extraction:{job_id}:{agent_type}"
        return self.retrieve(key)

    def store_action(self, job_id: str, action: Dict[str, Any]) -> None:
        """Store an action taken for a job."""
        key = f"action:{job_id}"
        self.store(key, action)

    def get_action(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the action taken for a job."""
        key = f"action:{job_id}"
        return self.retrieve(key)

    def store_decision_trace(self, job_id: str, trace: List[Dict[str, Any]]) -> None:
        """Store the decision trace for a job."""
        key = f"trace:{job_id}"
        self.store(key, trace)

    def get_decision_trace(self, job_id: str) -> Optional[List[Dict[str, Any]]]:
        """Retrieve the decision trace for a job."""
        key = f"trace:{job_id}"
        return self.retrieve(key)

    def clear_job_data(self, job_id: str) -> None:
        """Clear all data associated with a job."""
        if self.memory_type == "redis":
            pattern = f"*:{job_id}:*"
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        else:
            keys_to_delete = [k for k in self.memory.keys() if job_id in k]
            for key in keys_to_delete:
                del self.memory[key]
