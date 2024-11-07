import os
import sys
from pathlib import Path

def check_wsgi_configuration():
    """
    Diagnoses common WSGI configuration issues in a Django project
    Returns a dictionary of findings and suggestions
    """
    issues = []
    recommendations = []
    
    # Check current directory structure
    current_dir = Path.cwd()
    project_files = list(current_dir.glob('*'))
    
    # Check for manage.py
    if not any(f.name == 'manage.py' for f in project_files):
        issues.append("manage.py not found in current directory")
        recommendations.append("Ensure you're in the correct project directory")
    
    # Check PYTHONPATH
    python_path = os.environ.get('PYTHONPATH', '')
    if not python_path:
        issues.append("PYTHONPATH environment variable not set")
        recommendations.append("Set PYTHONPATH to include your project root")
    
    # Check sys.path
    project_in_path = False
    for path in sys.path:
        if str(current_dir) in path:
            project_in_path = True
            break
    
    if not project_in_path:
        issues.append("Project directory not in Python path")
        recommendations.append("Add project directory to PYTHONPATH")
    
    # Check wsgi.py existence and structure
    wsgi_locations = [
        current_dir / 'wsgi.py',
        current_dir / 'api_project' / 'wsgi.py',
        *current_dir.glob('*/wsgi.py')
    ]
    
    wsgi_found = False
    for wsgi_path in wsgi_locations:
        if wsgi_path.exists():
            wsgi_found = True
            # Check wsgi.py content
            with open(wsgi_path) as f:
                content = f.read()
                if 'application = get_wsgi_application()' not in content:
                    issues.append(f"wsgi.py at {wsgi_path} might be misconfigured")
                    recommendations.append("Ensure wsgi.py has proper application configuration")
    
    if not wsgi_found:
        issues.append("wsgi.py not found in expected locations")
        recommendations.append("Create wsgi.py in your Django project directory")
    
    # Check Django project structure
    if not any(f.is_dir() and f.name == 'api_project' for f in project_files):
        issues.append("api_project directory not found")
        recommendations.append("Ensure project directory name matches WSGI module path")
    
    return {
        'current_directory': str(current_dir),
        'python_path': python_path,
        'sys_path': sys.path,
        'issues': issues,
        'recommendations': recommendations
    }

if __name__ == '__main__':
    results = check_wsgi_configuration()
    
    print("\n=== WSGI Configuration Diagnostic Results ===\n")
    print(f"Current Directory: {results['current_directory']}")
    print("\nPYTHONPATH:")
    print(results['python_path'] or '(not set)')
    
    print("\nIssues Found:")
    if results['issues']:
        for issue in results['issues']:
            print(f"- {issue}")
    else:
        print("No issues found")
    
    print("\nRecommendations:")
    if results['recommendations']:
        for rec in results['recommendations']:
            print(f"- {rec}")
    else:
        print("No recommendations needed")