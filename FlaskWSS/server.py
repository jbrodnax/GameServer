#!/bin/env python
from server import create_app, sock

app = create_app(debug=True)

if __name__ == '__main__':
    app.run()