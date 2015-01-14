# Run a test server.
from adminweb import app
#app.app.run(host='0.0.0.0', port=5000, debug=True)
app.app.run(host='127.0.0.1', port=5000, debug=True)
