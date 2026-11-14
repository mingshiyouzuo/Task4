from .cli import main

if "__main__" == __name__:
    try:
        main()
    except KeyboardInterrupt:
        print("\n已退出")
