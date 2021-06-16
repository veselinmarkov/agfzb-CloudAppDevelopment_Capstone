# Django / rest API / IBM cloudant demo application
It displays a list of car dealers and registered users are allowed to add reviews for every dealership. Guest users may view the dealerships and the attached reviews.

**User management** using the Django user authentication system.
Continuous integration and delivery in GitHub actions

**Backend services** uses 
Cloud functions to manage dealers and reviews
Django models and views to manage car model and car make
Django proxy services and views to integrate dealers, reviews, and cars together
 
**Dynamic pages with Django templates** consists of 
Root page that shows all the dealers
A page that show reviews for a selected dealer
A page that let's the end user add a review for a selected dealer

To **Containerize the application** 
Deployment artifacts are added
The application is deployed as IBM cloud Foundry app 
