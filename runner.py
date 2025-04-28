from core.manager import ProjectManager

if __name__ == "__main__":
    manager = ProjectManager()
    manager.load_manager_json('manager.json')
    manager.run()
