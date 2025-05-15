import os
import base64
import requests
import json
import glob

# GitHub credentials from environment variables
github_username = os.environ.get('GITHUB_USERNAME')
github_token = os.environ.get('GITHUB_TOKEN')

# Repository information
repo_name = "fb-share-tool"
repo_description = "Facebook post share automation tool with cookie-based authentication and custom configuration"

# Create repository
def create_repo():
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": repo_description,
        "private": False
    }
    
    # Check if repo already exists first
    check_url = f"https://api.github.com/repos/{github_username}/{repo_name}"
    check_response = requests.get(check_url, headers=headers)
    
    if check_response.status_code == 200:
        print(f"Repository already exists: {github_username}/{repo_name}")
        return True
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in (201, 200):
        print(f"Repository created successfully: {github_username}/{repo_name}")
        return True
    else:
        print(f"Failed to create repository. Status code: {response.status_code}")
        print(f"Error message: {response.text}")
        return False

# Upload a file to the repository
def upload_file(file_path, repo_path):
    try:
        # Read file content and encode to base64
        with open(file_path, 'rb') as file:
            content = base64.b64encode(file.read()).decode('utf-8')
        
        url = f"https://api.github.com/repos/{github_username}/{repo_name}/contents/{repo_path}"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Check if file exists already to get the SHA
        check_response = requests.get(url, headers=headers)
        if check_response.status_code == 200:
            # File exists, need to include SHA
            sha = check_response.json()['sha']
            data = {
                "message": f"Update {os.path.basename(file_path)}",
                "content": content,
                "sha": sha
            }
        else:
            # New file
            data = {
                "message": f"Add {os.path.basename(file_path)}",
                "content": content
            }
        
        response = requests.put(url, headers=headers, json=data)
        
        if response.status_code in (201, 200):
            print(f"Uploaded {file_path} to {repo_path}")
            return True
        else:
            print(f"Failed to upload {file_path}. Status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return False
    except Exception as e:
        print(f"Error uploading {file_path}: {e}")
        return False

# Create README.md
def create_readme():
    readme_content = """# FB Share Tool

An automated Facebook post sharing tool with sleek interface.

## Features

- Cookie-based authentication
- Cookie generator functionality
- Persistent process even if browser is closed
- Real-time sharing statistics
- Dark theme interface with modern design

## Setup

1. Install requirements:
   ```
   pip install streamlit aiohttp httpx rich bs4
   ```

2. Run the application:
   ```
   streamlit run app.py
   ```

## Usage

1. Enter your Facebook cookie or use the cookie generator
2. Provide Facebook post URL to share
3. Set number of shares and delay between operations
4. Click Start Engine to begin sharing

## Note

Use responsibly and only with accounts you own.
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    return 'README.md'

# Find all files recursively
def find_all_files():
    files_list = []
    
    # Add specific files we know exist
    specific_files = [
        'app.py',
        '.streamlit/config.toml',
        'pyproject.toml',
        'uv.lock',
        'generated-icon.png'
    ]
    
    for file_path in specific_files:
        if os.path.exists(file_path):
            files_list.append((file_path, file_path))
    
    # Add files from attached_assets
    if os.path.exists('attached_assets'):
        for root, dirs, files in os.walk('attached_assets'):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path):
                    files_list.append((file_path, file_path))
    
    return files_list

# Main function
def main():
    print("Starting GitHub repository creation and file upload...")
    
    # Create the repository
    if not create_repo():
        print("Aborting due to repository creation failure")
        return
    
    # Create README.md
    readme_path = create_readme()
    
    # Get all files to upload
    files_to_upload = [(readme_path, 'README.md')]  # Start with README
    files_to_upload.extend(find_all_files())
    
    print(f"Found {len(files_to_upload)} files to upload")
    
    # Upload each file
    for local_path, repo_path in files_to_upload:
        upload_file(local_path, repo_path)
    
    print(f"Repository setup complete. Visit: https://github.com/{github_username}/{repo_name}")

if __name__ == "__main__":
    main()