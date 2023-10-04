tasker
#### Video Demo:  <https://www.youtube.com/watch?v=g129vAlOb40>
#### Description:
Tasker is a Flask Web Application that helps manage tasks within groups of people with the targeted audience being employers or groups of students. Using Tasker, you can have a dashboard on what are the tasks that you need to complete and tasks that you have given out. You can remove or edit these tasks anytime to show everyone in the group the progress of the task, the due date, the importance, and the description. Apart from the home page, there is a Manage page which allows you to see an overview of all the tasks given out to the group. On the Manage page, there is a search function that allows you to look at a specific person's tasks. Some things I learned through this project are getting better at CSS, learning Bootstrap and how to layout pages with designs. However, this project was done without any JavaScript.
Tasker includes multiple functions such as Manage, Search, Edit, Remove, and Change Password. All these routes are managed through app.py. The Manage function allows users to see an overview of everyone's tasks, this is to help plan for the day and see who is busy so that they can properly assign tasks to people who are freer. The Search function allows users to look at specific users' tasks. The Edit function allows users to edit the information of their tasks, being able to update the status of the tasks. The Remove function removes the task from the database. The Change Password function allows users to change their password in the event they forget their password.
For the design, I took the login page idea from Diprella. I added some color codes to the status as it will stand out more. For the HTML pages, I implemented many for loops and if statements using jinja to create more dynamic tables with different information depending on the pages visited by the user.
Without JavaScript, there were many things that could not be done. Such things include a sorting function I wanted to create, passing of information smoothly from HTML page to HTML page, and creating much smoother and more dynamic webpages for user experience. I had to find other ways to overcome this barrier such as implementing more forms and more Python code to receive the information. Thus the code is messier than I hoped it to be and will learn JavaScript before working on the next project.
Some stuff that I have learned from this project is I have become much more proficient in CSS classes and style. However, I could learn more about the padding and margins to create more aligned spaces. I have also touched up on my flask knowledge, with sessions and routes.
One improvement to my project is that I could add a hierarchy system to the group, such as the boss, manager, and employee. This will allow only the boss to edit everyone else's tasks while the people with less power can only edit those at the same level as them. I could also implement group codes so that there could be multiple groups in the system and allow only those in the same group to look at the tasks of others in the same groups. These people can then be part of many different groups so that they can be involved in different projects.
