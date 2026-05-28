# task_ai.py

def generate_subtasks(task_title):
    title = task_title.lower()

    if "build" in title or "create" in title:
        return [
            "Define requirements and scope",
            "Design system architecture",
            "Setup project structure",
            "Implement core functionality",
            "Test feature",
            "Deploy application"
        ]

    elif "api" in title or "backend" in title:
        return [
            "Design API endpoints",
            "Create Django views",
            "Setup URLs",
            "Connect database",
            "Add validation",
            "Test APIs"
        ]

    elif "frontend" in title:
        return [
            "Design UI layout",
            "Create templates",
            "Connect backend APIs",
            "Add interactivity",
            "Make responsive design"
        ]

    else:
        return [
            "Break task into smaller steps",
            "Research requirements",
            "Implement step by step",
            "Test and refine"
        ]