
from src.main.core.manager      import WorkspaceManager

def main():
    manager = WorkspaceManager()
    manager.load_workspace("config/workspace.json")
    manager.run()

if __name__ == "__main__":
    main()