# Create necessary directories
New-Item -ItemType Directory -Force -Path "multi_agent_project"
New-Item -ItemType Directory -Force -Path "multiagentapi"
New-Item -ItemType Directory -Force -Path "agents"
New-Item -ItemType Directory -Force -Path "frontend"

# Copy Python files and directories
Copy-Item -Path "../MULTIAGENT/multi_agent_project/*" -Destination "multi_agent_project/" -Recurse -Force
Copy-Item -Path "../MULTIAGENT/multiagentapi/*" -Destination "multiagentapi/" -Recurse -Force
Copy-Item -Path "../MULTIAGENT/agents/*" -Destination "agents/" -Recurse -Force

# Copy frontend files (excluding node_modules)
Copy-Item -Path "../MULTIAGENT/frontend/src" -Destination "frontend/" -Recurse -Force
Copy-Item -Path "../MULTIAGENT/frontend/public" -Destination "frontend/" -Recurse -Force
Copy-Item -Path "../MULTIAGENT/frontend/package.json" -Destination "frontend/" -Force
Copy-Item -Path "../MULTIAGENT/frontend/package-lock.json" -Destination "frontend/" -Force
Copy-Item -Path "../MULTIAGENT/frontend/tsconfig.json" -Destination "frontend/" -Force

# Copy root level files
Copy-Item -Path "../MULTIAGENT/server.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/README.md" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/run.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/build_frontend.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/requirements.txt" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/main.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/test_server.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/test_api.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/manage.py" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/redis.windows.conf" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/fix_redis.ps1" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/setup_redis_user.ps1" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/setup_redis.ps1" -Destination "." -Force
Copy-Item -Path "../MULTIAGENT/redis.conf" -Destination "." -Force 