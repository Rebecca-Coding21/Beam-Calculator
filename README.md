# Beam Calculator
![image](https://github.com/Rebecca-Coding21/Beam-Calculator/assets/94243632/6f0d126d-9ab7-4c42-b512-f5e6b22a0a09)
### Video Demo: https://youtu.be/0ZYb2AWQ1gQ
### Descripton: 
The Beam Calculator is a web application to calculate the internal forces for continuous beams with two to five spans and a continuous line load. This is a useful tool for civil engineers, especailly for structural engineering. It can also help students controlling their hand calculations. 
The user can input the number of spans, the length of the span and a value for the continuous line load. Integer and float values are possible. If one input is missing, an error message is displayed at the top of the page.
After calculation, the user is directed to a new page. The page contains a table that summarizes the input data, a table with the results, including all relevant internal forces as well as the support forces of the beam. At the bottom of the page two diagrams show the torque curve and the shear force progression. 
The four buttons at the bottom enable the user to either start a new calculation, download the result values in csv-format, download the diagrams or print the whole page to pdf. The pdf-file can be useful as a summary of the results.

#### Tech Stack:
The application uses python in combination with flask as programming language. The style of the website is created by using HTML, CSS and Bootstrap 5. For the creation of the diagrams the mathplotlib library was used. The webpage is responsive which means that it adapts to the screensize of the user.
The backend of the application consists of a file called "app.py" which is the application itself. The "requirements.txt" file contains all libraries that are used in the project to make their installation easier and faster. The csv-file "momentfactors.csv" contains several factors from an engineer's table book that are needed for the calculation. The static folder contains "styles.css" which contains general style information for the website. The images in the folder are either created by the program itself (moments.png, shearForces.png) or uploaded images that are needed to display them on the webpage.  The templates-folder contains all HTML-templates that are used to build the webpage. In "layout.html" the style and structure that can be used for all pages are defined. The file "index.html" defines the structure of the start page whereas "calculated.html" contains the HTML-code for the webpage that is loaded after calculation.

#### Design Choices:
The layout of the tables and diagrams on the second page was chosen that the page looks clear. It was moreover important that the result table and the diagrams are visible without scrolling on a normal sized PC-screen. Also on the index page it was important that the image at the bottom can be fully seen without scrolling. The page uses light and compatible colors to deliver clean style.
