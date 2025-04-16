from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configuration
AIRA_HUB_URL = os.environ.get('AIRA_HUB_URL', 'https://aira-fl8f.onrender.com')


# Helper functions
def format_timestamp(timestamp):
    """Convert timestamp to human-readable format"""
    if not timestamp:
        return "N/A"
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def format_duration(seconds):
    """Format seconds into a human-readable duration"""
    if not seconds:
        return "N/A"

    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = []
    if days > 0:
        result.append(f"{int(days)}d")
    if hours > 0:
        result.append(f"{int(hours)}h")
    if minutes > 0:
        result.append(f"{int(minutes)}m")
    if seconds > 0 or not result:
        result.append(f"{int(seconds)}s")

    return " ".join(result)


def get_agents():
    """Get all registered agents from the hub"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/agents")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get agents: {response.text}", "error")
            return []
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return []


def get_agent_details(url):
    """Get details for a specific agent"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/agents/{url}")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get agent details: {response.text}", "error")
            return None
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return None


def get_hub_status():
    """Get AIRA Hub status"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/status")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get hub status: {response.text}", "error")
            return None
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return None


def get_resources():
    """Get all shared resources from the hub"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/resources")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get resources: {response.text}", "error")
            return []
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return []


def get_categories():
    """Get all agent categories from the hub"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/categories")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get categories: {response.text}", "error")
            return []
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return []


def get_tags(type="agent"):
    """Get all tags from the hub"""
    try:
        response = requests.get(f"{AIRA_HUB_URL}/tags?type={type}")
        if response.status_code == 200:
            return response.json()
        else:
            flash(f"Failed to get tags: {response.text}", "error")
            return []
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
        return []


# Routes
@app.route('/')
def index():
    """Home page showing overview of the AIRA Hub"""
    status = get_hub_status()
    agents = get_agents()

    active_agents = [a for a in agents if a.get('status') == 'online']

    context = {
        'status': status,
        'agents_count': len(agents),
        'active_agents_count': len(active_agents),
        'categories': get_categories(),
        'agent_tags': get_tags('agent'),
        'skill_tags': get_tags('skill')
    }

    return render_template('index.html', **context)


@app.route('/agents')
def agents_list():
    """Page showing all registered agents"""
    agents = get_agents()
    categories = get_categories()
    tags = get_tags('agent')

    # Filter parameters
    category = request.args.get('category')
    tag = request.args.get('tag')
    status = request.args.get('status')
    query = request.args.get('q', '').lower()

    # Apply filters
    if category:
        agents = [a for a in agents if a.get('category') == category]
    if tag:
        agents = [a for a in agents if tag in a.get('tags', [])]
    if status:
        agents = [a for a in agents if a.get('status') == status]
    if query:
        agents = [a for a in agents if query in a.get('name', '').lower() or
                  query in a.get('description', '').lower()]

    return render_template(
        'agents.html',
        agents=agents,
        categories=categories,
        tags=tags,
        filter_category=category,
        filter_tag=tag,
        filter_status=status,
        filter_query=query
    )


@app.route('/agents/<path:agent_url>')
def agent_details(agent_url):
    """Page showing details for a specific agent"""
    agent = get_agent_details(agent_url)
    if not agent:
        flash(f"Agent not found: {agent_url}", "error")
        return redirect(url_for('agents_list'))

    return render_template('agent_details.html', agent=agent)


@app.route('/resources')
def resources_list():
    """Page showing all shared resources"""
    resources = get_resources()

    # Filter parameters
    resource_type = request.args.get('type')
    query = request.args.get('q', '').lower()

    # Apply filters
    if resource_type:
        resources = [r for r in resources if r.get('resource', {}).get('type') == resource_type]
    if query:
        resources = [r for r in resources if query in r.get('resource', {}).get('description', '').lower() or
                     query in r.get('resource', {}).get('uri', '').lower()]

    return render_template(
        'resources.html',
        resources=resources,
        filter_type=resource_type,
        filter_query=query
    )


@app.route('/discover', methods=['GET', 'POST'])
def discover():
    """Page to discover agents based on criteria"""
    categories = get_categories()
    agent_tags = get_tags('agent')
    skill_tags = get_tags('skill')

    if request.method == 'POST':
        # Get discovery parameters
        query_params = {}

        skill_id = request.form.get('skill_id')
        if skill_id:
            query_params['skill_id'] = skill_id

        skill_tags_list = request.form.getlist('skill_tags')
        if skill_tags_list:
            query_params['skill_tags'] = skill_tags_list

        resource_type = request.form.get('resource_type')
        if resource_type:
            query_params['resource_type'] = resource_type

        agent_tags_list = request.form.getlist('agent_tags')
        if agent_tags_list:
            query_params['agent_tags'] = agent_tags_list

        category = request.form.get('category')
        if category:
            query_params['category'] = category

        status = request.form.get('status')
        if status:
            query_params['status'] = status

        # Make the discovery request
        try:
            response = requests.post(f"{AIRA_HUB_URL}/discover", json=query_params)
            if response.status_code == 200:
                result = response.json()
                return render_template(
                    'discover.html',
                    categories=categories,
                    agent_tags=agent_tags,
                    skill_tags=skill_tags,
                    results=result,
                    query_params=query_params
                )
            else:
                flash(f"Discovery request failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error connecting to AIRA Hub: {str(e)}", "error")

    return render_template(
        'discover.html',
        categories=categories,
        agent_tags=agent_tags,
        skill_tags=skill_tags,
        results=None,
        query_params={}
    )


@app.route('/register', methods=['GET', 'POST'])
def register_agent():
    """Page to register a new agent"""
    if request.method == 'POST':
        # Get registration data
        agent_data = {
            'url': request.form.get('url'),
            'name': request.form.get('name'),
            'description': request.form.get('description', ''),
            'version': request.form.get('version', '1.0.0'),
            'skills': json.loads(request.form.get('skills', '[]')),
            'shared_resources': json.loads(request.form.get('shared_resources', '[]')),
            'aira_capabilities': request.form.getlist('aira_capabilities'),
            'auth': json.loads(request.form.get('auth', '{}')),
            'tags': request.form.getlist('tags'),
            'category': request.form.get('category')
        }

        # Optional provider info
        provider_org = request.form.get('provider_organization')
        provider_url = request.form.get('provider_url')
        if provider_org or provider_url:
            agent_data['provider'] = {}
            if provider_org:
                agent_data['provider']['organization'] = provider_org
            if provider_url:
                agent_data['provider']['url'] = provider_url

        # Make the registration request
        try:
            response = requests.post(f"{AIRA_HUB_URL}/register", json=agent_data)
            if response.status_code == 201:
                result = response.json()
                flash(f"Agent '{agent_data['name']}' registered successfully!", "success")
                return redirect(url_for('agent_details', agent_url=agent_data['url']))
            else:
                flash(f"Registration failed: {response.text}", "error")
        except Exception as e:
            flash(f"Error connecting to AIRA Hub: {str(e)}", "error")

    categories = get_categories()
    return render_template('register.html', categories=categories)


@app.route('/heartbeat/<path:agent_url>', methods=['POST'])
def send_heartbeat(agent_url):
    """API endpoint to send a heartbeat for an agent"""
    try:
        response = requests.post(f"{AIRA_HUB_URL}/heartbeat/{agent_url}")
        return jsonify({"status": "success" if response.status_code == 200 else "error",
                        "message": response.text})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/unregister/<path:agent_url>', methods=['POST'])
def unregister_agent(agent_url):
    """API endpoint to unregister an agent"""
    try:
        response = requests.delete(f"{AIRA_HUB_URL}/agents/{agent_url}")
        if response.status_code == 200:
            flash(f"Agent unregistered successfully!", "success")
        else:
            flash(f"Failed to unregister agent: {response.text}", "error")
    except Exception as e:
        flash(f"Error connecting to AIRA Hub: {str(e)}", "error")
    return redirect(url_for('agents_list'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)