# ePortfolio - Jason Holmes

My name is Jason Holmes. I currently live in Tokyo and have recently completed the Computer Science bachelor's program at Southern New Hampshire University (SNHU). I prepared this ePortfolio as part of my Computer Science capstone course with the intent to highlight my capabilities and my strengths. Through this I intend to seek a career in game development focusing on design and software engineering.

## Table of Contents
* [Professional Self-Assessment](https://holmessnhu.github.io/#professional-self-assessment)
* [Artifact Selection](https://holmessnhu.github.io/#artifact-selection)
* [Code Review](https://holmessnhu.github.io/#code-review)
* [Project Structure and Planning](https://holmessnhu.github.io/#project-structure-and-planning)
* [Artifact Enhancement 1: Software Engineering & Design](https://holmessnhu.github.io/#enhancement-category-1-software-engineering--design)
* [Artifact Enhancement 2: Data Structures & Algorithms](https://holmessnhu.github.io/#enhancement-category-2-data-structures--algorithms)
* [Artifact Enhancement 3: Databases](https://holmessnhu.github.io/#enhancement-category-3-databases)
* [Course Outcomes](https://holmessnhu.github.io/#course-outcomes)
* [The Enhanced Artifact](https://holmessnhu.github.io#the-enhanced-artifact)
* [Creating the New Data](https://holmessnhu.github.io/#creating-the-new-data)
    * [Defining the Database](https://holmessnhu.github.io/#defining-the-database)
    * [Generating the Database](https://holmessnhu.github.io/#generating-the-database)

## Professional Self-Assessment
My computer science journey began in high school taking Java-based Advanced Placement-certified courses in computer science and programming alongside basic HTML development. After high school, I supplemented this education with many years of self-teaching and learning while navigating through life, during which time I taught myself C++ and the higher level concepts behind object-oriented programming, then later C#, Python, and higher level web development concepts including the basics behind the technology stack of modern website design.

This culminated most recently in enrolling at SNHU to formalize what I have learned, reinforce any areas that I had overlooked, and expand my knowledge wherever I could. During my time in the program, I expanded my understanding of data structures and algorithms, gained a more in-depth understanding of full stack development, and earned experience in leading a small team through the game development process from planning and development to private release.

**Collaborating in a team environment (collaboration)** is difficult experience to acquire outside of a professional environment, because self-directed projects tend to have fewer stakes. A game jam team might get together for the jam and then split apart, assuming that jam is even completed. For a larger project that becomes even more of a problem as the ugly and difficult parts of software development rear their heads; without the obligation imposed by a drawn salary or a pending grade, there's nothing stopping a team member from disappearing at the first obstacle. For these reasons, the GAM-305 Digital Game Development course is one of my favorite experiences throughout my time at SNHU; spending time with a stable team that have obligations to themselves and each other to work on and finish the project gave me ample opportunity to experience collaborating in a team environment. I also took on the producer and project lead role for the team, experiencing the tribulations of creating a design, identifying and scheduling the work that needs to be done, and guiding a team through several weeks of development. It is undoubtedly the most valuable experience I gained during my time in the program.

**Communicating with diverse audiences (communication)** is a core skill in software development. Without the ability to communicate clearly with a variety of technical backgrounds, it can quickly become impossible to do simple things like identify client needs, understand and communicate the difficulties associated with a given feature or request, or even prepare documentation on the software you create either to allow others to use it or even just to allow yourself to come back to a section of code later and understand the thought process you had when writing it. This is a skill I have been honing for many years, and every course allowed me to practice it in greater measure by interpreting rubrics, discussing course material with peers, and communicating with professors through email as well as tailored assignments. Well-commented code is a skill that was drilled into me from the first moments of my programming education, which will be clearly evident in the code presented later in the portfolio.

**Data structures and algorithms** represented the biggest challenge when coming into the program at SNHU, and I was excited to dig into it during the program. While my early education taught me the principles behind algorithm design, Big-O notation, and the importance of efficiency, learning which algorithms had which strengths and when was appropriate to implement which was something that had eluded me during my self-teaching process. Getting to experience and understand those things during my Data Structures & Algorithms course was a highlight of my time in the program.

My goal of working in the game development industry is centered around using **software engineering** as an invaluable asset in making myself an attractive asset to potential employers. In many ways, I see this as the second part of a whole when paired with communicating with diverse audiences, as it is impossible to design effective software without first understanding what goal you're aiming to reach, what problems you're aiming to solve, and what needs must be addressed. Understanding design patterns, the importance of good coding standards, and a full-throated belief in testing and maintenance-supportive design are all critical elements as well. Each one of these elements has been served through the experience I've gained programming in each course; from understanding the purpose behind the animal shelter outcomes dashboard developed in Client/Server Development to designing the game for Digital Game Development and breaking it down into task-sized objectives for the entire team to getting a full grasp of modern website design in Full Stack Development, much of my work in and before the program has been focused on improving my capabilities in software engineering.

Finally, **security** is increasingly important in modern software engineering. As we handle consumer data in greater and greater volumes, maintaining their privacy--along with protecting our own technology's integrity--should be considered of paramount importance. My self-teaching experience only allowed me to understand the importance of encryption and how that functions, but implementing that in a meaningful, robust way during the courses in Software Security, Client/Server Development, Full Stack Development, and especially the artifact enhancements I'll discuss later has been invaluable in expanding my understanding of the topic.

These five outcomes represent the pillars of the computer science program at SNHU, and this ePortfolio will highlight my alignment in these areas and my capabilities across each outcome as well as three major categories of software development: software engineering & design, data structures & algorithms, and databases. To this end, for this ePortfolio I have selected an artifact from one of the courses that I've taken and will enhance it along several vectors to demonstrate these capabilities.

## Artifact Selection

While I had the opportunity to choose a separate artifact for each of the three major categories of software engineering & design, data structures & algorithms, and databases, I chose instead to use a single artifact: a database visualization dashboard originally created for a project during my Client/Server Development course. This dashboard utilized a MongoDB database of animal shelter outcomes, a CRUD interface layer written in Python using PyMongo, and a dashboard built with the Dash by Plotly framework to visualize and display the animal shelter outcomes for use by a third-party to identify animal candidates for search-and-rescue training.

This artifact was chosen for two primary reasons. The first reason is that it is essentially a full stack application that covers all three refinement categories, which would allow me to focus all of my attention on this project to really showcase my capabilities for the ePortfolio. The entirety of the CRUD layer and a good portion of the dashboard were written entirely by me, so it’s not so much about making a few minor changes to someone else’s code as it is expanding and enhancing something I’d written before, which lines up with the artifact expectations. The second major reason I chose this is because it is very similar to some tools I used in my previous job working in finance administration for a wealth management firm and I could easily envision how it could be adapted to serve that purpose in a bespoke, performant way. The end result of this project would make a fantastic foundation for an actual, usable application for my previous job.

## Code Review

{% include youtube.html id="blLPAqMX2sw" %}

The dashboard code for the original artifact is available here:
* Link to AnimalShelterDashboard
* Link to AnimalShelterCRUD

This dashboard visualizes animal shelter patient outcome data in the Austin, TX region for a fictional client looking for an easy way to identify search-and-rescue animal training candidates.  outcomes provided by the original course, presenting a dashboard that allows the data to be filtered and sorted along with two visualizations of the data to help users understand it at a glance. However, much of the data presented is useless to the users who are looking for search-and-rescue training candidates. This is addressed using bespoke filters that have a specific set of requirements for each type of training that the user can call up at the click of the filter button, automatically displaying all of the relevant candidates.

The dashboard pulls the data stored in a MongoDB database through the use of a bespoke Python-based CRUD (Create, Read, Update, Delete) layer that enables interaction with the database using PyMongo, a framework that provides the necessary functions. This layer accepts requests from the dashboard and translates them into PyMongo requests, which apply them to the MongoDB database to fetch and change data. The dashboard then generates the HTML for the page and displays it using a callback system for updating those elements with the new data. MongoDB implements a role-based access control system to ensure that only valid users can access the data, which this dashboard bypasses using hard-coded administrator credentials.

## Project Structure and Planning

Updating this dashboard for use in financial administration will mean a great deal of adaptation. The data would of course need to be thrown out and replaced with financial data, then the dashboard itself would need to be updated to accurately reflect this data. The filters too would need to be updated to reflect what would be considered relevant to that data. In my previous experience in finance administration, this would include things like whether a given account is a non-retirement account or a retirement account, which dictates how those accounts are managed and what kinds of assets they can (and should) hold and whether or not certain annual regulatory requirements have been met.

Finally, the security present in the dashboard as-is would be considered woefully inadequate for a final product; anyone accessing this page would have immediately, unfiltered access to all of the data in the database. This is one thing when considering a private application with unimportant data, but when considering a web-based application with sensitive financial data, security immediately becomes the most important element to consider, so adding a login system with authentication, user accounts and role-based access control, session management, and other security features to bring this up to a minimum level of sophistication adequate for handling financial data will be necessary.

However, before the enhancements could proceed at a reasonable pace, I would need to generate suitable data to populate the database. This would, in turn, require the consideration of that database, how the data would get used, and a variety of other concerns. Most of this falls outside of the scope of the artifact enhancement project so I'll detail that in another section [at the end of the page here.](https://holmessnhu.github.io/#creating-the-new-data)

## Enhancement Category 1: Software Engineering & Design
The original artifact is essentially a full stack application providing both back-end and front-end technology layers to create a complete product. While this does make it an ideal candidate for selection to cover every category of potential enhancement, it also means that every enhancement is intrinsically linked to every other enhancement. For example, to enhance this artifact at all, the first step must be to have adequate data for use in testing which means I need to consider the final design of the application and how that data will be organized and used to decide how it should be organized. The details on how this was done are described at the end of the page as linked in the previous section, but this demonstrates how all three of the categories are touched on before the enhancements have even begun.

### Software Engineering
This holistic consideration is intrinsic to the nature of software engineering & design. Designing a solution to a problem is made much simpler once you understand the entirety of that problem, after which it becomes a matter of applying the necessary understanding of software engineering to take it from plan to product. For this purpose, I determined the target feature set for the dashboard and identified what all would be necessary to achieve that and drafted a basic flowchart:

![image](https://github.com/HolmesSNHU/holmessnhu.github.io/assets/120333685/c330dff4-b596-4478-beaf-d1dbbff381f1)

One issue I wanted to address with my enhancements was to correct an oversight I felt the original dashboard had: hard-coded login credentials. This is exceptionally bad practice and in a production environment it would be incredibly insecure and a nightmare for maintainability. Any change in the server organization, connection details, even a port changing would require that the entire application be brought down, updated, tested, and then deployed. A web application wants to minimize its downtime, not extend it unnecessarily, so I also want to set up a configuration system that will move the sensitive credential information to a separate configuration file that can be more readily secured and, in doing so, enable future development to more easily expand the maintenance functionality to make configuration updates smoother and require less downtime. 

### Security
The first and foremost of the concerns identified by the design flowchart was the security issue represented by the hard-coded credentials. Moving them to a configuration file would only be one step; I would also need to completely replace their presence with a robust security layer to ensure that the data could not be accessed without valid login credentials. This would require implementing logins and the underlying systems to support that, which would require a fundamental rewrite of how the dashboard displays everything in the first place. Then underneath that, login management, authentication and verification, and session management would be necessary. On the plus side, designing these systems properly should allow multiple users to interact with the data simultaneously. In a production environment user registration would be handled separately from login verification, but for demonstration purposes I built it into the login system to allow for immediate registration. 

### Communication
Throughout the writing of all of these systems, adequate documentation and code commenting, including file headers with the details for the purpose and author of each file and inline comments describing the how and why of everything happening serves a critical purpose in the communication with development peers past, present, and future. Furthermore, building these systems with an eye towards the user requirements pulled from my experience on the user-side of applications like this one also support the communication outcome.

## Enhancement Category 2: Data Structures & Algorithms
Implementing a login system by itself is its own challenge, but ensuring it is adequately secure is another entirely. For the enhancements I wanted to make, it wouldn't be enough to have a table of usernames and passwords. That would just be trading one poor security practice for another, and that wouldn't be enough for what I wanted to achieve. 

### Software Engineering
To implement a robust credential verification system, I would certainly need a login database to contain the credentials to be verified against. I would also need to build a session management system to ensure that the user at the controls remains the user that was verified. This would involve building such a login database from scratch, hashing passwords with cryptographic algorithms, verifying them securely against one another, and generating and managing active user sessions that continually verify themselves with a security token and session IDs generated at random. 

To do any of that, however, I would need to start with the login database. Identifying how that would look would allow me to build the rest of the security layer. To this end, I worked out a login validation schema for the MongoDB login database. allowing MongoDB to handle data validation and other concerns:

* Link to validation schema

While simple, the production of this schema helped me identify several of the factors that I would need to consider when building the security layer such as the hashing of passwords, role-based access, and session management--including failed login attempts, account locking, session tracking, and security tokens.

### Data Structures and Algorithms
There were three elements that I would need but which I would have to handle individually: session IDs, security token generation, and password hashing. A session ID needs to uniquely identify a user after they've logged in and allow the server to track their status, so not much is needed here; adequate randomness and uniqueness is all that is needed, so making use of Python's universal unique identifier (UUID) algorithm to generate an ID for each session and building the necessary management systems for tracking active sessions was all that was required. Security tokens validate that the user has successfully passed credential validation and grant access to the resources available to their set of permissions, so the complexity with these has more to do with the management systems than generating the token. The token itself is generated using the Python secrets library to ensure it is an adequately random token. These two systems serve similar functionality but provide important distinctions allowing them to support one another; however, a different design may have chosen to merge the two into a single system.

Hashing passwords is a somewhat more thorny topic. Passwords cannot simply be stored in a database to be compared against as doing so is bad practice and extremely insecure--though, you do still see companies being caught doing exactly this from time to time. To avoid this, you need to alter the password the user provides in a way that you can still validate the password the user inputs when logging in, but so that neither you nor anyone else who gets access to your database can tell what that password actually is. By running it through a cryptographic algorithm, you can produce a unique result that no other input will produce but which cannot be reversed to get the original value. If anyone gets access to the database, all they will find for passwords is a long series of nonsense characters that can't be used for anything.

The difficult here is striking the right balance between security and optimization. Since you are hashing the password every time someone attempts to log in, the computational complexity of the chosen algorithm has serious concerns for the scalability of your application. The more secure the algorithm you choose for hashing passwords, the more secure the passwords become--but the more computationally expensive that authentication becomes. Given that I'm designing a system for use with financial data, the security element is critical; the algorithm I choose must provide adequate password security without being so demanding that the system cannot support scale. To this end, I chose SHA-256 as an adequate middle ground. SHA-256 is a cryptographic function that generates a 256-bit hash value based on the input data; in this case, the password a user chooses. It is sufficiently complex to generate essentially unique results no matter the input and ensure that it would be infeasible to reverse calculate the input. It also features several optimization techniques to help minimize the resource and complexity costs of hashing passwords, helping to keep it adequately performant to allow for scaling. While this application is unlikely to ever see the kind of scale where this would make a big impact, considering these things earlier instead of later helps to minimize the amount of work done to reconfigure or refactor in the future.

Additionally, many of the little details of my enhancement work have been focused on balancing the efficiency of pulling data from the database when needed and caching it in the application when possible, as evidenced by my usage of the VerifyUser function pulling the login record for each user when it verifies them and using that data elsewhere for efficiency.

### Security
In addition to the above concerns which are all heavily focused on security as well, the password hashing, session management, and login verification systems I added are all focused on mitigating security vulnerabilities before they happen. Furthermore, they’re designed with potential expansion in mind; for example, the password hashing functionality can easily be expanded with support for the salting of the hashed data. An expanded awareness and implementation of error handling also further reinforces the security mindset by hedging against potential threats to the stability of the application.

## Enhancement Category 3: Databases
The new financial data dashboard would have to throw out everything from the animal shelter database and replace it with randomly-generated-but-reasonably-accurate account data. I've included the process and methodology of generating that data [at the end of the page here.](https://holmessnhu.github.io/#creating-the-new-data) I would also need to create a login database to handle the login credentials and access level for each user.

One of the challenges I faced with enhancing the databases portion of this project was that it was already utilizing MongoDB as part of its technology stack. At first blush, I thought that might be as good as it got, but as I dug into the process of reinforcing the security aspects of the dashboard I realized how much more could be done for the database to reinforce it for public use and how precariously it was situated on ensuring that everything went exactly as it was meant to go. 

### Collaboration
My work in expanding permissions and access control allows for multiple users to work simultaneously on data stored in a single database while maintaining security and integrity of that data, improving collaboration prospects for users. Adequate documentation on the development side improves the collaboration prospects for developers as well.

### Data Structures / Software Engineering
When I transitioned the database to use financial data, I improved data redundancy by splitting the data between two collections: one for client records and one for account records. Clients each have a client ID and every account is tied to an existing client through this ID. This allows the data to be kept separately while the dashboard can query both collections and merge the records around the client ID. This also allows for the simple inclusion of derived data. When I began looking into establishing the login database, I learned about and implemented a validation schema in the database, ensuring that a user can only be registered if each data field passes some basic data verification. In addition to assisting with securing the database, this also helps to make it more robust and resistant to costly data errors. Designing the database data model, the validation schema, implementing efficient access control and user authentication processes all work together to serve these outcomes.

### Security
The security layer I wrote would tie everything together into a more secure package by creating the login database and using it to validate users before granting them access to the data in the clients and accounts databases. In addition to the security benefits, this would allow the dashboard to serve many different users instead of just one. Once properly hosted, the app will manage login authentication, verification, and session management for multiple users. User registration is implemented through the dashboard currently for demonstration purposes only, since privileged user accounts should be set up through a more involved process. These inclusions ensure that a user must have the requisite permissions level before they can access sensitive financial data, which represents a critical step in ensuring the security of the database.

A vast portion of my enhancements across the entire project were focused on improving the security and reliability of the system as a whole, given how many of them have been centered around reinforcing and improving the security of the database to allow for regulatory-adherent storage of sensitive information. From shifting server credentials out of the application code to implementing a security layer to handle user authentication, session management, and user account handling, nearly every enhancement has been focused on security. While all of the data in the databases currently has been generated pseudo-randomly, this near-obsession with a security focus stands as a proof of concept for the potential use with legitimate client financial data.

### Communications
Documenting all of the changes to the database, its access control mechanisms, new access roles, and dramatically expanding the commenting and console messaging of the application stands as an endorsement towards the communications outcome—though admittedly, more can be done here to truly make it usable for anyone and not just trained or familiar personnel.

## Course Outcomes
To summarize my enhancements and the outcomes that they served beyond just the category of those enhancements, here is a quick breakdown for convenience:

### Collaboration
* Adequate documentation of data models, validation schema, and data generation processes so that others can understand the reasoning and the layout and quickly utilize them as well.
* Extensive inline and header commenting to ensure each file clearly explains what it's for and how it's doing it to ensure future collaborators can jump right in with minimial acclimation time.
### Communication
* Detailed code review examining the original artifact, reasoning through its inadequacies, and planning its enhancements
* Extensive inline and header commenting designed to facilitate understanding through indirect communications
### Data Structures & Algorithms
* Designing data models and database schema to reduce redundancy, improve the separation of concerns, and increase efficiency while achieving objectives
* Identifying and implementing algorithms for password hashing, security token, and session ID generation
* Caching where possible to minimize the number of database calls to improve efficiency
### Software Engineering
* Redesigning the application from a dashboard and simple CRUD / database structure to include a robust security layer
* Building a security layer to handle user authentication, session management, and role-based access control
* Redesigning the dashboard to cleanly support a login layout that enables user login authentication and registration
### Security
* Correcting security vulnerabilities by abstracting credential verification from hard-coded solution to a protected configuration file
* Designing and implementing a login authentication system to enforce role-based access control to sensitive data
* Managing session IDs and security tokens to help minimize the chance of unauthorized personnel gaining access to sensitive data

## The Enhanced Artifact
Finally, here is the enhanced artifact, split as it was to maintain separation of concerns:
* Link to ClientDataDashboard - The Dashboard which handles the display and retrieval of data.
* Link to ClientDataCRUD - The CRUD layer that interfaces between the dashboard and the database.
* Link to ClientDataSecurity - The security layer that interfaces between the other components to handle user authentication and session management.

I also created a unit test driver for testing the security layer while it was being developed before the login system had been adequately developed, which can be found below:
* Link to SecurityTestDriver

I’ve learned a great deal in the journey to get here, but one sticks most in my mind is how much more I’d like to do. As I worked, I made a note in the comments of the code marked by tags like <IMPROVEMENT> or <CORRECTION> of aspects that I felt could be improved in clear and certainly valuable ways, but which sat outside the scope of the current enhancement plan. With each feature I implemented, I felt that while I achieved many of the goals I had set out to achieve, new, more involved goals would appear and tempt me towards deviating from the plan to dig deeper onto a given feature and expand how robust or valuable it was. It was an ongoing struggle throughout the project to stay focused on the task at hand and not get lost in the weeds of maximizing the modularity of components or templating functions far beyond where they needed to go. Having a plan from the start was absolutely critical in keeping myself from meandering onto improvements that would be technically superior but not relevant to the task at hand, and while “planning is invaluable” is hardly a new concept, it’s certainly valuable to see it reinforced time after time.

## Creating the New Data
The artifact enhancements described above would have been far more difficult without a set of practice data in the database to use during testing and verification. Using real data was obviously out of the question as it is sensitive, private data, so the economical route was to generate the data randomly but within the guidelines of what my experience would suggest to be realistic data that one might find in such records. This technically falls outside of the scope of the artifact enhancement project, but I felt it was an interesting enough process that it was worth detailing, so I included the process and methodology I followed below.

### Defining the Database
Before any meaningful enhancements to the original artifact could be made, I first needed data with which to populate the database for testing. I needed to generate fictional data that looked enough like legitimate data to make for valid testing material while still obviously fake. This is the best opportunity to consider the database design since having that in place prior to writing code for interacting with it will be critical in ensuring that I don't have a lot of extra work to do in the future. To that end, I developed the following data model for the database:

* Link to Data Model

This model divides the required data into two main groups: clients and accounts. Accounts are further subdivided into another two groups: non-retirement accounts and retirement accounts. In both cases, this division is important to ensure that there is minimal redundancy in the data itself. Each account must have a client associated with it, so rather than having the client data attached to each account entry, that client data is separated into its own Clients data collection with all of the important client details stored there. Each account then has a valid client ID associated with it which links to that client record.

The account types themselves are split between retirement accounts and non-retirement accounts due to retirement accounts having a greater level of regulatory requirements associated with them. The IRS requires that once the holder of a retirement account reaches a certain age, they must begin taking required minimum distributions (RMDs) from their retirement accounts each year or face enormous penalties. The specific amount is calculated using life-expectancy tables and year-end account values, but that is outside the purview of this project; what I'm concerned with is providing the data necessary to help ensure these RMDs are taken. In the context of a wealth management firm handling client investments it's an important element of customer service to assist with these requirements, so tracking them becomes a major part of the finance administrator's responsibilities. Nor is it the least of these responsibilities as if these distributions are not taken the client is responsible for the associated penalties--which can reach into the tens or hundreds of thousands of dollars depending on the given account value.

Non-retirement accounts, however, are not subject to these requirements and thus have no need to track an RMD amount at all. Dividing these account types up based on this allows us to make valuable assumptions about the data in each account's record while ensuring that there are no 'empty' or 'dead' data fields for accounts that do not need them. This division is also helpful in a number of other ways outside of the scope of this project, so it's valuable to design the database with this in mind ahead of time to empower future development and extensibility.

### Generating the Database
With the data model in place, the data needed to populate the database can now be generated. I did this using custom generation scripts for clients and accounts. Since accounts are dependent on extant clients, the data was generated in two steps: first the client data is generated and fed into the database, then exported and provided to the account generation script so that each account can be attached to a client.

* Link to Client Data Script

The client data generation process is fairly straightforward. From the US Census department I sourced the 500 most common first names as of 2022 and the 500 most common surnames as of 2010 and provided those as `names.txt` and `surnames.txt`, which are linked below:

* Link to names
* Link to surnames

The generation script pulls the names from these files and stores it internally for later use. It defines a function to generate a random, unique social security number (SSN) made up of three letters followed by 6 numbers to accurately model an SSN but make it explicitly clear that it is not real data and is not tied to any real individual. It then takes an arbitrary number of clients to generate and creates the client data accordingly for each field. Each fictional client has their names are randomly selected from the names and surnames provided, a date of birth generated to place them between the ages of 18 and 80, an SSN generated using the previously defined function, and a field called 'last_review_date' given a date sometime within the last 500 days. This field is used to calculate the number of days since their last review with the financial advisor, which is an important element in the US financial industry's regulation of wealth management firms and therefore an important aspect of finance administration.

This data is then output into a .csv file for later use. The one I used for this project is available below:

* Link to client_data.csv

Once the client data has been generated, it is imported into the MongoDB database that has been set up with the necessary data validation restrictions. Each client record is then exported again; this step is critical because once the data has been imported, MongoDB assigns it a client_id which will be used to tie each account to the owning client.

* Link to clients_export.csv
* Link to Account Data Script

The script imports the client data as it was exported from the database for later use during the generation process. It then creates a function to take that data and generate an arbitrary number of accounts associated with those clients. It sets a few other arbitrary limits to help the data appear to be more realistic such as a maximum number of accounts per client and a percentage of the accounts to be made as retirement accounts.

Then it generates the data for each account. It chooses an eligible client and randomly determines whether it's a retirement account or not based on the weight provided previously. It then chooses a sub-type for the account ('Rollover IRA', 'TOD Account', etc.) based on the type and applies a nickname with that information and the client's name to make it a little more realistic. It then generates several account statistics randomly within certain ranges to help improve the data and differentiate it adequately and applies an RMD amount to the relevant accounts. These are all then output into a .csv file for database import. The one I used for this project is provided below:

* Link to account_data.csv

With the data now ready, everything would be in place to begin the artifact enhancements.