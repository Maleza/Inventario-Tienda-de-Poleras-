from db.conexion import crear_tablas
from ui.app import iniciar_app

def main():
    crear_tablas()
    iniciar_app()

if __name__ == "__main__":
    main()