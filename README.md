# StatusQ.cpu

> Efficient monitoring and management of CPU status.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Rick-torrellas/core-log-engine/badges/version.json)
[![Main CI Pipeline](https://github.com/Rick-torrellas/StatusQ.cpu/actions/workflows/main.yaml/badge.svg)](https://github.com/Rick-torrellas/StatusQ.cpu/actions/workflows/main.yaml)

## 📖 Description

**StatusQ**.cpu is a tool designed to provide accurate, real-time metrics on CPU performance and status. Its purpose is to facilitate observability in systems, allowing developers and administrators to make informed decisions based on the current workload.

## ✨ Main Features

- **Real-Time Monitoring**: Instant visualization of core and process usage.
- **Lightweight and Fast**: Designed to have a minimal memory footprint.
- **Configurable Alerts**: Set thresholds to receive notifications when the CPU exceeds certain limits.
- **Data Export**: Ability to export logs for later analysis.

## 📋 Table of Contents

- [🚀 Installation](#installation)
- [💻 Usage](#usage)
- [⚙️ Configuración](#config)

## 🚀 Installation

### Prerequisites

Ensure you have the following installed before starting:

- python
- pip

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/Rick-torrellas/statusq.cpu.git
   ```
2. Navigate to the project directory:
   ```bash
   cd statusq-cpu
   ```
3. Install the dependencies:
   ```bash
   just setup
   ```

## 💻 Usage

To start the application in monitoring mode:

```bash
just run
```

## ⚙️ Configuración


## 🤝 Contributing

Contributions are welcome! Please check our contribution guide for more details.

1. Fork the project.
2. Create your feature branch (git checkout -b feature/NewFeature).
3. Commit your changes (git commit -m 'Add NewFeature').
4. Push to the branch (git push origin feature/NewFeature).
5. Open a Pull Request.

## 📄 License

Distributed under the MIT License. See the LICENSE file for more information.
