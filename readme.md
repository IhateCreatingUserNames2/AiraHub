# AIRA Hub WebUI

DEFAULT AIRA HUB URL in the code = https://aira-fl8f.onrender.com/

A modern, responsive web interface for the AIRA Hub, providing easy management and visualization of AI agents connected to the AIRA network through the Agent-to-Agent (A2A) and Model Context Protocol (MCP).

## Overview

AIRA Hub WebUI provides a user-friendly interface for:

- Viewing registered agents and their capabilities
- Discovering agents based on specific criteria
- Registering new agents with the AIRA Hub
- Managing resources shared across the network
- Monitoring hub status and agent health

This web interface simplifies the process of working with A2A and MCP protocols, enabling seamless interoperability between AI agents from different frameworks and vendors.

## Features

- **Agent Registry**: Browse, search, and filter all registered agents
- **Agent Details**: View comprehensive information about each agent, including skills and resources
- **Resource Directory**: Browse all shared resources across the network
- **Discovery Engine**: Find agents based on specific capabilities, tags, or resource types
- **Registration Form**: Register new agents with a simple form interface
- **Status Dashboard**: Monitor the health and status of the AIRA Hub
- **Heartbeat Management**: Send heartbeats to agents to check their status


![image](https://github.com/user-attachments/assets/eda2654d-d77f-41c3-a5ef-232a118a7e34)

## Installation

### Prerequisites

- Python 3.8+
- Flask 2.0+
- Access to an AIRA Hub instance

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/aira-hub-webui.git
   cd aira-hub-webui
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set environment variables:
   ```bash
   export AIRA_HUB_URL=https://your-aira-hub-url  # URL of your AIRA Hub
   export SECRET_KEY=your-secret-key              # For Flask session security
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Access the WebUI at http://localhost:5000

## Configuration

You can configure the application using environment variables or by modifying the `config.py` file:

- `AIRA_HUB_URL`: URL of the AIRA Hub instance
- `SECRET_KEY`: Secret key for Flask sessions
- `PORT`: Port to run the web server on (default: 5000)
- `DEBUG`: Enable debug mode (default: False in production)

## Docker Deployment

A Docker image is available for easy deployment:

```bash
docker pull yourusername/aira-hub-webui:latest

docker run -p 5000:5000 \
  -e AIRA_HUB_URL=https://your-aira-hub-url \
  -e SECRET_KEY=your-secret-key \
  yourusername/aira-hub-webui:latest
```

## Usage

### Viewing Agents

Browse all registered agents through the Agents page. Use filters to narrow down by category, tags, or status.

### Agent Details

Click on any agent to view its details, including:
- Basic information (name, URL, status)
- Description and tags
- Authentication requirements
- Skills provided
- Resources shared

You can also send heartbeats to check if an agent is responsive.

### Discovering Agents

Use the Discovery page to find agents based on specific criteria:
- Skills (by ID or tags)
- Resource types
- Agent tags or category
- Status (online/offline)

### Registering a New Agent

Use the Registration form to add a new agent to the AIRA Hub:
1. Fill in the basic information (URL, name, description)
2. Set provider details if applicable
3. Specify AIRA capabilities (A2A, MCP, etc.)
4. Configure authentication if required
5. Add skills and resources (advanced)

## Architecture

The AIRA Hub WebUI follows a simple Flask-based architecture:
- Flask web application
- Bootstrap 5 for responsive UI
- Direct API communication with the AIRA Hub

## Development

### Project Structure

```
aira_hub_webui/
├── app.py                     # Main Flask application
├── templates/                 # HTML templates
├── static/                    # Static assets
├── utils/                     # Utility functions
├── config.py                  # Configuration settings
└── requirements.txt           # Python dependencies
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Related Projects

- [AIRA Hub](https://github.com/google/A2A) - The main AIRA Hub repository
- [A2A Protocol](https://github.com/google/A2A) - Agent-to-Agent Protocol
- [Model Context Protocol](https://modelcontextprotocol.io) - Model Context Protocol

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google's A2A Protocol team
- Model Context Protocol contributors
- All the agents sharing their capabilities on the AIRA network
