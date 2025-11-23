from app import app
import time

def test_hello():
    # Simulate a long running test suite (20 seconds)
    print("Running heavy tests...") 
    time.sleep(20) 
    
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"Hello World" in response.data
