import os
from app import app


#Insert the line below to to run on Cloud9    
app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))
#end insert, place above __name__ == __main__
if __name__ == '__main__':
    app.run()
    app.debug(True)