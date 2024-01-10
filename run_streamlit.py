if __name__ == "__main__":
    import dotenv
    from src.main import main
    from src import logger

    dotenv.load_dotenv()
    logger.setup_logging()

    # import logging
    # logging.getLogger("fsevents").setLevel(logging.WARNING)
    # logging.getLogger("matplotlib").setLevel(logging.WARNING)
    main()
