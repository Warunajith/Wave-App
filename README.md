# Wave-App

This Wave app Predicts the Real State prices based on several Factors.

1. Run the Wave Server
   
     Download and run the suitable Wave Server on your local machine using this link.

     https://wave.h2o.ai/docs/installation#downloading-wave
3. Clone this project and setup a virtual environment.
   
     git clone https://github.com/Warunajith/Wave-App.git
   
     python -m venv venv
   
     .\venv\Scripts\activate

 4. Install the Wave Python driver and Wave ML

      pip install h2o-wave

      pip install h2o-wave[ml]

 5. Run the App
    
      wave run wave-app.py

The app will be running on http://localhost:10101/predict


