from core.application import EtlApplication


def main():
    """
    Punto de entrada principal del ETL
    """

    app = EtlApplication()
    app.run()


if __name__ == "__main__":
    main()
