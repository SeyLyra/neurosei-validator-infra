# NeuroSei Testnet Deployment Guide

One-click deployment for NeuroSei validator infrastructure on SEI testnet.

## 🚀 Quick Deploy

```bash
# Clone and deploy
git clone https://github.com/your-org/neurosei-tooling-infra.git
cd neurosei-tooling-infra
./deploy.sh
```

## 📋 Prerequisites

- Ubuntu 20.04+ or macOS
- Docker and Docker Compose
- 8GB+ RAM, 4+ CPU cores
- SEI testnet validator account

## 🔧 Manual Setup

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Install Python
sudo apt install python3 python3-pip python3-venv

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Configure Validator

```bash
# Create validator config
mkdir -p ~/.neurosei
cat > ~/.neurosei/config.toml << EOF
[validator]
name = "neurosei-validator"
chain_id = "sei-testnet-1"
rpc_endpoint = "https://rpc.testnet.sei.io"
grpc_endpoint = "https://grpc.testnet.sei.io"

[ai]
model_path = "/opt/neurosei/models/validator-ai"
optimization_enabled = true
anomaly_detection = true

[zk_proofs]
ezkl_enabled = true
circuit_path = "/opt/neurosei/circuits/validator.circuit"

[payment]
sei_address = "sei1your-validator-address"
fee_collection_enabled = true
auto_optimization = true
EOF
```

### 3. Deploy Components

```bash
# Build and start validator core
cd validator-core
cargo build --release
sudo cp target/release/neurosei-validator-core /usr/local/bin/

# Install Python SDK
cd ../python-sdk
pip3 install -e .

# Setup dashboard
cd ../dashboard
npm install
npm run build

# Create systemd service
sudo tee /etc/systemd/system/neurosei-validator.service << EOF
[Unit]
Description=NeuroSei Validator Core
After=network.target

[Service]
Type=simple
User=neurosei
ExecStart=/usr/local/bin/neurosei-validator-core
Restart=always
RestartSec=10
Environment=RUST_LOG=info

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable neurosei-validator
sudo systemctl start neurosei-validator
```

### 4. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  validator-core:
    build: ./validator-core
    container_name: neurosei-validator
    restart: unless-stopped
    environment:
      - RUST_LOG=info
      - SEI_CHAIN_ID=sei-testnet-1
    volumes:
      - ~/.neurosei:/opt/neurosei/config
      - ./data:/opt/neurosei/data
    ports:
      - "26656:26656"
      - "26657:26657"

  dashboard:
    build: ./dashboard
    container_name: neurosei-dashboard
    restart: unless-stopped
    ports:
      - "3000:3000"
    depends_on:
      - validator-core

  python-sdk:
    build: ./python-sdk
    container_name: neurosei-sdk
    restart: unless-stopped
    volumes:
      - ./examples:/opt/neurosei/examples
    depends_on:
      - validator-core
```

### 5. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f validator-core
```

## 🔍 Monitoring

### Dashboard Access
- URL: http://localhost:3000
- Default credentials: admin/neurosei2024

### Logs
```bash
# Validator logs
docker-compose logs -f validator-core

# Dashboard logs
docker-compose logs -f dashboard

# System logs
sudo journalctl -u neurosei-validator -f
```

### Metrics
```bash
# CPU/Memory usage
docker stats neurosei-validator

# Network connections
netstat -tulpn | grep 26656
```

## 🧪 Testing

### Run Stress Tests
```bash
cd stress-tests
python3 load_test.py --target-tps 10000 --duration 60
```

### Validate Setup
```bash
# Check validator status
curl http://localhost:26657/status

# Test AI integration
python3 -c "from neurosei import AI; print('AI SDK working!')"

# Verify ZK proofs
cargo test --package neurosei-validator-core
```

## 🔧 Troubleshooting

### Common Issues

1. **Validator not starting**
   ```bash
   # Check config
   cat ~/.neurosei/config.toml
   
   # Check logs
   sudo journalctl -u neurosei-validator -n 50
   ```

2. **Dashboard not accessible**
   ```bash
   # Check if port is open
   netstat -tulpn | grep 3000
   
   # Restart dashboard
   docker-compose restart dashboard
   ```

3. **AI model not loading**
   ```bash
   # Download models
   wget https://models.neurosei.ai/validator-ai.tar.gz
   tar -xzf validator-ai.tar.gz -C /opt/neurosei/models/
   ```

### Performance Tuning

```bash
# Increase file descriptors
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Optimize kernel parameters
echo "net.core.rmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 📊 Health Checks

```bash
#!/bin/bash
# health_check.sh

echo "=== NeuroSei Health Check ==="

# Check validator
if curl -s http://localhost:26657/status > /dev/null; then
    echo "✅ Validator: RUNNING"
else
    echo "❌ Validator: STOPPED"
fi

# Check dashboard
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Dashboard: RUNNING"
else
    echo "❌ Dashboard: STOPPED"
fi

# Check AI SDK
if python3 -c "from neurosei import AI" 2>/dev/null; then
    echo "✅ AI SDK: WORKING"
else
    echo "❌ AI SDK: ERROR"
fi

echo "=== Health Check Complete ==="
```

## 🆘 Support

- **Emergency**: Discord #neurosei-support
- **Documentation**: https://docs.neurosei.ai
- **Issues**: GitHub Issues
- **Email**: support@neurosei.ai

---

**Deploy with confidence! 🚀** 