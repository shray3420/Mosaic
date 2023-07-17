High-level Overview:
    The application is composed of a central middleware server and multiple Microservice Mosaic Generators (MMGs). Each MMG is specifically designed to generate a mosaic image based on a given theme.
    To set up the generator, there are two commands that need to be executed in the project-1989 terminal. Running these commands will mark the bash files as "executable," allowing the scripts to be executed when required:
        - "chmod +x start.sh"
        - "chmod +x kill.sh"
    After executing these commands, simply run "python3 -m flask run" to launch the main service, which will automatically start all microservices. This occurs because the startup.sh bash file is called when the main Flask app starts, and this script runs all the microservices. The system is now ready to accept images and generate mosaics based on the provided themes.
MMG Connection to Middleware:
    When the middleware server starts, it checks for the availability of each MMG by sending a GET request to the MMG's root endpoint (/) and verifies that it returns a 200 response. The middleware waits for up to 10 seconds for the MMGs to become available. The terminal will display the ongoing process and notify the user if any issues arise.

Middleware Requesting Mosaic from MMGs:
    When a user uploads a base image to the middleware, the middleware sends a POST request to the /generateMosaic endpoint of each MMG to request the generation of a mosaic. The request includes the image, tilesAcross, renderedTileSize, and the theme to be generated. The MMG processes the data and returns a JSON object containing a base64-encoded string of the generated mosaic image. After all mosaics are generated, the middleware sends the data to the front-end to be displayed for the user.

Additional Details:
    - Upon termination (CTRL+C) of the main Flask app, the "kill.sh" script is automatically invoked to close all microservices. This ensures that the ports are available for the next instance and helps maintain the application's efficiency, avoiding potential issues with port availability. 
    - For added convenience, the main Flask app dynamically updates the MMGs array based on the contents of the themes folder, eliminating the need to update the array manually.
    - Since it can be difficult to fully view all images on the front end, all generated mosaics are saved in the "mosaics" folder for isolated viewing. Throughout the process, the terminal displays updates on the application's progress, informing the user about the program's status, the theme of the mosaic being generated, and the total runtime required to produce all mosaics.