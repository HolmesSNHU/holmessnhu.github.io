# ePortfolio - Jason Holmes

My name is Jason Holmes. I currently live in Tokyo and have recently completed the Computer Science bachelor's program at Southern New Hampshire University (SNHU). I prepared this ePortfolio as part of my Computer Science capstone course with the intent to highlight my capabilities and my strengths. Through this I intend to seek a career in game development focusing on design and software engineering.

## Table of Contents
* [Professional Self-Assessment](https://holmessnhu.github.io/#professional-self-assessment)
* [Artifact Selection](https://holmessnhu.github.io/#artifact-selection)
* [Code Review](https://holmessnhu.github.io/#code-review)
* [Project Structure and Planning](https://holmessnhu.github.io/#project-structure-and-planning)
    * [Defining the Database](https://holmessnhu.github.io/#defining-the-database)
    * [Generating the Database](https://holmessnhu.github.io/#generating-the-database)
* [Artifact Enhancement 1: Software Engineering & Design](https://holmessnhu.github.io/#)
* [Artifact Enhancement 2: Data Structures & Algorithms](https://holmessnhu.github.io/#)
* [Artifact Enhancement 3: Databases](https://holmessnhu.github.io/#)
* [Course Outcomes](https://holmessnhu.github.io/#course-outcomes)

## Professional Self-Assessment
My computer science journey began in high school taking Java-based Advanced Placement-certified courses in computer science and programming alongside basic HTML development. After high school, I supplemented this education with many years of self-teaching and learning while navigating through life, during which time I taught myself C++ and the higher level concepts behind object-oriented programming, then later C#, Python, and higher level web development concepts including the basics behind the technology stack of modern website design.

This culminated most recently in enrolling at SNHU to formalize what I have learned, reinforce any areas that I had overlooked, and expand my knowledge wherever I could. During my time in the program, I expanded my understanding of data structures and algorithms, gained a more in-depth understanding of full stack development, and earned experience in leading a small team through the game development process from planning and development to private release.

Collaborating in a team environment is difficult experience to acquire outside of a professional environment, because self-directed projects tend to have fewer stakes. A game jam team might get together for the jam and then split apart, assuming that jam is even completed. For a larger project that becomes even more of a problem as the ugly and difficult parts of software development rear their heads; without the obligation imposed by a drawn salary or a pending grade, there's nothing stopping a team member from disappearing at the first obstacle. For these reasons, the GAM-305 Digital Game Development course is one of my favorite experiences throughout my time at SNHU; spending time with a stable team that have obligations to themselves and each other to work on and finish the project gave me ample opportunity to experience collaborating in a team environment. I also took on the producer and project lead role for the team, experiencing the tribulations of creating a design, identifying and scheduling the work that needs to be done, and guiding a team through several weeks of development. It is undoubtedly the most valuable experience I gained during my time in the program.

Communicating with diverse audiences is a core skill in software development. Without the ability to communicate clearly with a variety of technical backgrounds, it can quickly become impossible to do simple things like identify client needs, understand and communicate the difficulties associated with a given feature or request, or even prepare documentation on the software you create either to allow others to use it or even just to allow yourself to come back to a section of code later and understand the thought process you had when writing it. This is a skill I have been honing for many years, and every course allowed me to practice it in greater measure by interpreting rubrics, discussing course material with peers, and communicating with professors through email as well as tailored assignments. Well-commented code is a skill that was drilled into me from the first moments of my programming education, which will be clearly evident in the code presented later in the portfolio.

Data structures and algorithms represented the biggest challenge when coming into the program at SNHU, and I was excited to dig into it during the program. While my early education taught me the principles behind algorithm design, Big-O notation, and the importance of efficiency, learning which algorithms had which strengths and when was appropriate to implement which was something that had eluded me during my self-teaching process. Getting to experience and understand those things during my Data Structures & Algorithms course was a highlight of my time in the program.

My goal of working in the game development industry is centered around using software engineering as an invaluable asset in making myself an attractive asset to potential employers. In many ways, I see this as the second part of a whole when paired with communicating with diverse audiences, as it is impossible to design effective software without first understanding what goal you're aiming to reach, what problems you're aiming to solve, and what needs must be addressed. Understanding design patterns, the importance of good coding standards, and a full-throated belief in testing and maintenance-supportive design are all critical elements as well. Each one of these elements has been served through the experience I've gained programming in each course; from understanding the purpose behind the animal shelter outcomes dashboard developed in Client/Server Development to designing the game for Digital Game Development and breaking it down into task-sized objectives for the entire team to getting a full grasp of modern website design in Full Stack Development, much of my work in and before the program has been focused on improving my capabilities in software engineering.

Finally, security is increasingly important in modern software engineering. As we handle consumer data in greater and greater volumes, maintaining their privacy--along with protecting our own technology's integrity--should be considered of paramount importance. My self-teaching experience only allowed me to understand the importance of encryption and how that functions, but implementing that in a meaningful, robust way during the courses in Software Security, Client/Server Development, Full Stack Development, and especially the artifact enhancements I'll discuss later has been invaluable in expanding my understanding of the topic.

These five outcomes represent the pillars of the computer science program at SNHU, and this ePortfolio will highlight my alignment in these areas and my capabilities across each outcome as well as three major categories of software development: software engineering & design, data structures & algorithms, and databases. To this end, for this ePortfolio I have selected an artifact from one of the courses that I've taken and will enhance it along several vectors to demonstrate these capabilities.

## Artifact Selection

While I had the opportunity to choose a separate artifact for each of the three major categories of software engineering & design, data structures & algorithms, and databases, I chose instead to use a single artifact; a database visualization dashboard originally created for a project during my Client/Server Development course. This dashboard utilized a MongoDB database of animal shelter outcomes, a CRUD interface layer written in Python using PyMongo, and a dashboard built with the Dash by Plotly framework to visualize and display the animal shelter outcomes for use by a third-party to identify animal candidates for search-and-rescue training.

This artifact was chosen for two primary reasons. The first reason is that it is essentially a full stack application that covers all three refinement categories, which would allow me to focus all of my attention on this project to really showcase my capabilities for the ePortfolio. The entirety of the CRUD layer and a good portion of the dashboard were written entirely by me, so it’s not so much about making a few minor changes to someone else’s code as it is expanding and enhancing something I’d written before, which lines up with the artifact expectations. The second major reason I chose this is because it is very similar to some tools I used in my previous job working in finance administration for a wealth management firm and I could easily envision how it could be adapted to serve that purpose in a bespoke, performant way. The end result of this project would make a fantastic foundation for an actual, usable application for my previous job.

## Code Review

{% include youtube.html id="blLPAqMX2sw" %}

The dashboard code for the original artifact is available here:
* Link to AnimalShelterDashboard
* Link to AnimalShelterCRUD

This dashboard visualizes animal shelter patient outcome data in the Austin, TX region for a fictional client looking for an easy way to identify search-and-rescue animal training candidates.  outcomes provided by the original course, presenting a dashboard that allows the data to be filtered and sorted along with two visualizations of the data to help users understand it at a glance. However, much of the data presented is useless to the users who are looking for search-and-rescue training candidates. This is addressed with bespoke filters that have a specific set of requirements for each type of training that the user can call up at the click of the filter button, automatically displaying all of the relevant candidates.

The dashboard pulls the data stored in a MongoDB database through the use of a bespoke Python-based CRUD (Create, Read, Update, Delete) layer that enables interaction with the database using PyMongo, a framework that provides the necessary functions. This layer accepts requests from the dashboard and translates them into PyMongo requests, which apply them to the MongoDB database to fetch and change data. The dashboard then generates the HTML for the page and displays it using a callback system for updating those elements with the new data. MongoDB implements a role-based access control system to ensure that only valid users can access the data, which this dashboard bypasses using hard-coded administrator credentials.

## Project Structure and Planning

Updating this dashboard for use in financial administration will mean a great deal of adaptation. The data would of course need to be thrown out and replaced with financial data, then the dashboard itself would need to be updated to accurately reflect this data. The filters too would need to be updated to reflect what would be considered relevant to that data. In my previous experience in finance administration, this would include things like whether a given account is a non-retirement account or a retirement account, which dictates how those accounts are managed and what kinds of assets they can (and should) hold and whether or not certain annual regulatory requirements have been met.

Finally, the security present in the dashboard as-is would be considered woefully inadequate for a final product; anyone accessing this page would have immediately, unfiltered access to all of the data in the database. This is one thing when considering a private application with unimportant data, but when considering a web-based application with sensitive financial data, security immediately becomes the most important element to consider, so we will need to add a login system with authentication, user accounts and role-based access control, session management, and other security features to bring this up to a minimum level of sophistication adequate for handling financial data. We'll discuss this in greater detail for the later enhancement categories.

### Defining the Database
Before we can make any meaningful updates to the existing system however, we will need data with which to populate the database for testing. It goes without saying tha we cannot use real data here as that is sensitive information, so we will need to generate data that looks enough like legitimate data to make for valid testing material. This is the best opportunity for us to consider the database design, since having that in place prior to writing code for interacting with it will be critical in ensuring that we don't have a lot of extra work to do in the future. To that end, I developed the following data model for the database:

* Link to Data Model

This model divides the required data into two main groups: clients and accounts. Accounts are further subdivided into another two groups: non-retirement accounts and retirement accounts. In both cases, this division is important to ensure that there is minimal redundancy in the data itself. Each account must have a client associated with it, so rather than having the client data attached to each account entry, that client data is separated into its own Clients data collection with all of the important client details stored there. Each account then has a valid client ID associated with it which links to that client record. 

The account types themselves are split between retirement accounts and non-retirement accounts due to retirement accounts having a greater level of regulatory requirements associated with them. The IRS requires that once the holder of a retirement account reaches a certain age, they must begin taking required minimum distributions (RMDs) from their retirement accounts each year or face enormous penalties. The specific amount is calculated using life-expectancy tables and year-end account values, but that is outside the purview of this project; what we're concerned with is ensuring that these RMDs are taken. In the context of a wealth management firm handling client investments, it's an important element of customer service to assist with these requirements, so tracking them becomes a major part of the finance administrator's responsibilities; not least of which because if they are not taken, the client is responsible for the associated penalties which can reach into the tens or hundreds of thousands of dollars depending on the given account value.

However, non-retirement accounts are not subject to these requirements and thus have no need to track an RMD amount at all. Dividing these account types up based on this allows us to make valuable assumptions about the data in each account's record while ensuring that there are no 'empty' or 'dead' data fields for accounts that do not need them. This division is also helpful in a number of other ways outside of the scope of this project, so it's valuable to design the database with this in mind ahead of time for extension purposes.

### Generating the Database
With this data model in place, we can now generate the data that we need to populate the database. I did this using custom generation scripts for clients and accounts. Since accounts are dependent on extant clients, the data was generated in two steps: first the client data is generated and fed into the database, then exported and provided to the account generation script so that each account can be attached to a client.

* Link to Client Data Script

The client data generation process is fairly straightforward. From the US Census department I sourced the 500 most common first names as of 2022 and the 500 most common surnames as of 2010 and provided those as `names.txt` and `surnames.txt`, which are linked below:

* Link to names
* Link to surnames

The generation script pulls the names from these files and stores it internally for later use. It defines a function to generate a random, unique social security number (SSN) made up of three letters followed by 6 numbers to accurately model an SSN but make it explicitly clear that it is not real data and is not tied to any real individual. It then takes an arbitrary number of clients to generate and creates the client data accordingly for each field. Each fictional client has their names are randomly selected from the names and surnames provided, a date of birth generated to place them between the ages of 18 and 80, an SSN generated using the previously defined function, and a field called 'last_review_date' given a date sometime within the last 500 days. This field is used to calculate the number of days since their last review with the financial advisor, which is an important element in the US financial industry's regulation of wealth management firms and therefore an important aspect of finance administration.

This data is then output into a .csv file for later use. The one I used for this project is available below:

* Link to client_data.csv

Once the client data has been generated, it is imported into the MongoDB database that has been set up with the necessary data validation restrictions. Each client record is then exported again; this step is critical because once the data has been imported, MongoDB assigns it a client_id which we plan to use for each account to tie it to the owning client.

* Link to clients_export.csv
* Link to Account Data Script

The script imports the client data as it was exported from the database for later use during the generation process. It then creates a function to take that data and generate an arbitrary number of accounts associated with those clients. It sets a few other arbitrary limits to help the data appear to be more realistic such as a maximum number of accounts per client and a percentage of the accounts to be made as retirement accounts.

Then it generates the data for each account. It chooses an eligible client and randomly determines whether it's a retirement account or not based on the weight provided previously. It then chooses a sub-type for the account ('Rollover IRA', 'TOD Account', etc.) based on the type and applies a nickname with that information and the client's name to make it a little more realistic. It then generates several account statistics randomly within certain ranges to help improve the data and differentiate it adequately and applies an RMD amount to the relevant accounts. These are all then output into a .csv file for database import. The one I used for this project is provided below:

* Link to account_data.csv

With the data now ready, we can move on to enhancing the artifact.

## Artifact Enhancements
* For each of the three major categories of software design & engineering, algorithm & data structures, and databases, include a written narrative describing in detail the enhancements for each category. This can and should be adapted from the submitted milestones after incorporating feedback from the original submissions.
* Each course outcome that is addressed in the enhancement should be presented clearly and explicitly here. I'm thinking of having each category section broken down into an introduction section followed by sections divided and headed by which outcomes they address.

## Course Outcomes
* For each of the 5 major course outcomes, summarize which enhancements addressed the outcome.