from random import choice

def generate_resume_line(keyword):
    """
    Returns a smart resume bullet point or line using the given keyword.
    You can expand this further using AI models for better quality.
    """
    templates = {
        "flask": [
            "Developed backend services using Flask for RESTful APIs.",
            "Built scalable Flask apps with database integration."
        ],
        "django": [
            "Created web apps with Django and PostgreSQL.",
            "Implemented Django models and views to manage business logic."
        ],
        "sql": [
            "Wrote complex SQL queries to retrieve and analyze data.",
            "Optimized SQL database performance for large datasets."
        ],
        "git": [
            "Used Git for version control and collaborative development.",
            "Managed feature branches and pull requests using Git workflows."
        ],
        "rest": [
            "Integrated third-party APIs using REST architecture.",
            "Designed REST endpoints for CRUD operations."
        ],
        # Add more as needed...
    }

    if keyword in templates:
        return choice(templates[keyword])
    else:
        return f"Added relevant experience with {keyword} in technical projects."
