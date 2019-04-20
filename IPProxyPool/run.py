from Api.api import app
from schedule import Schedule


def main():
    s = Schedule()
    s.run()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
