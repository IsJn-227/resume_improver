from random import choice

SMART_TEMPLATES = {
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
    "github": [
        "Hosted and reviewed code on GitHub with team-based versioning.",
        "Used GitHub Actions for CI/CD pipelines."
    ],
    "gitlab": [
        "Used GitLab for collaborative development and version control.",
        "Configured GitLab CI/CD pipelines for deployment automation."
    ],
    "docker": [
        "Containerized applications using Docker for scalable deployment.",
        "Built Docker images and managed multi-container setups."
    ],
    "backend": [
        "Designed and implemented robust backend architectures.",
        "Worked on scalable backend systems for web platforms."
    ],
    "api": [
        "Built and consumed RESTful APIs in live applications.",
        "Integrated third-party APIs using best practices."
    ],
    "cloud": [
        "Deployed applications on AWS/GCP cloud platforms.",
        "Configured cloud services for scalable deployment."
    ],
    "development": [
        "Led end-to-end development cycles for full-stack projects.",
        "Contributed to development of production-ready applications."
    ],
    "proficiency": [
        "Demonstrated proficiency in key technologies like Python and Flask.",
        "Maintained strong technical proficiency across tools and frameworks."
    ]
    # Add more smart lines as needed
}

def generate_resume_line(keyword):
    keyword = keyword.lower()

    # Handle compound keywords like "flask django"
    words = keyword.split()
    generated_lines = []

    for word in words:
        if word in SMART_TEMPLATES:
            generated_lines.append(choice(SMART_TEMPLATES[word]))
        else:
            generated_lines.append(f"Added relevant experience with {word} in technical projects.")

    return "\n".join(generated_lines)
