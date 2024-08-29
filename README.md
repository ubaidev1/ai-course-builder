# Course Builder

#### There can be a normal user or an admin to access the site, Now I will go through both of the phase, first for a normal user

## For a Normal user

A normal user when visits the site first time, he/she will have to signup, then login to access the site.
On home page user can view all the courses, the course title and description will be appeared on the course card
including the progress bar.

### Course Details

On click on view course, user will be redirected to the course details page, where we can see all the modules in that
course and on click on view details, user will be redirected to the module details page.

### Module Details

On this page user will be able to see the list of the lessons with in that module, with a button 'Details'

### Lesson Details

Here user can see the content of a specific lesson and at the end there will be a option to take a quiz.
User should take the quiz after reading the lesson details, to increase the course progress.
A user can also retake the quiz if he do wants to improve the score. The score will be displayed with the quiz once user
completed the quiz.

#### User assistance

For user assistance a sidebar is added which allows user to view the index of a course and also helps in fast access to
any lesson, module and other pages.
Moreover, a breadcrumb is also added for user navigational aid.

## For Admin

A script is already written to create a admin
An admin can have all the access which a normal user has, but in addition a admin can have access to following things,
which a normal user cannot access.

### Dashboard

Dashboard can be accessed by an admin from the 'DashBoard' button on navbar
Admin can access the dashboard where he will have two options:

#### 1- Can Upload a pdf file and generate content for a course.

#### 2- Option to extending the existing course ( including more modules, lessons, quizzes)

For this user should select a course from the dropdown menu and upload a pdf file.
After processing and when the course content will be generated and a course will be created, the course with the full
content will be displayed in a readable format.

### Result

This option is also available on navbar, only for admin.
This page consists of a table with columns : Course, Username, Email, Obtained Score, Total Score and Percentage.

Following option are also provided on the result page:

#### 1- Search: Admin can search with the username or email.

#### 2- Filter: Course Filter will show a dropdown on click and will filter out the table with the selected course.
