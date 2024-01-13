from uagents import Bureau
from agents.manager import manager

bureau = Bureau()

bureau.add(manager)

if __name__ == "__main__":
    bureau.run()
